from django.contrib import admin
from .models import Document, Item

class ItemInline(admin.TabularInline):
    model = Item
    extra = 0

@admin.register(Document)
class DocAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'party', 'type')
    list_filter = ('type',)
    search_fields = ('number', 'party')
    inlines = [ItemInline]
