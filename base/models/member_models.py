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
from .subscription_models import Subscription

PREFIX = "MB"


def member_pk():
    return create_pk(PREFIX)


katakana_validator = RegexValidator(
    r"^[ァ-ヴー\s]+$", "全角カタカナで入力してください。"
)


class Member(AbstractUser):
    id = models.CharField(
        default=member_pk, primary_key=True, max_length=36, editable=False
    )

    # 会員種別（無料/有料）
    class MembershipType(models.TextChoices):
        FREE = "free", _("無料会員")
        SUBSCRIBED = "subscribed", _("有料会員")

    membership_type = models.CharField(
        max_length=10,
        choices=MembershipType.choices,
        default=MembershipType.FREE,
        verbose_name="会員種別",
    )

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

    # 作成・更新日時
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")


def __str__(self):
    status = "退会済" if not self.is_active else "有効"
    return f"{self.username} ({self.get_membership_type_display()} / {status})"
