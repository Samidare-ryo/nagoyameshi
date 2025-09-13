# nagoyameshi/base/services/review_service.py
"""レビュー関連のサービス"""

from django.shortcuts import get_object_or_404
from django.utils import timezone
from base.models.review_models import Review
from base.models.member_models import Member
from base.models.restaurant_models import Restaurant
from base.models.review_models import Review


# レビュー捜査中に対処できないエラーが発生した場合に使用する例外
class ReviewError(Exception):
    pass


# レビューを作成 - ratingは1〜5
def create_review(member_id: str, restaurant_id: str, content: str, rating: int):
    try:
        member = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        raise ReviewError("会員が存在しません")

    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        raise ReviewError("対象の店舗が存在しません")

    if not (1 <= rating <= 5):
        raise ReviewError("評価は1〜5の範囲で指定してください")

    review = Review.objects.create(
        member=member,
        restaurant=restaurant,
        content=content,
        rating=rating,
        created_at=timezone.now(),
        updated_at=timezone.now(),
    )
    return review


# レビューの更新
def update_review(review_id: str, content: str, rating: int):
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        raise ReviewError("レビューが存在しません")

    if not (1 <= rating <= 5):
        raise ReviewError("評価は1〜5の範囲で指定してください")

    review.content = content
    review.rating = rating
    review.updated_at = timezone.now()
    review.save()
    return review


# レビューを削除（論理削除なども可）
def delete_review(review_id: str):
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        raise ReviewError("レビューが存在しません")

    review.delete()
    return True


# 会員が投稿したレビュー一覧を取得
def get_member_reviews(member_id: str):
    reviews = Review.objects.filter(member_id=member_id).order_by("-created_at")
    return [
        {
            "review_id": r.id,
            "restaurant_name": r.restaurant.name,
            "content": r.content,
            "rating": r.rating,
            "created_at": r.created_at,
        }
        for r in reviews
    ]


"""レビューID取得"""


def get_review_id(review_id: str):
    return get_object_or_404(Review, id=review_id)
