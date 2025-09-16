# nagoyameshi/base/models/restaurant_models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from base.utils.pk_fix_generator import create_pk
from .category_models import Category
from .tag_models import Tag


PREFIX = "RS"


def restaurant_pk():
    return create_pk(PREFIX)


def upload_image_to(instance, filename):
    restaurant_id = instance.id
    return os.path.join("static", "restaurant", restaurant_id, filename)


class Holiday(models.Model):
    id = models.IntegerField(primary_key=True)
    day_of_week = models.CharField(max_length=10)


class SpecialHoliday(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField(blank=False, null=False)


class Restaurant(models.Model):
    # 店舗PK
    id = models.CharField(
        default=restaurant_pk, primary_key=True, max_length=36, editable=False
    )
    # 店舗名
    name = models.CharField(default="", max_length=50)
    # 店舗詳細
    description = models.TextField(default="", blank=True)
    # 電話番号
    phone_number = models.CharField(max_length=15, blank=True, default="")
    # 店舗メール
    email = models.EmailField(max_length=100, blank=True, default="")
    # 平均予算（円）
    budget = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="1人あたりの平均予算（円）",
    )
    # 定休日（例: "月曜日"）
    regular_holiday = models.ManyToManyField(Holiday, default=0)  # 複数曜日入力
    # 特別休日（例: "2025-01-01, 2025-02-11"）
    special_holiday = models.ManyToManyField(SpecialHoliday, blank=True)
    # 編集中の扱い（確定するまで掲載しない）
    is_published = models.BooleanField(default=False)
    # 登録日と更新日
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # カテゴリ（1店舗 = 1カテゴリ）
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="restaurants",
    )

    # タグ（1店舗 = 複数タグ）
    tags = models.ManyToManyField(Tag, blank=True, related_name="restaurants")

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    id = models.AutoField(primary_key=True)

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="images"
    )

    image = models.ImageField(
        upload_to=upload_image_to,
        blank=True,
        null=True,
    )

    caption = models.CharField(max_length=100, blank=True, default="")

    IMAGE_TYPE_CHOICES = [
        ("exterior", "外観"),
        ("interior", "内装"),
        ("food", "料理"),
    ]

    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name} - Image {self.id} ({self.get_image_type_display()})"
