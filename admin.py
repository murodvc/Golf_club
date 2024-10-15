from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from blog.models import Eventss, Founder, ClubHistory, CoFounder, ImagesFounder, ImageCoFounder, Email, \
    MembershipComments, SendMessage, User

# Register your models here.

# admin.site.register(Eventss)
admin.site.register(ClubHistory)
admin.site.register(Founder)
admin.site.register(CoFounder)
admin.site.register(ImagesFounder)
admin.site.register(ImageCoFounder)
admin.site.register(Email)
admin.site.register(MembershipComments)
admin.site.register(SendMessage)
admin.site.register(User)


@admin.register(Eventss)
class Product(ImportExportModelAdmin, admin.ModelAdmin):
    List_display = ('title', 'description', 'location','ticket','imag','date_joined','slug')
