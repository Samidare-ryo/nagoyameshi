# nagoyameshi/base/views/subscription_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from base.services.subscription_service import (
    create_stripe_checkout_session,
    retrieve_stripe_session,
    create_stripe_billing_portal_session,
    cancel_stripe_subscription,
)


PRICE_ID = "PRICE_ID"


@login_required
def subscribe_register(request):
    if request.method == "POST":
        url = create_stripe_checkout_session(
            request.user.id,
            price_id=PRICE_ID,
            success_path="/accounts/subscribe-success/",
            cancel_path="/accounts/subscribe-register/",
        )
        return redirect(url)
    return render(request, "subscribe/subscribe_register.html")


@login_required
def subscribe_success(request):
    session_id = request.GET.get("session_id")
    user_id = request.GET.get("user_id")
    if not session_id or not user_id:
        return HttpResponse("Invalid request", status=400)
    retrieve_stripe_session(session_id, user_id)
    return redirect("top_page")


@login_required
def subscribe_edit(request):
    if request.method == "POST":
        url = create_stripe_billing_portal_session(
            request.user.id, return_path="/accounts/subscribe-success/"
        )
        return redirect(url)
    return render(request, "subscribe/subscribe_edit.html", {"user": request.user})


@login_required
def subscribe_cancel(request):
    if request.method == "POST":
        cancel_stripe_subscription(request.user.id)
        return redirect("top_page")
    return render(request, "subscribe/subscribe_cancel.html", {"user": request.user})
