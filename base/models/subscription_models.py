# nagoyameshi/base/models/subscription_models.py

from django.db import models
from django.utils import timezone
from base.utils.pk_dt_generator import create_dt_pk

"""
会員サブスク履歴モデル
"""

PREFIX = "SB"


def subscription_pk():
    return create_dt_pk(PREFIX)


class Subscription(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=subscription_pk)

    # 会員との紐付け（過去履歴も残すため OneToMany 関係）
    member = models.ForeignKey(
        "base.Member",  # 循環importを避けるため文字列参照
        on_delete=models.CASCADE,
        related_name="subscriptions",
        null=True,
        blank=True,
    )

    # プラン情報（将来的に複数プラン対応可能）
    plan = models.CharField(max_length=50)

    # サブスク期間
    start_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField()

    # 状態管理
    active = models.BooleanField(default=True)  # 現在有効か
    cancelled = models.BooleanField(default=False)  # 解約済みか

    # 履歴管理用
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    payment_card_last4 = models.CharField(
        max_length=4, blank=True, null=True, verbose_name="カード下4桁"
    )

    class Meta:
        ordering = ["-start_date"]  # 最新の履歴を上に表示

    def __str__(self):
        status = "Active" if self.active else "Inactive"
        return f"{self.member.id} - {self.plan} ({status})"
