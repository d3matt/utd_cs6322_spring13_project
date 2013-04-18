from django.contrib import admin
from cite.models import Paper_Author, Citation_Author, Citation, Paper, Token, PaperToken

admin.site.register(Paper_Author)
admin.site.register(Citation_Author)
admin.site.register(Citation)
admin.site.register(Paper)
admin.site.register(Token)
admin.site.register(PaperToken)
