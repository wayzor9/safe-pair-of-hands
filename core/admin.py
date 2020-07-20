from django.contrib import admin
from .models import Donation, Institution, Category, CustomUser

admin.site.register(Donation)
admin.site.register(Category)


@admin.register(Institution)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
    list_filter = ('type',)
    search_fields = ('name', 'decsription')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_staff', 'email', 'first_name', 'last_name')
    search_fields = ('email',)
    ordering = ('is_staff', 'id')