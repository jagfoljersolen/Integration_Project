from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Commodity


class CorrelationView(TemplateView):
    template_name = 'tables/correlations.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        raw_rows = list(Commodity.objects.all().values())

        if not raw_rows:
            ctx['column_verbose_names'] = []
            ctx['rows'] = []
            return ctx

        column_order = list(raw_rows[0].keys())

        field_verbose_map = {
            f.name: f.verbose_name for f in Commodity._meta.fields
        }

        column_verbose_names = []
        for col in column_order:
            if col in field_verbose_map:
                column_verbose_names.append(field_verbose_map[col])
            else:
                column_verbose_names.append(col.replace('_', ' ').capitalize())

        ctx['rows'] = raw_rows
        ctx['column_verbose_names'] = column_verbose_names

        return ctx