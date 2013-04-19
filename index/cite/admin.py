from django.contrib import admin
from cite.models import Author, Paper, Token, PaperToken

class PaperAdmin(admin.ModelAdmin):
    list_display = ('filename', 'title', 'length')
    filter_horizontal = ('authors', 'citations')

class TokenAdmin(admin.ModelAdmin):
    list_display = ('stem', 'total')

class PaperTokenAdmin(admin.ModelAdmin):
    list_display = ('num', 'paper', 'token')

admin.site.register(Author)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(PaperToken, PaperTokenAdmin)
