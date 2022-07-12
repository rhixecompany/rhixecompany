from django.contrib import admin

# Register your models here.

from .models import *

admin.site.site_header = "RhixeCompany Admin"
admin.site.site_title = "RhixeCompany Admin Area"
admin.site.index_title = "Welcome to the RhixeCompany admin area"


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(PostComment)
