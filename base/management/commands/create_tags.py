from django.core.management.base import BaseCommand
from base.models.tag_models import Tag


class Command(BaseCommand):
    help = "NAGOYAMESHI用の初期タグを一括登録します"

    def handle(self, *args, **kwargs):
        tags = [
            # 名古屋めし系
            {"name": "味噌カツ", "slug": "miso-katsu"},
            {"name": "手羽先", "slug": "tebasaki"},
            {"name": "ひつまぶし", "slug": "hitsumabushi"},
            {"name": "あんかけスパ", "slug": "ankake-spa"},
            {"name": "台湾ラーメン", "slug": "taiwan-ramen"},
            {"name": "モーニング", "slug": "morning"},
            {"name": "みそ煮込みうどん", "slug": "miso-nikomi-udon"},
            {"name": "どて煮", "slug": "dote-ni"},
            {"name": "天むす", "slug": "tenmusu"},
            {"name": "きしめん", "slug": "kishimen"},
            {"name": "えびふりゃー", "slug": "ebi-fry"},
            # シーン・利用目的
            {"name": "デート向き", "slug": "date"},
            {"name": "女子会", "slug": "girls-party"},
            {"name": "ファミリー・子連れOK", "slug": "family-kids"},
            {"name": "接待・会食", "slug": "business-meal"},
            {"name": "お一人様歓迎", "slug": "solo-friendly"},
            {"name": "宴会・大人数", "slug": "party-large"},
            {"name": "記念日・誕生日", "slug": "anniversary"},
            {"name": "学生向け", "slug": "student"},
            {"name": "ビジネスランチ", "slug": "business-lunch"},
            {"name": "昼飲み", "slug": "daytime-drink"},
            {"name": "夜飲み", "slug": "nighttime-drink"},
            # サービス・特徴
            {"name": "個室あり", "slug": "private-room"},
            {"name": "掘りごたつ席", "slug": "horigotatsu"},
            {"name": "カウンター席", "slug": "counter"},
            {"name": "テラス席", "slug": "terrace"},
            {"name": "食べ放題", "slug": "all-you-can-eat"},
            {"name": "飲み放題", "slug": "all-you-can-drink"},
            {"name": "テイクアウト可", "slug": "takeout"},
            {"name": "デリバリー対応", "slug": "delivery"},
            {"name": "深夜営業", "slug": "late-night"},
            {"name": "24時間営業", "slug": "open-24h"},
            {"name": "早朝営業", "slug": "early-morning"},
            {"name": "Wi-Fiあり", "slug": "wifi"},
            {"name": "コンセントあり", "slug": "power-outlet"},
            {"name": "禁煙席あり", "slug": "non-smoking"},
            {"name": "ペット可", "slug": "pet-friendly"},
            {"name": "バリアフリー対応", "slug": "barrier-free"},
            {"name": "駐車場あり", "slug": "parking"},
            {"name": "クレジットカード可", "slug": "credit-card"},
            {"name": "電子マネー対応", "slug": "electronic-money"},
            {"name": "子供椅子あり", "slug": "kids-chair"},
            # 雰囲気・スタイル
            {"name": "おしゃれ", "slug": "stylish"},
            {"name": "レトロ", "slug": "retro"},
            {"name": "隠れ家", "slug": "hidden-gem"},
            {"name": "カジュアル", "slug": "casual"},
            {"name": "高級感あり", "slug": "luxury"},
            {"name": "インスタ映え", "slug": "instagrammable"},
            {"name": "落ち着いた雰囲気", "slug": "calm"},
            {"name": "広々", "slug": "spacious"},
            {"name": "アットホーム", "slug": "at-home"},
            {"name": "モダン", "slug": "modern"},
            {"name": "和モダン", "slug": "wa-modern"},
            # こだわり・食文化
            {"name": "地元食材", "slug": "local-ingredients"},
            {"name": "オーガニック", "slug": "organic"},
            {"name": "健康志向", "slug": "healthy"},
            {"name": "ヴィーガン対応", "slug": "vegan"},
            {"name": "グルテンフリー", "slug": "gluten-free"},
            {"name": "ハラール対応", "slug": "halal"},
            {"name": "無添加", "slug": "additive-free"},
            {"name": "地酒・クラフトビールあり", "slug": "local-alcohol"},
            {"name": "季節限定メニュー", "slug": "seasonal"},
            {"name": "手作り料理", "slug": "handmade"},
            {"name": "熟成肉", "slug": "aged-meat"},
            {"name": "自家製スイーツ", "slug": "homemade-sweets"},
        ]

        for t in tags:
            Tag.objects.get_or_create(name=t["name"], slug=t["slug"])

        self.stdout.write(self.style.SUCCESS(f"{len(tags)}個のタグを登録しました。"))
