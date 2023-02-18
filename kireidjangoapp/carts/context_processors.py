def cart_total_quantity(request):
    total_quantity = 0
    cart = request.session.get("cart", {})
    for item in cart.values():
        total_quantity += item["quantity"]
    return {"cart_total_quantity": total_quantity}
