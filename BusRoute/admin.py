from django.contrib import admin
from django.utils.html import format_html
from .models import BusDriver, DriverReview

@admin.register(BusDriver)
class BusDriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'years_of_service', 'cnic_number', 'contact_number', 'blood_group', 'rating', 'image_tag')
    search_fields = ('name', 'cnic_number', 'contact_number')
    list_filter = ('years_of_service', 'blood_group')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:100px;"/>', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image'


@admin.register(DriverReview)
class DriverReviewAdmin(admin.ModelAdmin):
    list_display = ('driver', 'student', 'rating', 'created_at')
    search_fields = ('driver__name', 'student__username')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at',)
