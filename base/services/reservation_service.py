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
def create_reservation(member_id: str, restaurant_id: str, reserved_at):
    try:
        member = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        raise ReservationError("会員が存在しません")

    if not member.is_paid:
        raise ReservationError("有料会員のみ予約可能です")

    if Reservation.objects.filter(member=member, reserved_at=reserved_at).exists():
        raise ReservationError("同じ時間に既に予約があります")

    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        raise ReservationError("対象の店舗が存在しません")

    reservation = Reservation.objects.create(
        member=member,
        restaurant=restaurant,
        reserved_at=reserved_at,
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

    reservation.is_canceled = True
    reservation.cancel_reason = cancel_reason
    reservation.canceled_at = timezone.now()
    reservation.save()
    return reservation


"""予約一覧取得"""


# 会員の未来予約一覧
def get_future_reservations(member_id: str):
    reservations = Reservation.objects.filter(
        member_id=member_id, reserved_at__gte=timezone.now(), status="active"
    ).order_by("reserved_at")
    return [
        {
            "reservation_id": r.id,
            "restaurant_name": r.restaurant.name,
            "reserved_at": r.reserved_at,
        }
        for r in reservations
    ]


# 会員の過去予約一覧（キャンセル以外）
def get_past_reservations(member_id: str):
    reservations = Reservation.objects.filter(
        member_id=member_id, reserved_at__lt=timezone.now(), status="active"
    ).order_by("-reserved_at")
    return [
        {
            "reservation_id": r.id,
            "restaurant_name": r.restaurant.name,
            "reserved_at": r.reserved_at,
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
            "reserved_at": r.reserved_at,
            "cancel_reason": r.cancel_reason,
            "canceled_at": r.canceled_at,
        }
        for r in reservations
    ]


def get_member_reservations(member_id: str):
    """
    会員の予約一覧を取得
    未来予約・過去予約・キャンセル済み予約をまとめて返す
    """
    from django.utils import timezone

    # 未来予約（キャンセルされていない予約）
    future_reservations = Reservation.objects.filter(
        member_id=member_id, reserved_at__gte=timezone.now(), is_canceled=False
    ).order_by("reserved_at")

    # 過去予約（キャンセルされていない予約）
    past_reservations = Reservation.objects.filter(
        member_id=member_id, reserved_at__lt=timezone.now(), is_canceled=False
    ).order_by("-reserved_at")

    # キャンセル済み予約
    canceled_reservations = Reservation.objects.filter(
        member_id=member_id, is_canceled=True
    ).order_by("-updated_at")

    # 辞書形式で返す
    return {
        "future_reservations": [
            {
                "reservation_id": r.id,
                "restaurant_name": r.restaurant.name
                if r.restaurant
                else "削除済み店舗",
                "reserved_at": r.reserved_at,
                "number_of_people": r.number_of_people,
                "note": r.note,
            }
            for r in future_reservations
        ],
        "past_reservations": [
            {
                "reservation_id": r.id,
                "restaurant_name": r.restaurant.name
                if r.restaurant
                else "削除済み店舗",
                "reserved_at": r.reserved_at,
                "number_of_people": r.number_of_people,
                "note": r.note,
            }
            for r in past_reservations
        ],
        "canceled_reservations": [
            {
                "reservation_id": r.id,
                "restaurant_name": r.restaurant.name
                if r.restaurant
                else "削除済み店舗",
                "reserved_at": r.reserved_at,
                "number_of_people": r.number_of_people,
                "note": r.note,
                "cancel_reason": r.cancel_reason,
                "canceled_at": r.updated_at,
            }
            for r in canceled_reservations
        ],
    }
