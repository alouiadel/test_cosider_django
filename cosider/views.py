from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
import requests
from .models import Invoice, InvoiceItem
from django.views.decorators.csrf import csrf_exempt


# Search by item label
def search_invoices(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        invoices = Invoice.objects.filter(
            Q(invoiceitem__item_label__icontains=query) |
            Q(invoiceitem__item_unit__icontains=query) |
            Q(client_name__icontains=query) |
            Q(supplier_name__icontains=query)
        ).distinct()
        return render(request, 'search_results.html', {'invoices': invoices, 'query': query})


# Print invoice
@csrf_exempt
def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
    context = {'invoice': invoice}
    return render(request, 'print_invoice.html', context)


# Fetch invoice data from external service and display it
# The view had to be cleared and not appended to the existing one
@transaction.atomic  # This decorator ensures that the database is not left in an inconsistent state if an error occurs
def fetch_invoices(request):
    url = 'https://elhoussam.github.io/invoicesapi/db.json'
    response = requests.get(url)
    data = response.json()
    # Clear existing data
    Invoice.objects.all().delete()
    for invoice_data in data:
        # Extract invoice data
        invoice_id = invoice_data['InvoiceID']
        invoice_date = invoice_data['InvoiceDate']
        client_name = invoice_data['ClientName']
        supplier_name = invoice_data['SupplierName']
        total_amount = (sum(item['ItemPrice'] for item in invoice_data['InvoiceItems'])
                        + sum(item['ItemTax'] for item in invoice_data['InvoiceItems']))
        # Create Invoice object
        invoice = Invoice.objects.create(
            invoice_id=invoice_id,
            invoice_date=invoice_date,
            client_name=client_name,
            supplier_name=supplier_name,
            total_amount=total_amount
        )
        # Extract and create InvoiceItem objects
        for item_data in invoice_data['InvoiceItems']:
            item_label = item_data['ItemLibelle']
            item_unit = item_data['ItemUnit']
            quantity = item_data['ItemQuantity']
            price = item_data['ItemPrice']
            tax = item_data['ItemTax']
            total_item_amount = (price + tax) * quantity
            InvoiceItem.objects.create(
                invoice=invoice,
                item_label=item_label,
                item_unit=item_unit,
                quantity=quantity,
                price=price,
                tax=tax,
                total_item_amount=total_item_amount
            )
    return render(request, 'invoices.html', {'invoices': Invoice.objects.all()})


# Define the 404 page
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
