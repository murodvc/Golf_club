from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from blog.forms import RegisterForm, EmailForm, LoginForm
from blog.models import User
from blog.view.tokens import account_activation_token



class LoginView(LoginView):
    template_name = 'blog/auth/login.html'
    form_class = LoginForm

    def form_invalid(self, form):
        if form.errors:
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                if not user.check_password(form.cleaned_data['password']):
                    messages.add_message(self.request, messages.ERROR, 'Password didn\'t match')

            except User.DoesNotExist:
                messages.add_message(request=self.request, level=messages.ERROR, message='User does not exists')

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user is not None and user.is_active:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('index')


def logout_page(request):
    logout(request)
    return redirect(reverse('login'))


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'blog/auth/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(first_name=first_name, email=email, password=password)
            user.is_active = False
            user.is_staff = True
            user.is_superuser = True
            user.save()
            current_site = get_current_site(request)
            subject = 'Verify your email'
            message = render_to_string('blog/auth/email/activation.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user)
            })
            email_message = EmailMessage(subject, message, to=[email])
            email_message.content_subtype = 'html'
            email_message.send()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('verify_email_done')

        return render(request, self.template_name, {'form': form})





class SendingEmailView(View):
    template_name = 'blog/sending-email.html'

    def get(self, request):
        form = EmailForm()
        return render(request, self.template_name, {'form': form, 'sent': False})

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            from_email = form.cleaned_data.get('from_email')
            to = form.cleaned_data.get('to')
            send_mail(subject, message, from_email, [to])
            return render(request, self.template_name, {'form': form, 'sent': True})

        return render(request, self.template_name, {'form': form, 'sent': False})




class VerifyEmailDoneView(View):
    template_name = 'blog/auth/email/verify-email-done.html'
    def get(self, request):
        return render(request, self.template_name)




class VerifyEmailConfirmView(View):
    template_name = 'blog/auth/email/verify-email-confirm.html'
    success_url = reverse_lazy('verify_email_complete')

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(self.success_url)
        else:
            messages.warning(request, 'The link is invalid.')

        return render(request, self.template_name)


class VerifyEmailCompleteView(View):
    template_name = 'blog/auth/email/verify-email-complete.html'

    def get(self, request):
        return render(request, self.template_name)
