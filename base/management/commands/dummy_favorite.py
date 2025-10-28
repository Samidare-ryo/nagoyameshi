# nagoyameshi/base/management/commands/dummy_favorite.py

import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from base.models.member_models import Member
from base.models.restaurant_models import Restaurant
from base.models.favorite_models import Favorite


class Command(BaseCommand):
    help = "会員ごとのダミーお気に入りデータを作成します"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num",
            type=int,
            default=5,
            help="1人あたりに作成するお気に入り件数（デフォルト: 5）",
        )

    def handle(self, *args, **options):
        num_per_member = options["num"]

        members = Member.objects.all()
        restaurants = list(Restaurant.objects.filter(is_published=True))

        if not members.exists() or not restaurants:
            self.stdout.write(self.style.WARNING("会員またはレストランが存在しません"))
            return

        total_created = 0
        for member in members:
            chosen_restaurants = random.sample(
                restaurants, min(num_per_member, len(restaurants))
            )
            for restaurant in chosen_restaurants:
                if not Favorite.objects.filter(
                    member=member, restaurant=restaurant
                ).exists():
                    Favorite.objects.create(
                        member=member,
                        restaurant=restaurant,
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                    )
                    total_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"ダミーのお気に入りデータを作成しました ({total_created}件)"
            )
        )
