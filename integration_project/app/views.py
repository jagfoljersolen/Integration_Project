from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Commodity, Conflict
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import logging
from django.db.models import Count, Q
import json


class CorrelationView(TemplateView):
    template_name = 'tables/correlations.html'

    # Map user‐facing codes → actual column names in the DB
    JOIN_CHOICES = {
        "year" : "year"
    }

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
    





def commodity_dashboard(request):
    
    commodities = []

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

@require_GET
def commodity_data_api(request):
    commodity = request.GET.get('commodity', 'cocoa')
    
    try:
        if not hasattr(Commodity, commodity):
            return JsonResponse({
                'error': f"Invalid commodity field: {commodity}"
            }, status=400)

        filter_kwargs = {f'{commodity}__isnull': False}
        queryset = Commodity.objects.filter(**filter_kwargs).order_by('year')
        
        if not queryset.exists():
            return JsonResponse({
                'error': f"No data available for {commodity}"
            }, status=404)
            
        data = {
            'years': [c.year for c in queryset],
            'prices': [float(getattr(c, commodity)) for c in queryset],
            'commodity_name': commodity.replace('_', ' ').title()
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        logger.error(f"API Error: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': 'Internal server error'
        }, status=500)
    



def conflict_dashboard(request):
    # Base queryset
    conflicts = Conflict.objects.all()
    
    # Main aggregations
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


@require_GET
def conflict_data_api(request):
    conflicts = Conflict.objects.all()
    
    yearly_data = list(conflicts.values('year').annotate(
        total=Count('conflict_id')
    ).order_by('year'))
    
    return JsonResponse({
        'yearly_data': yearly_data
    }) 



def conflicts_vs_commodities(request):

    conflicts = Conflict.objects.all()

    yearly_data = list(conflicts.values('year').annotate(
        total=Count('conflict_id')
    ).order_by('year'))
    
    # Prepare commodity list
    commodities = []

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
    
    # Check which commodities have data
    for field, name in commodity_fields:
        if hasattr(Commodity, field):
            # Check if any records have data for this field
            filter_kwargs = {f'{field}__isnull': False}
            if Commodity.objects.filter(**filter_kwargs).exists():
                commodities.append({'field': field, 'name': name})
    
    context = {
        'yearly_data': yearly_data,
        'commodities': commodities,
        'default_commodity': 'cocoa' if commodities else None,
        'commodity_fields': commodity_fields}
    
    return render(request, 'conflicts_vs_commodities.html', context)
