from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Commodity, Conflict


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