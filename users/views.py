from django.core.mail import EmailMessage
from email.utils import make_msgid
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from redirect_to_next import redirect_to_next
from stripe_payment.models import Order, Invoice
from .models import Address
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib import messages
from general import random_num
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

user = get_user_model()


@login_required
def new_address(request):
    if request.method != 'POST':
        return render(request, 'new_address.html')
    user_address = Address
    post_dict = {
        'user': request.user,
        'full_name': request.POST.get('full_name'),
        'email': request.POST.get('email'),
        'address1': request.POST.get('address1'),
        'address2': request.POST.get('address2'),
        'country': request.POST.get('country'),
        'city': request.POST.get('city'),
        'zipcode': request.POST.get('zipcode'),
        'phone': request.POST.get('phone'),
    }
    user_address.objects.create(**post_dict)
    redirect_to_next(request)
    return redirect('user-address')


@login_required
def set_default(request, address_id):
    address = Address
    address.objects.all().update(default=False)
    address.objects.filter(id=address_id).update(default=True)
    # referer = redirect_to_next(request)
    # if referer:
    #     return redirect(referer)
    return redirect(redirect_to_next(request))


@login_required
def del_address(request, address_id):
    Address.objects.filter(id=address_id).delete()
    # redirect_to_next(request)
    return redirect(redirect_to_next(request))


@login_required
def edit_address(request, address_id):
    user_address = Address.objects.filter(id=address_id).first()
    if request.method != 'POST':
        return render(request, 'new_address.html', {'user_address': user_address, 'address_id': address_id})

    post_dict = {
        'full_name': request.POST.get('full_name'),
        'email': request.POST.get('email'),
        'address1': request.POST.get('address1'),
        'address2': request.POST.get('address2'),
        'country': request.POST.get('country'),
        'city': request.POST.get('city'),
        'zipcode': request.POST.get('zipcode'),
        'phone': request.POST.get('phone'),
    }

    Address.objects.filter(id=address_id).update(**post_dict)
    # redirect_to_next(request)
    return redirect(redirect_to_next(request))


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).all()
    return render(request, 'orders.html', {'orders': orders})


@login_required
def invoices(request):
    invoices = Invoice.objects.filter(user=request.user).all()
    return render(request, 'invoices.html', {'invoices': invoices})


@login_required
def account(request):
    return render(request, 'account.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


@login_required
def user_address(request):
    address_list = Address.objects.filter(user=request.user).all()
    return render(request, 'user_address.html', {'address_list': address_list})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('account')
    if request.method != 'POST':
        return render(request, 'sign_in.html')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if not email:
        messages.error(request, 'Please enter an email address')
        return redirect('sign-in')
    if not password:
        messages.error(request, 'Please enter password')
        return redirect('sign-in')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        if not user.email_verified and not user.is_superuser:
            messages.error(request, 'Email is not verified')
            return redirect('verify-email', user_id=user.pk)
        login(request, user)
        request.session['user_id'] = user.pk
        return redirect(redirect_to_next(request))
    messages.error(request, 'Invalid email or password')
    return redirect('sign-in')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('account')
    if request.method != 'POST':
        return render(request, 'signup.html')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')

    if not email:
        messages.error(request, 'Please enter an email address')
        return redirect('sign-up')
    if not password:
        messages.error(request, 'Please enter password')
        return redirect('sign-up')
    if password != password2:
        messages.error(request, 'Password does not match')
        return redirect('sign-up')

    check_user = user.objects.filter(email=email).first()
    if check_user:
        messages.error(request, 'Email address already in use')
        return redirect('sign-up')
    verify_code = random_num(6)
    new_user = user.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=make_password(password),
        verify_code=verify_code,
    )

    from_email = 'admin@example.com'
    MESSAGE_ID = make_msgid(domain=from_email.split("@")[1])
    subject = f'Your verification code {new_user.pk}'
    html_content = f"Please enter your verification code \n {verify_code} \n in http://127.0.0.1:8000/verify-email/{new_user.pk}/"
    email_msg = EmailMessage(
        subject,
        html_content,
        from_email,
        [email],
        headers={"Message-ID": MESSAGE_ID},
    )
    email_msg.content_subtype = "html"
    email_msg.send()
    return redirect('verify-email', user_id=new_user.pk)


def verify_email(request, user_id):
    check_user = user.objects.filter(id=user_id).first()
    if request.method != 'POST':
        return render(request, 'verify_email.html')
    verify_code = request.POST.get('verify-code')
    if not verify_code:
        messages.error(request, 'Please enter the verify code')
        return redirect(request.path)
    if check_user.verify_code != verify_code:
        messages.error(request, 'Wrong verify code')
        return redirect(request.path)
    check_user.email_verified = True
    check_user.is_active = True
    check_user.save()
    messages.success(request, 'Your email has been verified')
    return redirect('sign-in')
