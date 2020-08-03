from django.views.generic import TemplateView
from src.co2_consumption.models import (ConsumptionInterpolate, Consumption,
                                        Season)
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter
from django.apps import apps
from statistics import median, mean
from django.db.models import Q
from collections import OrderedDict


class IndexView(TemplateView):
    """
        Controller used to display all the results of the exercice I did.
    """
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        years = [2017, 2018]

        df_original = pd.DataFrame(
            Consumption.objects.all().order_by('datetime').values()
        ).set_index('datetime')

        df_interpolated = pd.DataFrame(
            ConsumptionInterpolate.objects.all().order_by('datetime').values()
        ).set_index('datetime').resample('30T').asfreq().interpolate()

        # Using ffill() to fill the last data of the dataframe.
        df_diff = df_original['co2_rate'].sub(
            df_interpolated['co2_rate']
        ).ffill()

        context['graph_diff'] = plot([Scatter(
                x=df_original.groupby(
                    pd.Grouper(freq='15D')
                ).mean().index.tolist(),
                y=df_diff,
                mode='lines',
                name='graph difference between original and interpolated',
                opacity=0.8,
                marker_color='green'
            )],
            output_type='div'
        )

        for model in ('Consumption', 'ConsumptionInterpolate'):

            context[
                'median_season_'+model.lower()
            ] = self.make_season_stats(model, years)

            context['weekdays_mean_'+model.lower()],context['weekend_mean_'+model.lower()] = self.make_weekdays_stats(model)

        return context

    def make_season_stats(self, model_name, years):
        """
            Method used to calculate stats on season for models Consumption and ConsumptionInterpolate
        """
        model = apps.get_model(
            app_label='co2_consumption',
            model_name=model_name
        )

        seasons = [season for season in Season.objects.filter(
            Q(start_date__year__in=years) | Q(end_date__year__in=years)
        )]

        median_by_season = OrderedDict()

        for season in seasons:
            season_name = "{} {}".format(season.name, season.start_date.year)
            median_by_season[season_name] = median(
                model.objects.filter(
                    datetime__lte=season.end_date,
                    datetime__gte=season.start_date
                ).values_list('co2_rate', flat=True)
            )

        return median_by_season

    def make_weekdays_stats(self, model_name):
        """
            Method used to calculate stats on days for models Consumption and ConsumptionInterpolate
        """
        model = apps.get_model(
            app_label='co2_consumption',
            model_name=model_name
        )

        weekdays_values = []
        weekend_values = []

        for instance in model.objects.all():
            if instance.datetime.weekday() < 5:
                weekdays_values.append(instance.co2_rate)
            else:
                weekend_values.append(instance.co2_rate)

        return mean(weekdays_values), mean(weekend_values)