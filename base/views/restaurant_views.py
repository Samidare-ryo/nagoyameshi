# nagoyameshi/base/views/restaurant_views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from base.models.restaurant_models import Restaurant
from base.services.restaurant_service import list_restaurants, get_restaurant_details
from base.services.favorite_service import toggle_favorite

from base.utils.decorators import subscribe_required

"""
店舗一覧表示（検索可）
無料・有料会員共通
"""


def restaurant_list(request):
    user = request.user
    query = request.GET.get("q", "")
    restaurants = list_restaurants(query)
    context = {"user": user, "restaurants": restaurants, "query": query}
    return render(request, "pages/restaurant_list.html", context)


"""
店舗詳細表示（有料会員のみ）
"""


@subscribe_required
def restaurant_detail(request, restaurant_id):
    restaurant = get_restaurant_details(restaurant_id)
    return render(request, "pages/restaurant_detail.html", {"restaurant": restaurant})


"""
お気に入り登録／解除（有料会員のみ）
"""


@subscribe_required
def favorite_toggle(request, restaurant_id):
    toggle_favorite(request.user, restaurant_id)
    return redirect("restaurant_detail", restaurant_id=restaurant_id)
