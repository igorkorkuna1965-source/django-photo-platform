from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Album, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    inlines = [PhotoInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(album__user=request.user)

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):

    list_display = ("username", "email", "first_name", "last_name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

