# nagoyameshi/base/models/member_models.py
"""
会員モデル
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from base.utils.pk_fix_generator import create_pk


import secrets

PREFIX = "MB"


def member_pk():
    return create_pk(PREFIX)


katakana_validator = RegexValidator(
    r"^[ァ-ヴー\s]+$", "全角カタカナで入力してください。"
)


# MembershipTypeモデル
class MembershipType(models.Model):
    FREE = "free"
    SUBSCRIBED = "subscribed"

    MEMBERSHIP_CHOICES = [
        (FREE, "Free"),
        (SUBSCRIBED, "Subscribed"),
    ]

    code = models.CharField(max_length=20, primary_key=True, choices=MEMBERSHIP_CHOICES)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.name


# Memberモデル
class Member(AbstractUser):
    id = models.CharField(
        default=member_pk, primary_key=True, max_length=36, editable=False
    )
    # メール認証
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=64, blank=True, null=True)
    email_verification_sent_at = models.DateTimeField(blank=True, null=True)

    # 会員種別（無料/有料）
    membership_type = models.ForeignKey(
        MembershipType,
        on_delete=models.PROTECT,
        default="free",
        to_field="code",  # code フィールドを参照
        verbose_name="会員種別",
    )

    # サブスク関連
    is_subscribed = models.BooleanField(default=False)
    subscription_expiry = models.DateTimeField(blank=True, null=True)

    # 連絡先
    phone_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="電話番号"
    )
    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="住所"
    )

    # フリガナ
    last_name_kana = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="セイ（全角カナ）",
        validators=[katakana_validator],
    )
    first_name_kana = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="メイ（全角カナ）",
        validators=[katakana_validator],
    )

    zipcode = models.CharField(max_length=10, blank=True, null=True)
    job = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    # 作成・更新日時
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    def __str__(self):
        status = "退会済" if not self.is_active else "有効"
        return f"{self.username} ({self.get_membership_type_display()} / {status})"
