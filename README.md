# Invoice Digitization Test Task
This repository contains the solution for the Invoice Digitization test task for COSIDER CANALISATION POLE C01 interview.

## Task Description
The task involves creating an application to digitize a journal of invoices presented on a web page. The application should retrieve invoice data from a provided web service and implement functionalities such as:

- Reading and formatting invoice data for display.
- Searching invoices by item label.
- Printing selected invoices in a specified format.

## Implementation
The solution is implemented using Python with the Django framework. Here's an overview of the key components:

- **Models:**: The `models.py` file defines Django models for storing invoice and invoice item data.
- **Views:** The `views.py` file contains the necessary view functions to achieve the required functionalities.
- **Templates:** HTML templates are provided for rendering invoice data and details.
- **External Data:** Invoice data is fetched from the provided URL using the Requests library.

## Task Details
- Duration: 72 hours
- Technologies: Python, Django, bootstrap, HTML, CSS
- External Resources:
    - Invoice URL: [Invoices API](https://elhoussam.github.io/invoicesapi/db.json)
