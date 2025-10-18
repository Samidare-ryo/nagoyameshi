# nagoyameshi/base/views/favorite_views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models.restaurant_models import Restaurant
from base.services.favorite_service import (
    get_member_favorites,
    toggle_favorite,
)
from base.utils.decorators import subscribe_required

"""
有料会員のみ
"""


# ログインユーザーのお気に入り一覧表示
@login_required
@subscribe_required
def favorite_list(request):
    user = request.user
    favorites = get_member_favorites(user.id)
    context = {"user": user, "favorites": favorites}
    return render(request, "pages/favorite_list.html", context)


# お気に入り登録／解除
@login_required
@subscribe_required
def favorite_toggle_view(request, restaurant_id):
    user = request.user
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    toggle_favorite(user.id, restaurant.id)
    messages.success(request, "お気に入りを更新しました。")
    return redirect("restaurant_detail", restaurant_id=restaurant.id)
