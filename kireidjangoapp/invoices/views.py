from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request
from fpdf import FPDF
from orders.models import ProductOrder
from my_payments.models import ProductPayment
from products.models import Product
from django.db.models import Sum


def generate_invoice(request, order_id, product_id):
    order = get_object_or_404(ProductOrder, pk=order_id)
    product = get_object_or_404(Product, pk=product_id)
    specific_product = order.payment.productpayment_set.get(product_id=product_id)

    # get all ProductPayments with the same cart_payment_id
    product_payments = ProductPayment.objects.filter(
        cart_payment_id=specific_product.cart_payment_id
    )

    # Define the invoice information
    customer_first_name = order.customer.first_name
    customer_last_name = order.customer.last_name
    customer_document_number = order.customer.document_number
    customer_area_code = order.customer.area_code
    customer_phone_number = order.customer.phone_number
    # customer_address = order.customer.address
    # customer_city = order.customer_city
    # customer_province = order.customer_province
    customer_country = "Argentina"
    # customer_zipcode = order.customer_zipcode

    date_string = order.created_at.strftime("%Y-%m-%d")

    # Create a PDF object
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font and add logo
    pdf.set_font("Arial", "B", 21)

    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "logo.png")

    pdf.image(image_path, x=5, y=6, w=50)

    # Add title and blank lines
    pdf.cell(0, 10, "FACTURA", 0, 0, "C")
    pdf.cell(0, 10, "", 0, 1)

    # Add company info

    pdf.set_font("Arial", "", 12)

    # Draw rectangle border around the cells
    pdf.rect(10, 30, 190, 30)

    # Position cells inside the rectangle
    pdf.set_xy(10, 30)
    pdf.cell(70, 10, "Razón Social: Kirei S.A", 0, 1)

    pdf.set_xy(10, 40)
    pdf.cell(70, 10, "Domicilio Comercial: THAMES 1906", 0, 1)

    pdf.set_xy(10, 50)
    pdf.cell(70, 10, "Condición Frente al IVA: Resp. Insc.", 0, 1)

    pdf.cell(0, 10, "", 0, 1)
    # Add invoice info
    pdf.set_font("Arial", "B", 12)

    pdf.cell(70, 10, "Factura", 0, 1, "L")

    pdf.set_font("Arial", "", 12)
    pdf.cell(70, 10, f"Comp. Nro: 00001970", 0, 0)
    pdf.cell(70, 10, f"Fecha de Emisión: {date_string}", 0, 1, "R", 20)
    pdf.cell(70, 10, "CUIT: 33717465909", 0, 0)
    pdf.cell(70, 10, f"Factura Nro: {order.id}", 0, 1, "R", 20)

    # Add a line break
    pdf.cell(0, 10, "", 0, 1)

    # Add customer info
    pdf.set_font("Arial", "B", 12)
    pdf.cell(70, 10, "Información del Cliente", 0, 0)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "", 0, 1)
    pdf.cell(70, 10, f"DNI/CUIT: {customer_document_number}", 0, 0)
    pdf.cell(
        0,
        10,
        f"Nombre y Apellido / Razón Social: {customer_first_name} {customer_last_name}",
        0,
        1,
    )
    pdf.cell(0, 10, f"País: {customer_country}", 0, 1)
    pdf.cell(70, 10, f"Código de Área: {customer_area_code}", 0, 0)
    pdf.cell(70, 10, f"Número de Teléfono: {customer_phone_number}", 0, 1)

    # Add a line break
    pdf.cell(0, 10, "", 0, 1)

    # Create the table header for product
    pdf.set_font("Arial", "B", 12)
    pdf.cell(70, 10, "Producto/Servicio", border=1, align="L")
    pdf.cell(40, 10, "Cantidad", border=1, align="R")
    pdf.cell(40, 10, "Precio Unit.", border=1, align="R")
    pdf.cell(40, 10, "Subtotal", border=1, align="R")
    pdf.cell(0, 10, "", 0, 1)

    # Set the font and size for the product information

    pdf.set_font("Arial", "", 12)

    # Add the product information

    for product in product_payments:
        pdf.cell(70, 10, product.product.name, align="L")
        pdf.cell(40, 10, str(product.quantity), align="R")
        pdf.cell(40, 10, f"${product.product.price}", align="R")
        pdf.cell(40, 10, f"${product.product.price * product.quantity}", align="R")
        pdf.cell(0, 10, "", 0, 1)

    # Add a line break

    pdf.cell(0, 10, "", 0, 1)
    # Calculate the total amount and add it to the PDF

    total = sum(
        [product.product.price * product.quantity for product in product_payments]
    )

    pdf.set_font("Arial", "B", 15)
    pdf.cell(0, 10, f"Total: ${total}", border=0, ln=1, align="R")

    # Save the PDF file

    # pdf.output("invoice.pdf")

    from io import BytesIO
    import os
    from django.http import FileResponse

    # Save the PDF to a file

    filename = "invoice.pdf"
    file_path = os.path.join(os.path.dirname(__file__), filename)

    with open(file_path, "wb") as f:
        f.write(pdf.output(dest="S").encode("latin1"))

    # Return a response with the file
    response = FileResponse(open(file_path, "rb"), content_type="application/pdf")
    return response
