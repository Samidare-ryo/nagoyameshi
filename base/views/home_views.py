# nagoyameshi/base/views/home_views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from base.services.search_service import search_restaurants
from base.services.home_service import (
    get_home_data_for_free,
    get_home_data_for_subscribed,
)
from base.models.member_models import Member  # ログインユーザー情報取得


@login_required
def home_page(request):
    user = request.user

    # レストランデータ取得（無料/有料会員で分岐）
    if user.membership_type == "subscribed":
        restaurants = get_home_data_for_subscribed(user.id)
    else:
        restaurants = get_home_data_for_free()
        # 無料会員向けに有料プラン案内を追加
        premium_info = {
            "message": "有料会員になるとレビューやお気に入りが利用可能です！",
            "link": "/membership/subscribe",
        }
    # 検索フォーム保持用のparams（keywordのみ）
    params = {"keyword": request.GET.get("keyword", "")}

    # ビューに渡すコンテキスト
    context = {
        "user": user,
        "membership_type": user.membership_type,
        "restaurants": restaurants,
        "params": params,
    }

    # 無料会員なら案内も追加
    if user.membership_type != "subscribed":
        context["premium_info"] = premium_info

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
