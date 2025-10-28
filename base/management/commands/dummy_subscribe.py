# nagoyameshi/base/management/commands/dummy_subscribe.py

from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from base.models.member_models import Member
from base.models.subscription_models import Subscription


class Command(BaseCommand):
    help = "全会員を有料会員扱いにするダミーサブスクを作成します"

    def add_arguments(self, parser):
        parser.add_argument(
            "--plan",
            type=str,
            default="premium",
            help="作成するプラン名（デフォルト: premium）",
        )
        parser.add_argument(
            "--duration_days",
            type=int,
            default=365,
            help="サブスク有効日数（デフォルト: 365日）",
        )

    def handle(self, *args, **options):
        plan_name = options["plan"]
        duration_days = options["duration_days"]

        members = Member.objects.all()
        if not members.exists():
            self.stdout.write(self.style.WARNING("会員が存在しません"))
            return

        now = timezone.now()
        total_created = 0
        for member in members:
            # 既存のサブスクは無効化
            Subscription.objects.filter(member=member, active=True).update(
                active=False, cancelled=True
            )

            # 新規サブスク作成
            expiry_date = now + timedelta(days=duration_days)
            Subscription.objects.create(
                member=member,
                plan=plan_name,
                start_date=now,
                expiry_date=expiry_date,
                active=True,
                cancelled=False,
            )
            total_created += 1

        self.stdout.write(
            self.style.SUCCESS(f"全会員を有料会員に設定しました ({total_created}件)")
        )
