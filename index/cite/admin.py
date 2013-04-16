from django.contrib import admin
from cite.models import Paper_Author, Citation_Author, Citation, Paper

admin.site.register(Paper_Author)
admin.site.register(Citation_Author)
admin.site.register(Citation)
admin.site.register(Paper)
