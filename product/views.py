from django.contrib import messages
from django.shortcuts import redirect, render
from product.cart import Cart
from product.models import Coupon, Product, Image
from django.utils import timezone
from users.models import Address
from django.contrib.auth.decorators import login_required


def product_detail(request, category_slug, product_slug):
    product = Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
    images = Image.objects.filter(images=product).all()
    context = {
        'product_details': product,
        'images': images,
    }
    return render(request, 'product_detail.html', context)


def category(request, category_slug):
    categories = Product.objects.filter(category__slug=category_slug).all()
    return render(request, 'category.html', {'categories': categories})


def get_product_id(product_id):
    product_id = Product.objects.get(id=product_id)
    if not product_id.quantity >= 1:
        product_id = False
    return product_id


def cart_add(request, product_id):
    product = get_product_id(product_id)
    if not product:
        messages.error(request, 'Product out of stock')
        return redirect('home')
    Cart(request).add_to_cart(product=product)
    return redirect('home')


def cart_detail(request):
    return render(request, 'cart_detail.html')


@login_required
def checkout(request):
    user_address = Address
    address_list = user_address.objects.filter(user=request.user).all()
    if request.method != 'POST':
        return render(request, 'checkout.html', {'address_list': address_list})

    code = request.POST.get('code')

    if code:
        time_now = timezone.now()
        try:
            valid_code = Coupon.objects.get(
                code__iexact=code, valid_from__lte=time_now, valid_to__gte=time_now, active=True
            )
        except Coupon.DoesNotExist:
            messages.error(request, f'{code} Does Not Exist')
            return redirect('checkout')
        if valid_code.used == valid_code.limited:
            messages.info(request, f'{valid_code} limit reached')
            return redirect('checkout')

        request.session['coupon'] = {'code': valid_code.code, 'discount': str(valid_code.discount)}
        valid_code.used += 1
        valid_code.save()
        messages.success(request, f'{valid_code} applied successfully')

    return redirect('checkout')


def cart_clear(request):
    Cart(request).clear()
    return redirect('home')


def item_remove(request, product_id):
    Cart(request).remove(product=product_id)
    return redirect('cart-detail')


def item_decrement(request, product_id):
    Cart(request).decrement(product=product_id)
    return redirect('cart-detail')


def item_increment(request, product_id):
    product = get_product_id(product_id)
    if not product:
        messages.error(request, 'Product out of stock')
        return redirect('home')
    Cart(request).add_to_cart(product=product)
    return redirect('cart-detail')
