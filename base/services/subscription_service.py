# nagoyameshi/base/services/subscription_service.py

from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from base.models.member_models import Member
from base.models.subscription_models import Subscription
from base.utils.pk_dt_generator import create_dt_pk


def get_latest_subscription(member_id: str):
    """
    会員の最新サブスクレコードを取得
    """
    return (
        Subscription.objects.filter(member_id=member_id).order_by("-start_date").first()
    )


def get_subscription_history(member_id: str):
    """
    会員のサブスク履歴一覧を取得（最新順）
    """
    return Subscription.objects.filter(member_id=member_id).order_by("-start_date")


def is_subscribed(member_id: str) -> bool:
    """
    会員が有料会員かどうか判定
    """
    subscription = get_latest_subscription(member_id)
    if not subscription:
        return False
    return subscription.active and subscription.expiry_date >= timezone.now()


def can_access_premium(member_id: str) -> bool:
    """
    有料会員限定機能にアクセスできるか判定
    """
    return is_subscribed(member_id)


def create_subscription(member_id: str, plan: str, duration_days: int = 30):
    """
    新規サブスク作成（加入開始）
    """
    member = Member.objects.filter(id=member_id).first()
    if not member:
        raise ValueError(f"Member {member_id} does not exist.")

    now = timezone.now()
    expiry = now + timedelta(days=duration_days)

    subscription = Subscription.objects.create(
        id=create_dt_pk("SB"),
        member_id=member_id,
        plan=plan,
        start_date=now,
        expiry_date=expiry,
        active=True,
        cancelled=False,
    )
    return subscription


def renew_subscription(member_id: str, additional_days: int = 30):
    """
    サブスク更新（延長または期限切れ再加入）
    """
    latest = get_latest_subscription(member_id)
    now = timezone.now()

    if not latest or not latest.active:
        # 期限切れまたは未加入の場合は新規加入扱い
        plan = latest.plan if latest else "default"
        return create_subscription(member_id, plan, additional_days)

    # 有効期間中なら延長
    latest.expiry_date += timedelta(days=additional_days)
    latest.save()
    return latest


def cancel_subscription(member_id: str):
    """
    サブスク停止（解約）履歴として記録
    """
    latest = get_latest_subscription(member_id)
    if not latest or not latest.active:
        return None

    latest.active = False
    latest.cancelled = True
    latest.expiry_date = timezone.now()  # 停止日を記録
    latest.save()
    return latest
