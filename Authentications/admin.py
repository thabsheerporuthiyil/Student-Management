from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, Course


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role", "is_active")

    #edit page
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        ("Role", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_active", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    #add page
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "password1", "password2"),
        }),
    )

    search_fields = ("username", "email")
    ordering = ("username",)


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "roll_number", "year_of_admission")
    search_fields = ("user__username", "roll_number")
    list_filter = ("year_of_admission",)


admin.site.register(User, UserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Course)