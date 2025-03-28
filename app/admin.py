from django.contrib import admin
from .models import ToDoList, Item

class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')  # Show both name and user in list view
    list_filter = ('user',)  # Add ability to filter by user

admin.site.register(ToDoList, ToDoListAdmin)
admin.site.register(Item)
