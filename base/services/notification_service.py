# nagoyameshi/base/ervices/notification_service.py
from django.utils import timezone
from base.models.member_models import Member
from base.models.restaurant_models import Restaurant
from base.models.reservation_models import Reservation
from base.models.notification_models import Notification


# ------------------------------
# 汎用通知作成（予約ID紐付け対応）
# ------------------------------
def create_notification(
    member=None, restaurant=None, reservation_id=None, title="", message=""
):
    if not member and not restaurant:
        return None  # 作成しない

    reservation = None
    if reservation_id:
        try:
            reservation = Reservation.objects.get(reservation_id=reservation_id)
        except Reservation.DoesNotExist:
            reservation = None

    notification = Notification.objects.create(
        member=member,
        restaurant=restaurant,
        reservation=reservation,
        title=title,
        message=message,
        created_at=timezone.now(),
        read=False,
    )
    return notification.notification_id  # 作成された通知IDを返す


# ------------------------------
# 予約通知
# ------------------------------
def notify_reservation_created(member_id, restaurant_id, reservation_id):
    member = Member.objects.get(member_id=member_id)
    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)

    # 会員通知
    create_notification(
        member=member,
        reservation_id=reservation_id,
        title="予約作成通知",
        message="予約を作成しました。詳細をご確認ください。",
    )

    # 店舗通知
    create_notification(
        restaurant=restaurant,
        reservation_id=reservation_id,
        title="新規予約通知",
        message="新しい予約が作成されました。",
    )


def notify_reservation_response(
    member_id, restaurant_id, reservation_id, approved=True
):
    member = Member.objects.get(member_id=member_id)
    if approved:
        title = "予約承認通知"
        message = "予約が受理されました。ご来店をお待ちしています。"
    else:
        title = "予約不受理通知"
        message = "予約が承認されませんでした。別の日時でご予約ください。"
    create_notification(
        member=member, reservation_id=reservation_id, title=title, message=message
    )


def notify_reservation_canceled(
    member_id=None, restaurant_id=None, reservation_id=None, canceled_by="member"
):
    member = Member.objects.get(member_id=member_id) if member_id else None
    restaurant = (
        Restaurant.objects.get(restaurant_id=restaurant_id) if restaurant_id else None
    )

    if canceled_by == "member":
        title = "予約キャンセル通知"
        message = "予約がキャンセルされました（会員都合）。"
        create_notification(
            member=None,
            restaurant=restaurant,
            reservation_id=reservation_id,
            title=title,
            message=message,
        )
    else:
        title = "予約キャンセル通知"
        message = "予約がキャンセルされました（店舗都合）。"
        create_notification(
            member=member,
            restaurant=None,
            reservation_id=reservation_id,
            title=title,
            message=message,
        )


# ------------------------------
# 予約変更通知
# ------------------------------
def notify_reservation_change_request_by_member(
    member_id, restaurant_id, reservation_id
):
    member = Member.objects.get(member_id=member_id)
    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    create_notification(
        restaurant=restaurant,
        reservation_id=reservation_id,
        title="予約変更依頼",
        message=f"{member.name} さんから予約変更の依頼が届きました。",
    )


def notify_reservation_change_response_by_store(
    member_id, restaurant_id, reservation_id, approved=True
):
    member = Member.objects.get(member_id=member_id)
    if approved:
        title = "予約変更完了"
        message = "予約変更が完了しました。"
    else:
        title = "予約変更不受理"
        message = "予約変更は承認されませんでした。"
    create_notification(
        member=member, reservation_id=reservation_id, title=title, message=message
    )


def notify_reservation_change_request_by_store(
    member_id, restaurant_id, reservation_id
):
    member = Member.objects.get(member_id=member_id)
    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    create_notification(
        member=member,
        reservation_id=reservation_id,
        title="予約変更依頼",
        message=f"{restaurant.name} から予約変更の依頼が届きました。",
    )


def notify_reservation_change_response_by_member(
    member_id, restaurant_id, reservation_id, approved=True
):
    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    if approved:
        title = "予約変更完了"
        message = "予約変更が完了しました。"
    else:
        title = "予約変更不受理"
        message = "予約変更は承認されませんでした。"
    create_notification(
        restaurant=restaurant,
        reservation_id=reservation_id,
        title=title,
        message=message,
    )


# ------------------------------
# 予約イベント通知ハンドラ
# ------------------------------
def handle_reservation_event(
    event_type: str,
    actor: str,
    member_id: str,
    restaurant_id: str,
    reservation_id: str,
    approved: bool = True,
):
    """
    予約イベントに応じて通知を自動作成
    event_type: create, approve, reject, change_request, change_response, cancel
    actor: "member" or "store"
    """
    if event_type == "create":
        notify_reservation_created(member_id, restaurant_id, reservation_id)
    elif event_type == "approve":
        notify_reservation_response(
            member_id, restaurant_id, reservation_id, approved=True
        )
    elif event_type == "reject":
        notify_reservation_response(
            member_id, restaurant_id, reservation_id, approved=False
        )
    elif event_type == "change_request":
        if actor == "member":
            notify_reservation_change_request_by_member(
                member_id, restaurant_id, reservation_id
            )
        else:
            notify_reservation_change_request_by_store(
                member_id, restaurant_id, reservation_id
            )
    elif event_type == "change_response":
        if actor == "member":
            notify_reservation_change_response_by_member(
                member_id, restaurant_id, reservation_id, approved
            )
        else:
            notify_reservation_change_response_by_store(
                member_id, restaurant_id, reservation_id, approved
            )
    elif event_type == "cancel":
        canceled_by = "member" if actor == "member" else "store"
        notify_reservation_canceled(
            member_id=member_id,
            restaurant_id=restaurant_id,
            reservation_id=reservation_id,
            canceled_by=canceled_by,
        )
