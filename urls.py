from django.contrib import admin
from django.urls import path, include

from blog.view.auth import LoginView, logout_page, RegisterView, SendingEmailView, VerifyEmailDoneView, \
    VerifyEmailCompleteView, VerifyEmailConfirmView
from blog.view.views import (IndexView,
                             EventDetailView,
                             AboutView,
                             MembershipView,
                             EventView,
                             ContactUpView, ThankYou, Success, ExportDataView, EventList, Message)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('',IndexView.as_view(),name='index'),
    # event-list-detail
    path('event-list/',EventList.as_view(), name='event-list'),
    path('event-detail/<slug:slug>',EventDetailView.as_view(), name='event-detail'),

    # About
    path('about/', AboutView.as_view(), name='about'),
    path('thank-you/',ThankYou.as_view(),name='thank-you'),
    # Memberships
    path('membership/',MembershipView.as_view(), name='membership'),
    path('success/',Success.as_view(),name='success'),


    path('events/',EventView.as_view(), name='event'),
    path('events/export/', ExportDataView.as_view(), name='event_export'),


    path('contact-up/',ContactUpView.as_view(), name='contact-up'),
    path('message/',Message.as_view(),name='message'),


    path('login-page/', LoginView.as_view(), name='login'),
    path('logout-page/', logout_page, name='logout'),
    path('register-page/', RegisterView.as_view(), name='register'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    # sending email url
    path('sending-email-url/', SendingEmailView.as_view(), name='sending_email'),

    # verify email

    path('verify-email-done/', VerifyEmailDoneView.as_view(), name='verify_email_done'),
    path('verify-email/complete/', VerifyEmailCompleteView.as_view(), name='verify_email_complete'),
    path('verify-email-confirm/<uidb64>/<token>/', VerifyEmailConfirmView.as_view(), name='verify_email_confirm')
    #

]