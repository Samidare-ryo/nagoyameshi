# nagoyameshi/base/services/home_service.py

"""
ホームデータ取得
"""

from typing import List, Dict
from django.db.models import Count, Avg
from base.models.restaurant_models import Restaurant
from base.models.review_models import Review
from base.models.favorite_models import Favorite
from base.models.member_models import Member


# 無料会員用ホームデータ
def get_restaurant_data():
    restaurants = Restaurant.objects.all()[:20]  # 上位20件を表示
    return restaurants


"""
    for r in restaurants:
        data.append(
            {
                "id": r.id,
                "name": r.name,
                "category": r.category.name if r.category else None,
            }
        )
    return data
"""


# 有料会員ホームデータ
def get_home_data_for_subscribed(member_id: str):
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        return []

    restaurants = Restaurant.objects.annotate(
        avg_rating=Avg("review__rating"),
        review_count=Count("review"),
        favorite_count=Count("favorite"),
    ).all()[:20]  # 上位20件

    data = []
    for r in restaurants:
        data.append(
            {
                "id": r.id,
                "name": r.name,
                "category": r.category.name if r.category else None,
                "area": r.area,
                "avg_rating": r.avg_rating or 0,
                "review_count": r.review_count,
                "favorite_count": r.favorite_count,
                "is_favorited": Favorite.objects.filter(
                    member=member, restaurant=r
                ).exists(),
            }
        )
    return data
