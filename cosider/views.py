from django.shortcuts import render
import requests
from .models import Invoice, InvoiceItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.template.loader import render_to_string
from django.http import HttpResponse


# Task 1: Read and display invoice data
def display_invoices(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoices.html', {'invoices': invoices})


# Task 2: Search by item label
def search_invoices(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        invoices = InvoiceItem.objects.filter(item_label__icontains=query)
        data = serialize('json', invoices)
        return JsonResponse(data, safe=False)


# Task 3: Display invoice details
def display_invoice_details(request, invoice_id):
    invoice = Invoice.objects.get(invoice_id=invoice_id)
    items = InvoiceItem.objects.filter(invoice=invoice)
    return render(request, 'invoice_details.html', {'invoice': invoice, 'items': items})


# Task 4: Print invoice
@csrf_exempt
def print_invoice(request):
    if request.method == 'POST':
        invoice_id = request.POST.get('invoice_id')
        invoice = Invoice.objects.get(invoice_id=invoice_id)
        items = InvoiceItem.objects.filter(invoice=invoice)
        data = {'invoice': invoice, 'items': items}
        html = render_to_string('print_invoice.html', data)
        return HttpResponse(html)


# Task 5: Fetch invoice data from external service
def fetch_invoices(request):
    url = 'https://elhoussam.github.io/invoicesapi/db.json'
    response = requests.get(url)
    data = response.json()
    for item in data['invoices']:
        invoice = Invoice.objects.create(
            invoice_id=item['invoice_id'],
            invoice_date=item['invoice_date'],
            client_name=item['client_name'],
            supplier_name=item['supplier_name'],
            total_amount=item['total_amount']
        )
        for item_detail in item['items']:
            InvoiceItem.objects.create(
                invoice=invoice,
                item_label=item_detail['item_label'],
                item_unit=item_detail['item_unit'],
                quantity=item_detail['quantity'],
                price=item_detail['price'],
                tax=item_detail['tax'],
                total_item_amount=item_detail['total_item_amount']
            )
    return JsonResponse({'status': 'success'})
