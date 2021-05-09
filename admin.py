from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User,Collection

# Register your models here.
User = get_user_model()
admin.site.register(User)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id','title')