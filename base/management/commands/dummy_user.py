from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "ダミーユーザー作成"

    def handle(self, *args, **options):
        print("ダミーユーザーを作成しました。")
