# nagoyameshi/base/services/reservation_service.py
"""予約関連のサービス（作成・キャンセル・一覧取得）"""

from django.utils import timezone
from base.models.reservation_models import Reservation
from base.models.member_models import Member
from base.models.restaurant_models import Restaurant

"""予約関連の例外対策"""


class ReservationError(Exception):
    pass


"""予約作成・キャンセル"""


# 予約作成（有料会員のみ、重複チェックあり）
def create_reservation(member_id: str, restaurant_id: str, reservation_time):
    try:
        member = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        raise ReservationError("会員が存在しません")

    if not member.is_paid:
        raise ReservationError("有料会員のみ予約可能です")

    if Reservation.objects.filter(
        member=member, reservation_time=reservation_time
    ).exists():
        raise ReservationError("同じ時間に既に予約があります")

    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        raise ReservationError("対象の店舗が存在しません")

    reservation = Reservation.objects.create(
        member=member,
        restaurant=restaurant,
        reservation_time=reservation_time,
        status="active",
        created_at=timezone.now(),
    )
    return reservation


# 予約キャンセル
def cancel_reservation(reservation_id: str, cancel_reason: str):
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
    except Reservation.DoesNotExist:
        raise ReservationError("予約が存在しません")

    if cancel_reason not in ["user", "restaurant"]:
        raise ReservationError("キャンセル理由が不正です")

    reservation.status = "canceled"
    reservation.cancel_reason = cancel_reason
    reservation.canceled_at = timezone.now()
    reservation.save()
    return reservation


"""予約一覧取得"""


# 会員の未来予約一覧
def get_future_reservations(member_id: str):
    reservations = Reservation.objects.filter(
        member_id=member_id, reservation_time__gte=timezone.now(), status="active"
    ).order_by("reservation_time")
    return [
        {
            "reservation_id": r.id,
            "restaurant_name": r.restaurant.name,
            "reservation_time": r.reservation_time,
        }
        for r in reservations
    ]


# 会員の過去予約一覧（キャンセル以外）
def get_past_reservations(member_id: str):
    reservations = Reservation.objects.filter(
        member_id=member_id, reservation_time__lt=timezone.now(), status="active"
    ).order_by("-reservation_time")
    return [
        {
            "reservation_id": r.id,
            "restaurant_name": r.restaurant.name,
            "reservation_time": r.reservation_time,
        }
        for r in reservations
    ]


# 会員のキャンセル済み予約一覧
def get_canceled_reservations(member_id: str):
    reservations = Reservation.objects.filter(
        member_id=member_id, status="canceled"
    ).order_by("-canceled_at")
    return [
        {
            "reservation_id": r.id,
            "restaurant_name": r.restaurant.name,
            "reservation_time": r.reservation_time,
            "cancel_reason": r.cancel_reason,
            "canceled_at": r.canceled_at,
        }
        for r in reservations
    ]


def get_user_reservations():
    pass
