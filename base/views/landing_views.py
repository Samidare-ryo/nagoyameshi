# nagoyameshi/base/views/landing_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def landing_page(request):
    # ログイン済みの場合はhomeへ遷移する
    if request.user.is_authenticated:
        return redirect("home")
    # 未ログインの場合、ログイン・サインアップへ
    return render(request, "pages/landing.html")
