import uuid

from django import views

from .models import Cart, Customer


def CreateNotAuthCart(request):
    customer = Customer.objects.get(user=request.user)
    customer_cart = customer.cart_set.filter(in_order=False).first()
    if customer_cart:
        customer_cart.delete()
    cart = Cart.objects.get(id=request.session['cart_id'])
    cart.session_key = None
    cart.owner = customer
    cart.products.update(user=cart.owner, session_key=None)
    cart.save()
    del request.session['cart_id']

class CartMixin(views.View):
    def dispatch(self, request, *args, **kwargs):
        cart = None
        if request.user.is_authenticated and not request.user.is_superuser:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
            self.cart = cart
        else:
            if not request.session.get('cart_id'):
                cart = Cart.objects.create(
                    session_key=uuid.uuid4()
                )
                request.session['cart_id'] = cart.id
                self.cart = cart
            else:
                try:
                    cart = Cart.objects.get(id=request.session['cart_id'])
                except Cart.DoesNotExist():
                    cart = Cart.objects.create(
                        session_key=uuid.uuid4()
                    )
            self.cart = cart
        return super().dispatch(request, *args, **kwargs)