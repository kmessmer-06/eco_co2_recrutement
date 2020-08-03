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


class Season(models.Model):
    """
        Models used to store Seasons to easily works with.
    """

    NAME_CHOICE = [
        ('winter', 'winter'),
        ('spring', 'spring'),
        ('summer', 'summer'),
        ('autumn', 'autumn'),
    ]

    name = models.CharField(
        verbose_name='name',
        choices=NAME_CHOICE,
        max_length=6,
    )

    start_date = models.DateTimeField(
        verbose_name="start date",
    )

    end_date = models.DateTimeField(
        verbose_name="end date",
    )

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return "{} - {}".format(self.name, self.start_date)
