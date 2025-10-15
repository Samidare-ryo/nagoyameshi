# nagoyameshi/base/models/favorite_models.py

from django.db import models
from .member_models import Member
from .restaurant_models import Restaurant
from base.utils.pk_dt_generator import create_dt_pk
from django.utils import timezone

PREFIX = "FV"


def favorite_pk():
    """お気に入り用の主キーを生成"""
    return create_dt_pk(PREFIX)


class Favorite(models.Model):
    """
    会員のお気に入り店舗モデル
    """

    # お気に入りPK
    id = models.CharField(
        default=favorite_pk, primary_key=True, max_length=30, editable=False
    )

    # 外部キー
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="favorites"
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="favorite_by"
    )

    # 作成・更新日時
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "favorite"
        unique_together = ("member", "restaurant")  # 同じ店舗を重複登録不可にするため

    def __str__(self):
        return f"{self.member.username} - {self.restaurant.name}"
