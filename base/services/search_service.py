# nagoyameshi/base/services/search_service.py
from django.db.models import Q
from django.core.paginator import Paginator
from base.models.restaurant_models import Restaurant


def _build_search_queryset(params):
    qs = Restaurant.objects.all()
    filters = Q()

    # キーワード検索
    if params.get("keyword"):
        keyword = params["keyword"]
        filters &= Q(name__icontains=keyword) | Q(description__icontains=keyword)

    # カテゴリ検索
    if params.get("category_id"):
        filters &= Q(category_id=params["category_id"])

    # 予算
    if params.get("min_price"):
        filters &= Q(average_price__gte=params["min_price"])
    if params.get("max_price"):
        filters &= Q(average_price__lte=params["max_price"])

    qs = qs.filter(filters)

    """ 評価によるソートをコメントアウト
    # 平均評価
    qs = qs.annotate(avg_rating=Avg("reviews__rating"))

    # ソート順
    sort_by = params.get("sort_by", "rating")
    if sort_by == "rating":
        qs = qs.order_by("-avg_rating", "-updated_at")
    elif sort_by == "updated":
        qs = qs.order_by("-updated_at", "-avg_rating")

    return qs
    """
    qs = qs.order_by("-updated_at")
    return qs


def _format_restaurant_list(qs):
    results = []
    for r in qs:
        results.append(
            {
                "id": r.id,
                "name": r.name,
                "category": r.category.name if r.category else None,
                "avg_rating": getattr(r, "avg_rating", None),
                "average_price": r.average_price,
            }
        )
    return results


# レストラン検索を実行し、レスポンスdictを返す
# - ページネーション 10件/ページ
# - ソート順: 評価高い順 or 更新日順
def search_restaurants(member, params):
    qs = _build_search_queryset(params)

    # ページネーション
    page_number = params.get("page", 1)
    paginator = Paginator(qs, 10)  # 10件ずつ
    page_obj = paginator.get_page(page_number)

    formatted = _format_restaurant_list(page_obj)

    return {
        "restaurants": formatted,
        "is_paid_member": member.is_paid,
        "page": page_number,
        "total_pages": paginator.num_pages,
        "total_count": paginator.count,
    }
