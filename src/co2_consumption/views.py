from django.views.generic import TemplateView
from src.co2_consumption.models import ConsumptionInterpolate, Consumption
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter


class IndexView(TemplateView):
    """
        Controller used to display all the results of the exercice I did.
    """
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

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

        return context