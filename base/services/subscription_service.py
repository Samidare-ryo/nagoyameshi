# nagoyameshi/base/services/subscription_service.py

from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404
from base.models.member_models import Member
from base.models.subscription_models import Subscription
from base.utils.pk_dt_generator import create_dt_pk
import stripe

stripe.api_key = settings.STRIPE_API_SECRET_KEY


def get_latest_subscription(member_id: str):
    """会員の最新サブスクレコードを取得"""
    return (
        Subscription.objects.filter(member_id=member_id).order_by("-start_date").first()
    )


def get_subscription_history(member_id: str):
    """会員のサブスク履歴一覧を取得（最新順）"""
    return Subscription.objects.filter(member_id=member_id).order_by("-start_date")


def is_subscribed(member_id: str) -> bool:
    """会員が有料会員かどうか判定"""
    subscription = get_latest_subscription(member_id)
    if not subscription:
        return False
    return subscription.active and subscription.expiry_date >= timezone.now()


def can_access_premium(member_id: str) -> bool:
    """有料会員限定機能にアクセスできるか判定"""
    return is_subscribed(member_id)


def create_subscription(member_id: str, plan: str, duration_days: int = 30):
    """新規サブスク作成（加入開始）"""
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
    """サブスク更新（延長または期限切れ再加入）"""
    latest = get_latest_subscription(member_id)
    # now = timezone.now()

    if not latest or not latest.active:
        # 期限切れまたは未加入の場合は新規加入扱い
        plan = latest.plan if latest else "default"
        return create_subscription(member_id, plan, additional_days)

    # 有効期間中なら延長
    latest.expiry_date += timedelta(days=additional_days)
    latest.save()
    return latest


def cancel_subscription(member_id: str):
    """サブスク停止（解約）履歴として記録"""
    latest = get_latest_subscription(member_id)
    if not latest or not latest.active:
        return None

    latest.active = False
    latest.cancelled = True
    latest.expiry_date = timezone.now()  # 停止日を記録
    latest.save()
    return latest


# --- Stripe関連処理 ---
def create_stripe_checkout_session(
    member_id: str, price_id: str, success_path: str, cancel_path: str
):
    """Stripe Checkoutセッションを作成してURLを返す"""
    member = get_object_or_404(Member, id=member_id)
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url=f"{settings.YOUR_DOMAIN}{success_path}?session_id={{CHECKOUT_SESSION_ID}}&user_id={member.id}",
        cancel_url=f"{settings.YOUR_DOMAIN}{cancel_path}",
    )
    return session.url


def retrieve_stripe_session(session_id: str, member_id: str):
    """Stripeセッション情報を取得してMemberに反映"""
    member = get_object_or_404(Member, id=member_id)
    session = stripe.checkout.Session.retrieve(session_id, expand=["subscription"])
    subscription_id = session.subscription.id
    subscription = stripe.Subscription.retrieve(
        subscription_id, expand=["default_payment_method"]
    )
    payment_method = subscription.default_payment_method

    if payment_method and payment_method.get("card"):
        card = payment_method["card"]
        member.is_subscribed = True
        member.stripe_customer_id = session.customer  # 自アプリMemberのID
        member.stripe_subscription_id = subscription_id
        member.stripe_card_last4 = card["last4"]
        member.stripe_card_brand = card["brand"]
        member.stripe_card_exp_month = card["exp_month"]
        member.stripe_card_exp_year = card["exp_year"]
    else:
        member.is_subscribed = False
        member.stripe_customer_id = ""
        member.stripe_subscription_id = ""
        member.stripe_card_last4 = ""
        member.stripe_card_brand = ""
        member.stripe_card_exp_month = 0
        member.stripe_card_exp_year = 0

    member.save()
    return member


def create_stripe_billing_portal_session(member_id: str, return_path: str):
    """Stripeのサブスク編集ポータルURLを生成"""
    member = get_object_or_404(Member, id=member_id)
    session = stripe.billing_portal.Session.create(
        customer=member.stripe_customer_id,
        return_url=f"{settings.YOUR_DOMAIN}{return_path}?session_id=&user_id={member.id}",
    )
    return session.url


def cancel_stripe_subscription(member_id: str):
    """StripeサブスクをキャンセルしてMember情報を更新"""
    member = get_object_or_404(Member, id=member_id)
    stripe.Subscription.delete(member.stripe_subscription_id)
    member.is_subscribed = False
    member.stripe_customer_id = ""
    member.stripe_subscription_id = ""
    member.stripe_card_last4 = ""
    member.stripe_card_brand = ""
    member.stripe_card_exp_month = 0
    member.stripe_card_exp_year = 0
    member.save()
    return member
