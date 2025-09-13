# nagoyameshi/base/models/reservation_models.py
from django.db import models
from .member_models import Member
from .restaurant_models import Restaurant
from base.utils.pk_dt_generator import create_dt_pk

PREFIX = "RS"


def reservation_pk():
    """予約用の主キーを生成"""
    return create_dt_pk(PREFIX)


class Reservation(models.Model):
    class CancelReason(models.TextChoices):
        USER = "user", "ユーザー都合"
        RESTAURANT = "restaurant", "店舗都合"

    # 予約PK
    id = models.CharField(
        default=reservation_pk, primary_key=True, max_length=30, editable=False
    )

    # 会員（削除されても履歴は残す）
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)

    # 店舗（削除されても履歴は残す）
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.SET_NULL, null=True, blank=True
    )

    # 予約日時
    reserved_at = models.DateTimeField()

    # 予約人数
    number_of_people = models.PositiveIntegerField()

    # 備考
    note = models.TextField(blank=True, null=True)

    # キャンセルフラグ
    is_canceled = models.BooleanField(default=False)

    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reservation"
        verbose_name = "予約"
        verbose_name_plural = "予約"

    def __str__(self):
        member_name = self.member.username if self.member else "退会済み会員"
        restaurant_name = self.restaurant.name if self.restaurant else "削除済み店舗"
        return f"{member_name} - {restaurant_name} ({self.reserved_at})"
