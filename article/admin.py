from django.contrib import admin
from .models import Author, Article

admin.site.register(Article)
admin.site.register(Author)