# nagoyameshi/base/views/mypage_views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from base.utils.decorators import subscribe_required
from base.services.mypage_service import get_mypage_data_for_subscribed


@login_required
def mypage(request):
    return render(request, "mypage/mypage.html")


@login_required
@subscribe_required
def reservation_history(request):
    context = get_mypage_data_for_subscribed(request.user, section="reservations")
    return render(request, "mypage/reservation_history.html", context)


@login_required
@subscribe_required
def review_history(request):
    context = get_mypage_data_for_subscribed(request.user, section="reviews")
    return render(request, "mypage/review_history.html", context)


@login_required
@subscribe_required
def favorite_list(request):
    context = get_mypage_data_for_subscribed(request.user, section="favorites")
    return render(request, "mypage/favorite_list.html", context)
