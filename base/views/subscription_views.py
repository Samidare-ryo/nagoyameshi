# nagoyameshi/base/views/review_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.services.subscription_service import (
    create_subscription,
    cancel_subscription,
    get_latest_subscription,
    get_subscription_history,
    is_subscribed,
)


@login_required
def subscribe_page(request):
    member_id = request.user.id
    current = get_latest_subscription(member_id)
    history = get_subscription_history(member_id)
    context = {
        "current_subscription": current,
        "subscription_history": history,
        "is_subscribed": is_subscribed(member_id),
    }
    return render(request, "pages/subscribe.html", context)


@login_required
def subscribe_action(request):
    if request.method == "POST":
        create_subscription(request.user.id, plan="basic")
        return redirect("subscribe")
    return redirect("subscribe")


@login_required
def cancel_subscription_action(request):
    if request.method == "POST":
        cancel_subscription(request.user.id)
        return redirect("subscribe")
    return redirect("subscribe")
