from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import TemplateView, ListView, FormView, DetailView
from openpyxl.workbook import Workbook

from blog.forms import SubscriberForm, MembershipForm, SendMessag
from blog.models import Eventss, ClubHistory, MembershipComments
from config.settings import EMAIL_HOST_USER
import json
import csv

# Create your views here.

class IndexView(TemplateView):
    template_name = 'blog/home.html'


class EventList(ListView):
    model = Eventss
    template_name = 'blog/event/event-listing.html'
    context_object_name = 'events'
    paginate_by = 2



class EventDetailView(DetailView):
    model = Eventss
    template_name = 'blog/event/event-detail.html'
    context_object_name = 'event'





# About
class AboutView(ListView,FormView):
    model = ClubHistory
    template_name = 'blog/about.html'
    form_class = SubscriberForm
    success_url = reverse_lazy('thank-you')
    paginate_by = 1
    context_object_name = 'events'


    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
class ThankYou(TemplateView):
    template_name = 'blog/email.html'



# memberships
class MembershipView(FormView):
    template_name = 'blog/membership.html'
    form_class = MembershipForm
    success_url = reverse_lazy('success')

    def get_queryset(self):
        return Eventss.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.get_queryset()
        paginator = Paginator(club, 4)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


    def form_valid(self, form):
        form.save()
        subject = 'Membership Confirmation'
        message = 'Thank you for joining! We will comment soon.'
        recipient = form.cleaned_data['email']
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [recipient],
            fail_silently=False,
        )
        return super().form_valid(form)

    def comments(self):
        comment = MembershipComments.objects.all()
        comments = comment.comments.filter(is_active=True).order_by('-created_at')
        count = comment.comments.count()
        context = {
            'comment': comment,
            'comments': comments,
            'count': count,
        }
        return render(self.request, 'blog/membership.html', context)

class Success(TemplateView):
    template_name = 'blog/success.html'


from django.shortcuts import render, redirect

class EventView(ListView):
    model = Eventss
    template_name = 'blog/events.html'
    context_object_name = 'events'
    paginate_by = 2




class ExportDataView(View):
    def get(self, request):
        format = request.GET.get('format', 'csv')

        if format == 'csv':
            response = self.export_csv()
        elif format == 'json':
            response = self.export_json()
        elif format == 'xlsx':
            response = self.export_xlsx()
        else:
            response = HttpResponse(status=404)
            response.content = 'Bad requests'
        return response

    def export_csv(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customers.csv"'
        writer = csv.writer(response)
        writer.writerow(['id', 'title', 'description','location','ticket','imag'])
        events = Eventss.objects.all()
        for event in events:
            writer.writerow([event.id, event.title, event.description, event.location, event.ticket, event.imag])
        return response

    def export_json(self):
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="events.json"'
        data = list(Eventss.objects.values('id', 'title', 'description','location','ticket','imag'))
        response.content = json.dumps(data, indent=4)
        return response

    def export_xlsx(self):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="events.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = "Eventss"
        headers = ['id', 'title', 'description','location','ticket']
        ws.append(headers)

        events = Eventss.objects.all()
        for event in events:
            ws.append([event.id, event.title, event.description, event.location, event.ticket])
        wb.save(response)
        return response

class ContactUpView(FormView):
    template_name = 'blog/contact_up.html'
    form_class = SendMessag
    success_url = reverse_lazy('message')

    def form_valid(self, form):
        form.save()
        subject = 'Contact Up'
        message = 'We will review your message and contact you🚀'
        recipient = form.cleaned_data['email']
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [recipient],
            fail_silently=False,
        )
        return super().form_valid(form)

class Message(TemplateView):
    template_name = 'blog/message.html'

















