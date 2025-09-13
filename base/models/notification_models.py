# nagoyameshi/base/models/notification_models.py
from django.db import models
from django.utils import timezone
from .member_models import Member
from .restaurant_models import Restaurant
from .reservation_models import Reservation
from base.utils.pk_dt_generator import create_dt_pk

PREFIX = "NC"


def notification_pk():
    """通知用の主キーを生成"""
    return create_dt_pk(PREFIX)


class Notification(models.Model):
    notification_id = models.CharField(
        primary_key=True, default=notification_pk, max_length=20
    )

    # 通知対象
    member = models.ForeignKey(Member, null=True, blank=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, null=True, blank=True, on_delete=models.CASCADE
    )

    # 予約との紐付け
    reservation = models.ForeignKey(
        Reservation, null=True, blank=True, on_delete=models.CASCADE
    )

    # 通知内容
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
