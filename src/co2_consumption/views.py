from django.views.generic import TemplateView
from src.co2_consumption.models import ConsumptionInterpolate, Consumption
import pandas as pd


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

        return context