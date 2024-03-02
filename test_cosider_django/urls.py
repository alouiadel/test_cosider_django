from django.urls import path
from django.views.generic import RedirectView
from cosider import views
handler404 = 'cosider.views.custom_404_view'

urlpatterns = [
    # Redirect the root URL to the 'invoices' page
    path('', RedirectView.as_view(url='invoices/', permanent=True)),

    # Read and display invoice data
    path('invoices/', views.fetch_invoices, name='fetch_invoices'),

    # Search by item label
    path('search/', views.search_invoices, name='search_invoices'),

    # Print invoice
    path('print/', views.print_invoice, name='print_invoice'),
]
