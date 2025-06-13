from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .models import Commodity, Conflict
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import logging
from django.db.models import Count, Q, Avg, Max, Min
import json

from .forms import CreateUserForm, CreateLoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required

from django.db import connection, transaction
from functools import wraps

from enum import Enum, unique


@unique
class IsolationLevel(Enum):
    READ_UNCOMMITTED = "READ UNCOMMITTED"
    READ_COMMITTED   = "READ COMMITTED"
    REPEATABLE_READ  = "REPEATABLE READ"
    SERIALIZABLE     = "SERIALIZABLE"

    def __str__(self):
        # dla wygody, gdy będziesz wypisywać IsolationLevel.READ_COMMITTED
        return self.value


def transactional(isolation:IsolationLevel=IsolationLevel.READ_COMMITTED, read_only=True, timeout=None):
    """
    Function decorator for performing parametrized transactions.

    isolation: isolation level 'READ UNCOMMITED' | 'READ COMMITTED' | 'REPEATABLE READ' | 'SERIALIZABLE'
    read_only: True | False
    timeout: maximum transaction duration in miliseconds
    """
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with transaction.atomic():
                with connection.cursor() as cur:
                    cur.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation};")

                    if read_only:
                        cur.execute("SET TRANSACTION READ ONLY;")
                    if timeout and isinstance(timeout, int):
                        cur.execute(f"SET LOCAL statement_timeout = {timeout};")
                return fn(*args, **kwargs)
        return wrapper
    return deco

@transactional(timeout=10000)
@login_required(login_url='app:login')
def main_dashboard(request):
    """
    Main dashboard view that aggregates data from commodity and conflict models
    """
    # Get summary statistics
    total_commodities = Commodity.objects.values('year').distinct().count()
    total_conflicts = Conflict.objects.count()
    
    # Get latest data points
    latest_commodity_year = Commodity.objects.aggregate(Max('year'))['year__max']
    latest_conflict_year = Conflict.objects.aggregate(Max('year'))['year__max']
    
    context = {
        'total_commodities': total_commodities,
        'total_conflicts': total_conflicts,
        'latest_commodity_year': latest_commodity_year,
        'latest_conflict_year': latest_conflict_year,
        'data_range': f"{Commodity.objects.aggregate(Min('year'))['year__min']}-{latest_commodity_year}",
    }
    
    return render(request, 'main_dashboard.html', context)

@transactional(timeout=10000)
@login_required(login_url='app:login')
def dashboard_commodity_api(request):
    """
    API endpoint for commodity data used by dashboard charts
    """
    commodity = request.GET.get('commodity', 'cocoa')
    
    try:
        if not hasattr(Commodity, commodity):
            return JsonResponse({'error': f'Invalid commodity: {commodity}'}, status=400)
        
        # Get data for the selected commodity
        filter_kwargs = {f'{commodity}__isnull': False}
        queryset = Commodity.objects.filter(**filter_kwargs).order_by('year')
        
        data = {
            'years': [c.year for c in queryset],
            'prices': [float(getattr(c, commodity)) for c in queryset],
            'commodity_name': commodity.replace('_', ' ').title()
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@transactional(timeout=30000)
@login_required(login_url='app:login')
def dashboard_conflict_api(request):
    """
    API endpoint for conflict data used by dashboard charts
    """
    try:
        # Yearly conflict data
        yearly_data = list(Conflict.objects.values('year').annotate(
            total=Count('conflict_id'),
            type1=Count('conflict_id', filter=Q(type_of_conflict=1)),
            type2=Count('conflict_id', filter=Q(type_of_conflict=2)),
            type3=Count('conflict_id', filter=Q(type_of_conflict=3)),
            type4=Count('conflict_id', filter=Q(type_of_conflict=4))
        ).order_by('year'))
        
        # Location data
        location_data = list(Conflict.objects.values('location').annotate(
            count=Count('conflict_id')
        ).order_by('-count')[:10])
        
        # Intensity data
        intensity_data = list(Conflict.objects.values('intensity_level').annotate(
            count=Count('conflict_id')
        ).order_by('intensity_level'))
        
        return JsonResponse({
            'yearly_data': yearly_data,
            'location_data': location_data,
            'intensity_data': intensity_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {})
    return redirect('app:login')

def register_view(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:login')
    
    context = { 'register_form': form }
    
    return render(request, 'auth/register.html', context)

def login_view(request):

    form = CreateLoginForm(request)
    if request.method == 'POST':
        form = CreateLoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')


            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)
                return redirect('app:main_dashboard')
        else:
            print(form.errors) 
    
    context = { 'login_form': form }
    
    return render(request, 'auth/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('app:login')

class CorrelationView(TemplateView):
    template_name = 'tables/correlations.html'

    # Map user‐facing codes → actual column names in the DB
    JOIN_CHOICES = {
        "year" : "year"
    }

    @transactional(timeout=10000)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Read table choice from url.
        table_choice = self.request.GET.get('table', 'commodities').lower()
        if table_choice not in ('commodities', 'conflicts', 'join'):
            raise Http404('Invalid table name.')

        # User can choose between two distinct tables or 
        #   join them on given fileds.
        if table_choice == 'commodities':
            raw_rows = list(Commodity.objects.all().values())

            field_verbose_map = {
                f.name: f.verbose_name for f in Commodity._meta.fields
            }
        elif table_choice == 'conflicts':
            raw_rows = list(Conflict.objects.all().values())

            field_verbose_map = {
                f.name: f.verbose_name for f in Conflict._meta.fields
            }
        elif table_choice == 'join':
            # 1) Figure out which join‐key the user selected (default to first)
            user_choice = self.request.GET.get("join_on", None)
            if user_choice not in self.JOIN_CHOICES:
                user_choice = next(iter(self.JOIN_CHOICES))  # first key

            join_col = self.JOIN_CHOICES[user_choice]

            conflict_rows = list(Conflict.objects.all().values())
            commodity_rows = list(Commodity.objects.all().values())

            commodity_index = {}
            for row in commodity_rows:
                key = row.get(join_col)
                commodity_index.setdefault(key, []).append(row)

            merged = []
            for a in conflict_rows:
                key = a.get(join_col)
                matches = commodity_index.get(key, [])
                for b in matches:
                    merged_row = {**a, **b}
                    merged.append(merged_row)
            
            raw_rows = merged
            
            field_verbose_map = {}
            for f in Commodity._meta.fields:
                field_verbose_map[f.name] = f.verbose_name
            for f in Conflict._meta.fields:
                # if a Commodity field name conflicts with Conflict’s, you can rename here
                field_verbose_map[f.name] = f.verbose_name


        if not raw_rows:
            ctx['column_verbose_names'] = []
            ctx['rows'] = []
            return ctx
        
        # Replace None with empty string.
        for row in raw_rows:
            for key, value in row.items():
                if value is None:
                    row[key] = ""

        column_order = list(raw_rows[0].keys())

        column_verbose_names = []
        for col in column_order:
            if col in field_verbose_map:
                column_verbose_names.append(field_verbose_map[col])
            else:
                column_verbose_names.append(col.replace('_', ' ').capitalize())

        ctx.update({
            'rows': raw_rows,
            'column_verbose_names': column_verbose_names,
            'current_table': table_choice,
            'join_choices': self.JOIN_CHOICES.items()
        })

        return ctx
    

commodity_fields = [
        ('crude_oil_average_bbl', 'Crude Oil Average'),
        ('crude_oil_brent_bbl', 'Crude Oil Brent'),
        ('crude_oil_dubai_bbl', 'Crude Oil Dubai'),
        ('crude_oil_wti_bbl', 'Crude Oil WTI'),
        ('coal_australian_mt', 'Coal Australian'),
        ('coal_south_african_mt', 'Coal South African'),
        ('natural_gas_us_mmbtu', 'Natural Gas US'),
        ('natural_gas_europe_mmbtu', 'Natural Gas Europe'),
        ('liquefied_natural_gas_japan_mmbtu', 'Liquefied Natural Gas Japan'),
        ('natural_gas_index_2010_100', 'Natural Gas Index (2010=100)'),
        ('cocoa', 'Cocoa'),
        ('coffee_arabica_kg', 'Coffee Arabica'),
        ('coffee_robusta_kg', 'Coffee Robusta'),
        ('tea_avg_3_auctions_kg', 'Tea Avg 3 Auctions'),
        ('tea_colombo_kg', 'Tea Colombo'),
        ('tea_kolkata_kg', 'Tea Kolkata'),
        ('tea_mombasa_kg', 'Tea Mombasa'),
        ('coconut_oil_mt', 'Coconut Oil'),
        ('groundnuts_mt', 'Groundnuts'),
        ('fish_meal_mt', 'Fish Meal'),
        ('groundnut_oil_mt', 'Groundnut Oil'),
        ('palm_oil_mt', 'Palm Oil'),
        ('palm_kernel_oil_mt', 'Palm Kernel Oil'),
        ('soybeans_mt', 'Soybeans'),
        ('soybean_oil_mt', 'Soybean Oil'),
        ('soybean_meal_mt', 'Soybean Meal'),
        ('barley_mt', 'Barley'),
        ('maize_mt', 'Maize'),
        ('sorghum_mt', 'Sorghum'),
        ('rice_thai_5_mt', 'Rice Thai 5'),
        ('rice_thai_25_mt', 'Rice Thai 25'),
        ('rice_thai_a_1_mt', 'Rice Thai A 1'),
        ('rice_vietnamese_5_mt', 'Rice Vietnamese 5'),
        ('wheat_us_srw_mt', 'Wheat US SRW'),
        ('wheat_us_hrw_mt', 'Wheat US HRW'),
        ('banana_europe_kg', 'Banana Europe'),
        ('banana_us_kg', 'Banana US'),
        ('orange_kg', 'Orange'),
        ('beef_kg', 'Beef'),
        ('chicken_kg', 'Chicken'),
        ('lamb_kg', 'Lamb'),
        ('shrimps_mexican_kg', 'Shrimps Mexican'),
        ('sugar_eu_kg', 'Sugar EU'),
        ('sugar_us_kg', 'Sugar US'),
        ('sugar_world_kg', 'Sugar World'),
        ('tobacco_us_import_uv_mt', 'Tobacco US Import UV'),
        ('logs_cameroon_cubic_meter', 'Logs Cameroon'),
        ('logs_malaysian_cubic_meter', 'Logs Malaysian'),
        ('sawnwood_cameroon_cubic_meter', 'Sawnwood Cameroon'),
        ('sawnwood_malaysian_cubic_meter', 'Sawnwood Malaysian'),
        ('plywood_sheet', 'Plywood'),
        ('cotton_a_index_kg', 'Cotton A Index'),
        ('rubber_tsr20_kg', 'Rubber TSR20'),
        ('rubber_rss3_kg', 'Rubber RSS3'),
        ('phosphate_rock_mt', 'Phosphate Rock'),
        ('dap_mt', 'DAP'),
        ('tsp_mt', 'TSP'),
        ('urea_mt', 'Urea'),
        ('potassium_chloride_mt', 'Potassium Chloride'),
        ('aluminum_mt', 'Aluminum'),
        ('iron_ore_cfr_spot_mt', 'Iron Ore CFR Spot'),
        ('copper_mt', 'Copper'),
        ('lead_mt', 'Lead'),
        ('tin_mt', 'Tin'),
        ('nickel_mt', 'Nickel'),
        ('zinc_mt', 'Zinc'),
        ('gold_troy_oz', 'Gold'),
        ('platinum_troy_oz', 'Platinum'),
        ('silver_troy_oz', 'Silver')
    ]


@transactional(timeout=10000)
@login_required(login_url='app:login')
def commodity_dashboard(request):
    
    commodities = []

    # Check which commodities have data
    for field, name in commodity_fields:
        if hasattr(Commodity, field):
            # Check if any records have data for this field
            filter_kwargs = {f'{field}__isnull': False}
            if Commodity.objects.filter(**filter_kwargs).exists():
                commodities.append({'field': field, 'name': name})
    
    context = {
        'commodities': commodities,
        'default_commodity': 'cocoa' if commodities else None
    }
    
    return render(request, 'commodities.html', context)



logger = logging.getLogger(__name__)




@transactional(timeout=10000)
@login_required(login_url='app:login')
def conflict_dashboard(request):

    conflicts = Conflict.objects.all()
    
    yearly_data = list(conflicts.values('year').annotate(
        total=Count('conflict_id'),
        type1=Count('conflict_id', filter=Q(type_of_conflict=1)),
        type2=Count('conflict_id', filter=Q(type_of_conflict=2)),
        type3=Count('conflict_id', filter=Q(type_of_conflict=3)),
        type4=Count('conflict_id', filter=Q(type_of_conflict=4))
    ).order_by('year'))
    
    location_data = list(conflicts.values('location').annotate(
        count=Count('conflict_id')
    ).order_by('-count')[:10])
    
    intensity_data = list(conflicts.values('intensity_level').annotate(
        count=Count('conflict_id')
    ).order_by('intensity_level'))
    
    context = {
        'yearly_data': json.dumps(yearly_data),
        'location_data': json.dumps(location_data),
        'intensity_data': json.dumps(intensity_data),
        'conflict_types': json.dumps(dict(Conflict.TYPE_CHOICES)),
    }
    return render(request, 'conflicts.html', context)


@transactional(timeout=30000)
@login_required(login_url='app:login')
@require_GET
def conflict_data_api(request):
    conflicts = Conflict.objects.all()
    
    yearly_data = list(conflicts.values('year').annotate(
        total=Count('conflict_id')
    ).order_by('year'))
    
    return JsonResponse({
        'yearly_data': yearly_data
    }) 


@transactional(timeout=10000)
@login_required(login_url='app:login')
def conflicts_vs_commodities(request):

    conflicts = Conflict.objects.all()

    yearly_data = list(conflicts.values('year').annotate(
        total=Count('conflict_id')
    ).order_by('year'))
    
    commodities = []

    
    for field, name in commodity_fields:
        if hasattr(Commodity, field):
            filter_kwargs = {f'{field}__isnull': False}
            if Commodity.objects.filter(**filter_kwargs).exists():
                commodities.append({'field': field, 'name': name})
    
    context = {
        'yearly_data': yearly_data,
        'commodities': commodities,
        'default_commodity': 'cocoa' if commodities else None,
        'commodity_fields': commodity_fields}
    
    return render(request, 'conflicts_vs_commodities.html', context)

