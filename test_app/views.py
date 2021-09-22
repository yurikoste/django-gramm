from django.http import HttpResponse
from django.shortcuts import render, redirect
from . forms import NewUserForm, LoginForm, UserUpdateForm, DGUserPostForm, DGPictureForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from . models import DjangoGrammUser, DjangoGrammPost, Picture
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, force_str
from . gen_token import generate_token
from django.urls import reverse
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.auth.decorators import login_required
from services.counters import get_num_of_likes, get_num_of_followers
from services.checkers import check_is_post_liked_by_logg_user, is_user_subscribed


def index(request):
    return render(request, "index.html")


def register_request(request):
    context = {}

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            if not DjangoGrammUser.objects.filter(email=form.cleaned_data.get('email')).exists():
                return redirect("test_app:login_page")
            raw_password = form.cleaned_data.get('password1')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration successful.")
            user = DjangoGrammUser.objects.get(email=email)
            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,
                                 'We sent you an email to verify your account')
            return redirect("test_app:login")
        else:
            context['registration_form'] = form
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm(request.POST)
        context['registration_form'] = form
    return render(request, "register.html", context)


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    message = Mail(
        from_email=settings.EMAIL_FROM_USER,
        to_emails=[user.email],
        subject=email_subject,
        html_content=email_body
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return 'Successful sending'
    except Exception as e:
        return 'ERROR'


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = DjangoGrammUser.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect('test_app:login')

    return render(request, 'activation_failed.html', {"user": user})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user and not user.is_email_verified:
                list(messages.get_messages(request))
                messages.add_message(request, messages.ERROR,
                                     'Email is not verified, please check your email inbox')
                return render(request, 'login.html', {'form': form})
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('test_app:show_feed')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        return redirect('test_app:login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required()
def user_logout(request):
    logout(request)
    return redirect('test_app:index')


@login_required
def display_user_page(request, user_id):
    email = None
    if request.user.is_authenticated:
        user = DjangoGrammUser.objects.get(pk=user_id)
        imgs = Picture.objects.all()
        user_posts = DjangoGrammPost.objects.filter(owner_id=user_id)
        is_subscribed = is_user_subscribed(request, user_id)
        post_likes = [(post, get_num_of_likes(post.id), check_is_post_liked_by_logg_user(request.user, post)) for post in user_posts]

        return render(request, "user_page.html", {
            "user": user,
            'user_posts': user_posts,
            'user_id': user_id,
            'auth_user_id': request.user.pk,
            'auth_user': request.user,
            'imgs': imgs,
            'is_subscribed': is_subscribed,
            'post_likes': post_likes,
            'subscribers_count': get_num_of_followers(user_id)

        })
    else:
        return HttpResponse("User isn't logged in")


@login_required
def edit_user_page(request):
    if request.user.is_authenticated:
        if "cancel_edit_user_page" in request.POST:
            return redirect('test_app:user_page', user_id=request.user.id)
        email = request.user.email
        user = DjangoGrammUser.objects.get(id=request.user.id)
        form = UserUpdateForm(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            form.save()
            return display_user_page(request, user.id)
        return render(request, 'edit_user_page.html', {"user": user, 'form': form})


@login_required
def add_user_post(request):
    if request.user.is_authenticated:
        email = request.user.email
        user = DjangoGrammUser.objects.get(id=request.user.id)
        post_form = DGUserPostForm(request.POST or None, request.FILES or None)
        img_form = DGPictureForm(request.POST or None, request.FILES or None)
        if "cancel_add_user_post" in request.POST:
            return redirect('test_app:user_page', user_id=user.id)
        if post_form.is_valid() and img_form.is_valid():
            post = post_form.save(commit=False)
            img = img_form.save(commit=False)
            post.owner_id = user
            post.save()
            post_for_img = DjangoGrammPost.objects.get(id=post.id)
            img.post_id = post_for_img
            img.save()
            return redirect('test_app:user_page', user_id=request.user.id)
        return render(request, 'add_user_post.html',
                      {'form': post_form, 'form_img': img_form}
                      )


@login_required
def show_post(request, user_post_id):
    post = DjangoGrammPost.objects.get(id=user_post_id)
    imgs = Picture.objects.filter(post_id=user_post_id)
    user = DjangoGrammUser.objects.get(username=post.owner_id)
    return render(request, 'post.html', {
        "post": post, 'imgs': imgs, 'user_post_id': user_post_id, 'user': user, 'auth_user_id': request.user.pk
    }
                  )


@login_required
def edit_post(request, user_post_id):
    if request.user.is_authenticated:
        post = DjangoGrammPost.objects.get(id=user_post_id)
        imgs = Picture.objects.filter(post_id=user_post_id)
        post_form = DGUserPostForm(request.POST or None, request.FILES or None, instance=post)
        img_form = DGPictureForm(request.POST or None, request.FILES or None, instance=post)
        if "cancel" in request.POST:
            return redirect(reverse('test_app:user_page'))
        if post_form.is_valid():
            post = post_form.save()
        if img_form.is_valid():
            img = img_form.save()
            return redirect('test_app:user_page', user_id=request.user.id)
        return render(request, 'edit_post.html',
                      {'form': post_form, 'form_img': img_form}
                      )


@login_required
def show_feed(request):
    posts = DjangoGrammPost.objects.all()
    imgs = Picture.objects.all()
    users = DjangoGrammUser.objects.all()
    post_likes = [(post, get_num_of_likes(post.id), check_is_post_liked_by_logg_user(request.user, post)) for post in posts]
    return render(
        request, 'feed.html', {
            "users": users,
            "posts": posts,
            'imgs': imgs,
            'auth_user_id': request.user.pk,
            'post_likes': post_likes
        }
    )




