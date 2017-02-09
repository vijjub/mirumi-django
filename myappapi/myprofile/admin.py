from django.contrib import admin
from .models import UserProfile,Apartment, ApartmentImages, Roomie
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.


class AptImagesInline(admin.TabularInline):
    model = ApartmentImages
    can_delete = True


class AptAdmin(admin.ModelAdmin):
    inlines = [AptImagesInline]


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Apartment, AptAdmin)
admin.site.register(Roomie)




