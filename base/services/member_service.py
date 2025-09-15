# nagoyameshi/base/services/member_service.py
"""
会員関連のサービス処理
「会員管理の基本処理（作成・更新・削除・課金状態チェック）」を担う
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.mail import send_mail
from base.models.member_models import Member
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
import secrets

Member = get_user_model()


# 会員関連の例外
class MemberError(Exception):
    pass


"""会員CRUD系"""


# 新規会員を作成(無料会員からのスタート)
def create_member(username: str, email: str, password: str) -> Member:
    if Member.objects.filter(username=username).exists():
        raise MemberError("このユーザー名は既に使用されています。")
    if Member.objects.filter(email=email).exists():
        raise MemberError("このメールアドレスは既に登録されています。")

    member = Member.objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    member.is_subscribed = False
    member.save()
    return member


# 新規会員を編集
def update_member(member_id: str, **kwargs) -> Member:
    try:
        member = Member.objects.get(id=member_id)
    except ObjectDoesNotExist:
        raise MemberError("指定された会員は存在しません。")

    for key, value in kwargs.items():
        if hasattr(member, key):
            setattr(member, key, value)
        else:
            raise MemberError(f"会員に '{key}' という属性は存在しません。")

    member.save()
    return member


# 会員を削除（論理削除を想定し is_active=False）
def delete_member(member_id: str):
    try:
        member = Member.objects.get(id=member_id)
    except ObjectDoesNotExist:
        raise MemberError("指定された会員は存在しません。")

    member.is_active = False
    member.save()


# 会員を取得
def get_member(member_id: str) -> Member:
    try:
        return Member.objects.get(id=member_id)
    except ObjectDoesNotExist:
        raise MemberError("指定された会員は存在しません。")


"""サブスク（有料会員）関係"""


# 有料会員かどうかの判定
def is_subscribed_member(member_id: str) -> bool:
    try:
        member = Member.objects.get(id=member_id)
    except ObjectDoesNotExist:
        raise MemberError("指定された会員は存在しません。")
    return getattr(member, "is_subscribed", False)


# 有料会員に昇格　months: 契約延長月数（デフォルト1ヶ月）
def upgrade_to_subscribed(member: Member, months: int = 1) -> Member:
    now = timezone.now()
    # 残り期間がある場合は延長
    if member.subscription_expiry and member.subscription_expiry > now:
        member.subscription_expiry += relativedelta(months=months)
    # 新規 or 期限切れの場合は新たに設定
    else:
        member.subscription_expiry = now + relativedelta(months=months)

    member.is_subscribed = True
    member.save()
    return member


# 無料会員に降格 （- keep_until_expiry=True の場合、契約期間中は有料判定を維持）
def downgrade_to_free(member: Member, keep_until_expiry: bool = True) -> Member:
    now = timezone.now()

    # 契約期限が設定されていない場合、即時降格
    if not member.subscription_expiry:
        member.is_subscribed = False
    # 契約期限がある場合
    elif not keep_until_expiry or member.subscription_expiry <= now:
        member.is_subscribed = False

    member.save()
    return member


# 有効期限切れで自動的に無料会員へ
# （期限切れ後もsubscription_expiryは残す）
def downgrade_if_expired(member: Member) -> Member:
    if member.subscription_expiry and member.subscription_expiry <= timezone.now():
        member.is_subscribed = False
        member.save()
    return member


# Memberインスタンスに対して、有料会員かどうかを判定
def is_subscribed_member_instance(member: Member) -> bool:
    return getattr(member, "is_subscribed", False)


# メール認証トークン生成
def generate_email_verification_token() -> str:
    return secrets.token_urlsafe(32)


# メール送信
def send_verification_email(member: Member):
    token = generate_email_verification_token()
    member.email_verification_token = token
    member.email_verification_sent_at = timezone.now()
    member.save()

    verification_link = f"https://example.com/verify_email/{token}/"
    send_mail(
        subject="メールアドレス確認",
        message=f"下記リンクをクリックしてメールアドレスを認証してください。\n{verification_link}",
        from_email="noreply@example.com",
        recipient_list=[member.email],
    )


# トークンでメール認証
def verify_email_token(token: str) -> bool:
    try:
        member = Member.objects.get(email_verification_token=token)
    except Member.DoesNotExist:
        return False

    member.is_email_verified = True
    member.email_verification_token = None
    member.save()
    return True
