# nagoyameshi/base/models/subscription_models.py

from django.db import models
from django.utils import timezone
# from base.models.member_models import Member

"""
会員サブスク履歴モデル
"""


class Subscription(models.Model):
    id = models.CharField(
        max_length=50, primary_key=True
    )  # 後で create_dt_pk("SB") を利用

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
