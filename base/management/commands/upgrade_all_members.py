# nagoyameshi/base/management/commands/upgrade_all_members.py

from django.core.management.base import BaseCommand
from base.models.member_models import Member, MembershipType


class Command(BaseCommand):
    help = "全会員の membership_type を free から subscribed に変更します"

    def handle(self, *args, **options):
        subscribed_type = MembershipType.objects.get(code=MembershipType.SUBSCRIBED)
        members_to_upgrade = Member.objects.filter(
            membership_type__code=MembershipType.FREE
        )

        total_upgraded = members_to_upgrade.update(membership_type=subscribed_type)
        self.stdout.write(
            self.style.SUCCESS(f"{total_upgraded} 名の会員を subscribed に変更しました")
        )
