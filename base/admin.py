from django.contrib import admin
from base.models.member_models import Member, MembershipType
from base.models.restaurant_models import Restaurant
from base.models.category_models import Category
from base.models.tag_models import Tag
from base.models.review_models import Review
from base.models.reservation_models import Reservation
from base.models.subscription_models import Subscription
from base.models.favorite_models import Favorite


# ===== Member 系 =====
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "membership_type", "is_active")
    search_fields = ("username", "email")
    list_filter = ("membership_type", "is_active")


@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "monthly_fee")
    search_fields = ("code", "name")


# ===== Restaurant 系 =====
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "zipcode", "address")
    search_fields = ("name", "zipcode", "address")
    list_filter = ("category",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


# ===== Review 系 =====
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("member", "restaurant", "rating", "created_at")
    search_fields = ("member__username", "restaurant__name")
    list_filter = ("rating",)


# ===== Reservation 系 =====
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("member", "restaurant", "reserved_at")
    search_fields = ("member__username", "restaurant__name")


# ===== Subscription 系 =====
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("member", "plan", "start_date", "expiry_date", "active")
    search_fields = ("member__username",)
    list_filter = ("active",)


# ===== Favorite 系 =====
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("member", "restaurant")
    search_fields = ("member__username", "restaurant__name")
