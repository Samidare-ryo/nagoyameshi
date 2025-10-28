from django.core.management.base import BaseCommand
from faker import Faker
import MeCab  # type: ignore
import ipadic  # type: ignore
from base.models.member_models import Member, MembershipType


dic_kana = {
    "知実": "トモミ",
    "里佳": "リカ",
    "七夏": "ナナカ",
    "学": "マナブ",
    "亮平": "リョウヘイ",
    "裕太": "ユウタ",
    "治": "オサム",
    "聡太郎": "ソウタロウ",
    "拓真": "タクマ",
    "陽子": "ヨウコ",
}


def KanaFromKanji(kanji):
    mecab = MeCab.Tagger(ipadic.MECAB_ARGS)
    kana = ""
    items = mecab.parse(kanji).split("\n")

    for item in items:
        words = item.split(",")
        if len(words) == 9:
            kana += words[7]

    return kana


class Command(BaseCommand):
    help = "ダミーユーザー作成"

    def handle(self, *args, **options):
        fake = Faker("ja_JP")

        for _ in range(10):
            name = fake.name()
            email = fake.email()
            zipcode = fake.zipcode()
            address = fake.address()
            phone_number = fake.phone_number()
            job = fake.job()
            birthday = fake.date_of_birth(minimum_age=18, maximum_age=80)

            last_name = name.split(" ")[0]
            last_name_kana = KanaFromKanji(last_name)

            first_name = name.split(" ")[1]

            if first_name in dic_kana:
                first_name_kana = dic_kana[first_name]

            else:
                first_name_kana = KanaFromKanji(first_name)

            """
            print(
                f"{name} {last_name_kana} {first_name_kana} {email} {zipcode} {address} {phone_number} {job} {birthday}"
            )
            """

            # 無料会員をデフォルトで割り当てを行う。
            default_membership = MembershipType.objects.get(code="free")

            # DBに保存
            member = Member.objects.create(
                username=fake.user_name(),
                email=email,
                first_name=first_name,
                last_name=last_name,
                first_name_kana=first_name_kana,
                last_name_kana=last_name_kana,
                zipcode=zipcode,
                address=address,
                phone_number=phone_number,
                job=job,
                birthday=birthday,
                is_active=True,
                membership_type=default_membership,
            )

            # 確認用に出力
            self.stdout.write(self.style.SUCCESS(f"Created member {member.username}"))
