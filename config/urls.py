"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# nagoyameshi/config/urls.py
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from base.views.landing_views import landing_page
from base.views.home_views import home_page, restaurant_search_view
from base.views.restaurant_views import restaurant_list
from base.views.member_views import member_edit
from base.views.subscription_views import (
    subscribe_page,
    subscribe_action,
    cancel_subscription_action,
)

from base.views.mypage_views import (
    mypage,
    reservation_history,
    review_history,
    favorite_list,
    account_delete_confirm,
    account_delete,
)

# urls.py
from base.views.account_views import (
    CustomPasswordChangeView,
    CustomPasswordResetView,
    email_verification_request,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),  # allauthのため追加
    path("", landing_page, name="landing"),
    path("home/", home_page, name="home"),
    # サブスク関連
    path("pages/subscribe/", subscribe_page, name="subscribe"),
    path("subscribe/join/", subscribe_action, name="subscribe_action"),
    path(
        "subscribe/cancel/",
        cancel_subscription_action,
        name="cancel_subscription_action",
    ),
    # 検索
    path("serch_result/", restaurant_search_view, name="search_result"),
    # マイページ関連
    path("mypage/", mypage, name="mypage"),  # マイページトップ
    path("mypage/member_edit/", member_edit, name="member_edit"),
    path(
        "mypage/reservations/", reservation_history, name="reservation_list"
    ),  # 予約履歴
    path("mypage/reviews/", review_history, name="review_list"),  # レビュー履歴
    path("mypage/favorites/", favorite_list, name="favorite_list"),  # お気に入り一覧
    path(
        "mypage/account_delete_confirm/",
        account_delete_confirm,
        name="account_delete_confirm",
    ),  # 退会確認
    path("mypage/account_delete/", account_delete, name="account_delete"),  # 退会実行
    # パスワード変更
    path(
        "accounts/password_change/",
        CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    # パスワードリセット（メール送信）
    path(
        "accounts/password_reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    # メール認証リクエスト
    path(
        "accounts/email_verification/",
        email_verification_request,
        name="email_verification_request",
    ),
    # レストラン関係
    path("restaurants/", restaurant_list, name="restaurant_list"),
]
