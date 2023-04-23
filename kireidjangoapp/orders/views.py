from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import ProductOrder
from products.models import Product
from my_payments.models import ProductPayment
from django.db.models import Sum

@login_required(login_url="/login")
def order_detail(request):
    return render(request,"orders/order_detail.html")

def all_order(request):
    orders = ProductOrder.objects.filter(customer=request.user)

    return render(
        request,
        "orders/all_order.html",
        {"orders": orders},
    )

def all_order_detail(request, order_id, product_id):
    order = get_object_or_404(ProductOrder, pk=order_id)
    product = get_object_or_404(Product, pk=product_id)
    payment_method = order.payment.payment_method
    payment_status = order.payment.status
    payment_total = order.payment.cart_total
    specific_product=order.payment.productpayment_set.get(product_id=product_id)

    # get all ProductPayments with the same cart_payment_id
    product_payments = ProductPayment.objects.filter(cart_payment_id=specific_product.cart_payment_id)

    # sum the quantities of all ProductPayments
    total_quantity = product_payments.aggregate(Sum('quantity'))['quantity__sum']

    

    return render(
        request,
        "orders/all_order_detail.html",
        {"order": order, 
         "product":product,
         "payment_method":payment_method,
         "payment_status":payment_status,
         "payment_total":payment_total,
         "specific_product":specific_product,
         "total_quantity":total_quantity,
         }
    )
