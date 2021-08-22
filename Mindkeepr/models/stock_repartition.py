from django.db import models


class StockRepartition(models.Model):
    """ Represents a stock element (like a _lot_), a set of Element that have
     a status, a location and a project (if status is RESERVED) """
    """ TODO : Add project if reserved """
    STATUS = {
        ('FREE', "Free"),
        ('RESERVED', "Reserved")
    }
    location = models.ForeignKey(
        'location', on_delete=models.PROTECT, null=True, related_name="stock_repartitions")
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    status = models.CharField("Status",
                              null=False,
                              blank=False,
                              max_length=200,
                              choices=STATUS)
    element = models.ForeignKey('Element',
                                on_delete=models.PROTECT,
                                related_name='stock_repartitions',
                                null=True)
    project = models.ForeignKey('Project', on_delete = models.PROTECT, related_name='stock_repartitions',null=True)
    class Meta:#todo add project to constraint
        constraints = [
            models.UniqueConstraint(fields=[
                                    'element', 'location', 'status','project'], name='Unique set of location, status and element'),
        ]
        # todo also override  validate_unique method