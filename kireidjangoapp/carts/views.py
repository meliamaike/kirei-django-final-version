import json
from django.shortcuts import render, redirect
from products.models import Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.http import HttpResponseBadRequest
from my_payments.models import ProductPayment, CartPayment
from payments.models import PaymentStatus
from customers.models import Customer
from orders.models import ProductOrder, AppointmentOrder
import mercadopago


@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home:index")


@login_required(login_url="/login")
def item_clear(request, id, redirect_url):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect(redirect_url)


@login_required(login_url="/login")
def item_increment(request, id, redirect_url):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect(redirect_url)


@login_required(login_url="/login")
def item_decrement(request, id, redirect_url):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect(redirect_url)


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("carts:cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    return render(request, "carts/cart_detail.html")


@login_required(login_url="/login")
def many_items_add(request, id, quantity):
    print("cantidad: ", quantity)
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.adding_many(product=product, quantity=quantity)
    return redirect("carts:cart_detail")


@login_required(login_url="/login")
def replace_items_quantity(request, id, quantity):
    print("cantidad: ", quantity)
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.replace(product=product, quantity=quantity)
    return redirect("carts:cart_detail")


@login_required(login_url="/login")
def catalog_item_increment(request, id):
    cart = Cart(request)
    print("cart: ", cart)
    product = Product.objects.get(id=id)
    print("product: ", product)
    cart.add(product=product)
    return redirect("products:product_catalog")

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
@login_required(login_url="/login")
def cart_checkout(request):
    cart = Cart(request)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        request.session["payment_method"] = payment_method
        customer = Customer.objects.get(id=request.user.id)
        payment_method = request.session.get("payment_method")
        mercado_pago_payment_id = request.GET.get("payment_id")

        if payment_method == "mercadopago":
            # PROD_ACCESS_TOKEN needed
            sdk = mercadopago.SDK("TEST-2205723796037045-061917-a3112f05ebb5c1edb268154bb57034b4-451500124")

            # Create items in the preference
            items = []

            if isinstance(cart.cart, str):
                cart_dict = json.loads(cart.cart)
            else:
                cart_dict = cart.cart

            for item in cart_dict.values():
                print("item: ", item)
                product_id = item["product_id"]
                quantity = item["quantity"]

                product = Product.objects.get(id=product_id)

                item_data = {
                    "title": product.name,
                    "quantity": quantity,
                    "unit_price": float(product.price),
                    "currency_id": "ARS",
                }
                items.append(item_data)
            

            preference_data = {
                "items": items,
                "back_urls": {
                    "success": "http://127.0.0.1:8000/cart/success/",
                    "failure": "http://127.0.0.1:8000/cart/failure",
                    "pending": "https://127.0.0.1:8000/cart/pending",
                },
                "auto_return": "approved",
                "binary_mode": True,
            }

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]

            # Pass the item IDs to the template context
            item_ids = [item["id"] for item in preference["items"]]
            return render(
                request,
                "carts/mercado_pago.html",
                {
                    "item_ids": item_ids,
                    "item_id": preference["id"],
                },
            )

        elif payment_method == "cash":
            customer = Customer.objects.get(id=request.user.id)

            # Create a new CartPayment object
            cart_payment = CartPayment.objects.create(
                payment_method=payment_method,
                id_mercado_pago=mercado_pago_payment_id,
                status=PaymentStatus.CONFIRMED,
                currency="ARS",
                billing_first_name=customer.first_name,
                billing_last_name=customer.last_name,
                billing_email=customer.email,
                billing_phone=customer.phone_number,
            )

            if isinstance(cart.cart, str):
                cart_dict = json.loads(cart.cart)
            else:
                cart_dict = cart.cart

            # Iterate through the items in the cart
            cart_total = 0
            for item in cart_dict.values():
                product_id = item["product_id"]
                quantity = item["quantity"]

                product = Product.objects.get(id=product_id)

                # Create a new ProductPayment object
                product_payment = ProductPayment.objects.create(
                    product=product,
                    cart_payment=cart_payment,
                    quantity=quantity,
                    total=product.price * quantity
                   
                )

                # Update the stock of the product
                product.stock -= quantity
                product.save()

                # Add the ProductPayment object to cart_products field
                cart_payment.cart_products.add(product)

                cart_total += product_payment.total

            # Update the CartPayment object's total field with the sum of the totals for each ProductPayment
            cart_payment.cart_total = cart_total
            cart_payment.save()

            # Create the order object with customer information
            order = ProductOrder.objects.create(
                customer=customer,
                payment=cart_payment,
            )

            # Store the order id in the session for later reference
            request.session["order_id"] = order.id

            # Prepare the context data to pass to the template
            context = {
                "order": order,
            }

            # Render the HTML content of the email template
            html_message = render_to_string("carts/cart_detail_email.html", context)

            # Strip the HTML tags to generate the plain text version of the email
            plain_message = strip_tags(html_message)

            # Send the email
            send_mail(
                subject="Usted ha realizado una compra en Kirei",
                message=plain_message,
                from_email="hola@kirei.com", 
                recipient_list=[customer.email],  
                html_message=html_message,
                fail_silently=False,
            )

            cart.clear()

            return render(
                request,
                "orders/order_detail.html",
                {"order": order},
            )

        else:
            return messages.error(request, "Error en el método de pago. Intente más tarde.")

    return render(
        request,
        "carts/cart_checkout.html",
        {"cart": cart},
    )


@login_required(login_url="/login")
def mercado_pago_success(request):
    payment_method = request.session.get("payment_method")
    mercado_pago_payment_id = request.GET.get("payment_id")
    merchant_order_id = request.GET.get("merchant_order_id")

    cart = Cart(request)

    customer = Customer.objects.get(id=request.user.id)

    # Create a new CartPayment object
    cart_payment = CartPayment.objects.create(
        payment_method=payment_method,
        id_mercado_pago=mercado_pago_payment_id,
        status=PaymentStatus.CONFIRMED,
        currency="ARS",
        billing_first_name=customer.first_name,
        billing_last_name=customer.last_name,
        billing_email=customer.email,
        billing_phone=customer.phone_number,
    )

    if isinstance(cart.cart, str):
        cart_dict = json.loads(cart.cart)
    else:
        cart_dict = cart.cart

    cart_total = 0
    for item in cart_dict.values():
        product_id = item["product_id"]
        quantity = item["quantity"]

        product = Product.objects.get(id=product_id)

        # Create a new ProductPayment object
        product_payment = ProductPayment.objects.create(
            product=product,
            cart_payment=cart_payment,
            quantity=quantity,
            total=product.price * quantity,
        )

        # Update the stock of the product
        product.stock -= quantity
        product.save()

        # Add the ProductPayment object to cart_products field
        cart_payment.cart_products.add(product)

        cart_total += product_payment.total

    # Update the CartPayment object's total field with the sum of the totals for each ProductPayment
    cart_payment.cart_total = cart_total
    cart_payment.save()

    # Create the order object with customer information
    order = ProductOrder.objects.create(
        customer=customer,
        payment=cart_payment,
    )

    # Store the order id in the session for later reference
    request.session["order_id"] = order.id

    # Retrieve the list of products and their quantities from the cart_products field of the CartPayment instance
    ordered_products = [
        {
            "product": product_payment.product,
            "quantity": product_payment.quantity,
            "total_price": product_payment.total,
        }
        for product_payment in cart_payment.cart_products.through.objects.filter(
            cart_payment=cart_payment
        )
    ]

    context = {
        "payment_id": mercado_pago_payment_id,
        "merchant_order_id": merchant_order_id,
        "ordered_products": ordered_products,
        "cart_total": cart_total,
    }

    # Render the HTML content of the email template
    html_message = render_to_string("carts/mercado_pago_success_email.html", context)

    # Strip the HTML tags to generate the plain text version of the email
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        subject="Usted ha realizado una compra en Kirei",
        message=plain_message,
        from_email="hola@kirei.com", 
        recipient_list=[customer.email],  
        html_message=html_message,
        fail_silently=False,
    )

    cart.clear()

    return render(
        request,
        "carts/mercado_pago_success.html",
        context
    )


@login_required(login_url="/login")
def mercado_pago_failure(request):
    return render(request, "carts/mercado_pago_failure.html")


@login_required(login_url="/login")
def mercado_pago_pending(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "carts/mercado_pago_pending.html")
