# nagoyameshi/base/models_review_models.py
from django.db import models
from .member_models import Member
from .restaurant_models import Restaurant
from base.utils.pk_dt_generator import create_dt_pk

PREFIX = "RW"


def review_pk():
    return create_dt_pk(PREFIX)


class Review(models.Model):
    # レビューPK
    id = models.CharField(
        default=review_pk, primary_key=True, max_length=36, editable=False
    )
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="reviews")
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.PROTECT,
        related_name="reviews",
    )

    content = models.TextField(verbose_name="レビュー内容")
    rating = models.PositiveSmallIntegerField(
        verbose_name="評価", choices=[(i, str(i)) for i in range(1, 6)]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "レビュー"
        verbose_name_plural = "レビュー"
        ordering = ["-created_at"]

    def __str__(self):
        member_name = getattr(self.member, "username", "退会ユーザー")
        restaurant_name = getattr(self.restaurant, "name", "削除済店舗")
        return f"{self.id} | {member_name} - {restaurant_name} ({self.rating}点)"
