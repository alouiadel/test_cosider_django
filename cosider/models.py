from django.db import models


class Invoice(models.Model):
    invoice_id = models.CharField(max_length=100)
    invoice_date = models.DateField()
    client_name = models.CharField(max_length=100)
    supplier_name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_ht = models.DecimalField(default=0, max_digits=10, decimal_places=2)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item_label = models.CharField(max_length=100)
    item_unit = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    total_item_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_price_ht = models.DecimalField(default=0, max_digits=10, decimal_places=2)
