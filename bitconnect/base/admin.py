from django.contrib import admin
from .models import Member , Post ,Sessions

# Register your models here.
admin.site.register(Member)
admin.site.register(Post)
admin.site.register(Sessions)