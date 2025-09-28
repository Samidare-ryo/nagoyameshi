from django import forms
from django.contrib import admin
from base.models.member_models import Member, MembershipType
from base.models.restaurant_models import (
    Restaurant,
    Holiday,
    SpecialHoliday,
    RestaurantImage,
)
from base.models.category_models import Category
from base.models.tag_models import Tag
from base.models.review_models import Review
from base.models.reservation_models import Reservation
from base.models.subscription_models import Subscription
from base.models.favorite_models import Favorite
from base.models.notification_models import Notification


# ===== Member 系 =====
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "membership_type",
        "is_active",
        "is_subscribed",
        "created_at",
    )

    search_fields = ("username", "email")
    list_filter = ("membership_type", "is_active", "is_subscribed", "created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "monthly_fee")
    search_fields = ("code", "name")


# ===== Restaurant 系 =====
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "zipcode",
        "address",
        "opening_time",
        "closing_time",
        "is_published",
        "created_at",
    )
    search_fields = ("name", "zipcode", "address")
    list_filter = ("category", "is_published", "created_at")
    filter_horizontal = ("tags", "regular_holiday", "special_holiday")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ("id", "day_of_week")


@admin.register(SpecialHoliday)
class SpecialHolidayAdmin(admin.ModelAdmin):
    list_display = ("id", "date")


@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "caption", "image_type", "created_at")
    list_filter = ("image_type",)
    readonly_fields = ("created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


# ===== Review 系 =====
class ReviewForm(forms.ModelForm):
    class Mate:
        model = Review
        fields = "__all__"
        widgets = {
            "rating": forms.RadioSelect(choices=[(i, "★" * i) for i in range(1, 6)])
        }


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("member", "restaurant", "rating", "created_at")
    search_fields = ("content", "member", "restaurant")
    list_filter = ("rating", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


# ===== Reservation 系 =====
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "restaurant",
        "reserved_at",
        "number_of_people",
        "is_canceled",
        "created_at",
    )
    search_fields = ("member__username", "restaurant__name", "note")
    list_filter = ("is_canceled", "reserved_at", "created_at")
    readonly_fields = ("created_at", "updated_at")


# ===== Subscription 系 =====
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "plan",
        "start_date",
        "expiry_date",
        "active",
        "cancelled",
    )
    search_fields = ("member__username", "plan")
    list_filter = ("active", "cancelled", "start_date")
    readonly_fields = ("created_at", "updated_at")


# ===== Favorite 系 =====
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("member", "restaurant", "created_at")
    search_fields = ("member__username", "restaurant__name")
    readonly_fields = ("created_at", "updated_at")


# ===== Notification 系 =====
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "notification_id",
        "member",
        "restaurant",
        "reservation",
        "title",
        "read",
        "created_at",
    )
    search_fields = ("title", "message", "member__username", "restaurant__name")
    list_filter = ("read", "created_at")
    readonly_fields = ("created_at",)
