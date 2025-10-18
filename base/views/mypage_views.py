# nagoyameshi/base/views/mypage_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from base.utils.decorators import subscribe_required
from base.services.mypage_service import get_mypage_data_for_subscribed


@login_required
def mypage(request):
    return render(request, "pages/mypage.html")


@login_required
@subscribe_required
def reservation_history(request):
    context = get_mypage_data_for_subscribed(request.user, section="reservations")
    return render(request, "pages/reservation_history.html", context)


@login_required
@subscribe_required
def review_history(request):
    context = get_mypage_data_for_subscribed(request.user, section="reviews")
    return render(request, "pages/review_history.html", context)


@login_required
@subscribe_required
def favorite_list(request):
    context = get_mypage_data_for_subscribed(request.user, section="favorites")
    return render(request, "pages/favorite_list.html", context)


@login_required
def account_delete_confirm(request):
    """退会確認画面"""
    return render(request, "pages/account_delete.html")


@login_required
def account_delete(request):
    """退会実行処理"""
    if request.method == "POST":
        user = request.user
        logout(request)  # セッション終了
        user.delete()  # ユーザー削除
        return redirect("landing")  # トップページなどにリダイレクト
    return redirect("mypage")
