# nagoyameshi/base/views/home_views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from base.services.search_service import search_restaurants
from base.services.home_service import (
    get_restaurant_data,
)
from base.models.member_models import Member  # ログインユーザー情報取得


@login_required
def home_page(request):
    user = request.user
    restaurants = get_restaurant_data()

    # 検索フォーム保持用のparams（keywordのみ）
    params = {"keyword": request.GET.get("keyword", "")}

    # ビューに渡すコンテキスト
    context = {
        "user": user,
        "restaurants": restaurants,
        "params": params,
    }

    return render(request, "pages/home.html", context)


"""レストラン検索画面"""


@login_required
def restaurant_search_view(request):
    user = request.user

    # 検索条件をGETパラメータから取得
    params = {
        "keyword": request.GET.get("keyword", ""),
        "category_id": request.GET.get("category_id"),
        "min_price": request.GET.get("min_price"),
        "max_price": request.GET.get("max_price"),
        "sort_by": request.GET.get("sort_by", "rating"),
        "page": int(request.GET.get("page", 1)),
    }

    # 検索サービスを呼び出し
    search_result = search_restaurants(user, params)

    context = {
        "restaurants": search_result["restaurants"],
        "is_paid_member": search_result["is_paid_member"],
        "page": search_result["page"],
        "total_pages": search_result["total_pages"],
        "total_count": search_result["total_count"],
        "params": params,  # 検索フォーム保持用
    }

    return render(request, "pages/restaurant_search.html", context)
