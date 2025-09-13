# nagoyameshi/base/services/favorite_service.py
"""お気に入り関連のサービス"""

from django.utils import timezone
from base.models.favorite_models import Favorite
from base.models.member_models import Member
from base.models.restaurant_models import Restaurant


# お気に入り関連の例外
class FavoriteError(Exception):
    pass


# お気に入り登録
def add_favorite(member_id: str, restaurant_id: str):
    """お気に入り登録"""
    try:
        member = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        raise FavoriteError("会員が存在しません")

    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        raise FavoriteError("対象の店舗が存在しません")

    # 既にお気に入り登録済みかチェック
    if Favorite.objects.filter(member=member, restaurant=restaurant).exists():
        raise FavoriteError("すでにお気に入り登録されています")

    favorite = Favorite.objects.create(
        member=member,
        restaurant=restaurant,
        created_at=timezone.now(),
        updated_at=timezone.now(),
    )
    return favorite


# お気に入り削除
def remove_favorite(member_id: str, restaurant_id: str):
    try:
        favorite = Favorite.objects.get(
            member_id=member_id, restaurant_id=restaurant_id
        )
    except Favorite.DoesNotExist:
        raise FavoriteError("お気に入りが存在しません")

    favorite.delete()
    return True


# 会員のお気に入り一覧取得


def get_member_favorites(member_id: str):
    """会員のお気に入り一覧"""
    favorites = Favorite.objects.filter(member_id=member_id).order_by("-created_at")
    return [
        {
            "favorite_id": f.id,
            "restaurant_name": f.restaurant.name,
            "restaurant_id": f.restaurant.id,
            "created_at": f.created_at,
        }
        for f in favorites
    ]


# お気に入りの登録・解除
def toggle_favorite(member_id: str, restaurant_id: str):
    # 戻り値: True = 登録した / False = 解除した
    try:
        favorite = Favorite.objects.get(
            member_id=member_id, restaurant_id=restaurant_id
        )
        favorite.delete()
        return False
    except Favorite.DoesNotExist:
        favorite = add_favorite(member_id, restaurant_id)
        return True
