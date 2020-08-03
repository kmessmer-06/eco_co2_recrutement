from django.db import models


class BaseModel(models.Model):
    """
        BaseModel inherited in models Consumption and ConsumptionInterpolate
    """

    datetime = models.DateTimeField(
        verbose_name="datetime",
    )

    co2_rate = models.PositiveIntegerField(
        verbose_name="co2_rate"
    )

    def __str__(self):
        return "{} - {}".format(self.datetime, self.co2_rate)

    class Meta:
        ordering = ['datetime']
        abstract = True


class Consumption(BaseModel):
    pass


class ConsumptionInterpolate(BaseModel):
    pass
