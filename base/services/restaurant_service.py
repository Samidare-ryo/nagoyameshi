# nagoyameshi/base/services/restaurant_service.py

"""
レストラン
CRUD、検索・フィルター、有料会員用の詳細取得、関連データ取得
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Count, Q
from base.models.restaurant_models import Restaurant
from base.models.review_models import Review
from base.models.favorite_models import Favorite


# IDから単体のレストランを取得
def get_restaurant_by_id(restaurant_id: str):
    try:
        return Restaurant.objects.get(pk=restaurant_id, is_published=True)
    except ObjectDoesNotExist:
        return None


# 検索条件でレストラン一覧を取得
def list_restaurants(filters: dict = None):
    queryset = Restaurant.objects.filter(is_published=True)

    if filters:
        if "genre" in filters:
            queryset = queryset.filter(genre=filters["genre"])
        if "area" in filters:
            queryset = queryset.filter(area=filters["area"])
        if "open_now" in filters and filters["open_now"]:
            queryset = queryset.filter(is_open=True)
    return queryset


# 新規レストラン作成
def create_restaurant(data: dict):
    restaurant = Restaurant(**data)
    restaurant.save()
    return restaurant


# レストラン情報更新
def update_restaurant(restaurant_id: str, data: dict):
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        return None
    for key, value in data.items():
        setattr(restaurant, key, value)
    restaurant.save()
    return restaurant


# レストラン削除（論理削除）
def delete_restaurant(restaurant_id: str):
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        return False
    restaurant.is_published = False
    restaurant.save()
    return True


"""
有料会員専用: 店舗詳細＋レビュー・お気に入り情報取得
- member: 会員オブジェクト（有料か無料か判定用）
"""


def get_restaurant_details(restaurant_id: str, member=None):
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        return None

    details = {"restaurant": restaurant}

    # 無料会員は検索のみ
    if not member or not getattr(member, "is_premium", False):
        return details

    # レビュー・評価平均
    reviews = Review.objects.filter(restaurant=restaurant)
    avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"] or 0
    review_count = reviews.count()

    # お気に入り登録数
    favorite_count = Favorite.objects.filter(restaurant=restaurant).count()

    details.update(
        {
            "reviews": reviews,
            "avg_rating": avg_rating,
            "review_count": review_count,
            "favorite_count": favorite_count,
        }
    )

    return details


# キーワード検索＋フィルター処理
def search_restaurants(keyword: str = "", filters: dict = None):
    queryset = Restaurant.objects.filter(is_published=True)
    if keyword:
        queryset = queryset.filter(
            Q(name__icontains=keyword) | Q(description__icontains=keyword)
        )
    if filters:
        queryset = list_restaurants(filters)
    return queryset


# 過去履歴からおすすめ店舗を返す（サンプルは人気順）
def recommend_restaurants(member):
    if not member:
        return Restaurant.objects.none()
    # 過去レビュー・お気に入りの多い店舗を優先
    top_restaurants = Restaurant.objects.annotate(
        fav_count=Count("favorite"), review_count=Count("review")
    ).order_by("-fav_count", "-review_count")[:10]
    return top_restaurants
