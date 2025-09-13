# bnagoyameshi/ase/views/reservation_views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from base.utils.decorators import subscribe_required
from base.services.reservation_service import (
    get_user_reservations,
    create_reservation,
    cancel_reservation,
)


@subscribe_required
def reservation_list(request):
    reservations = get_user_reservations(request.user)
    return render(
        request, "reservation/reservation_list.html", {"reservations": reservations}
    )


@subscribe_required
def reservation_create(request, restaurant_id):
    if request.method == "POST":
        create_reservation(request.user, restaurant_id, request.POST)
        messages.success(request, "予約が完了しました。")
        return redirect("reservation_list")
    return render(
        request, "reservation/reservation_create.html", {"restaurant_id": restaurant_id}
    )


@subscribe_required
def reservation_cancel(request, reservation_id):
    cancel_reservation(request.user, reservation_id)
    messages.success(request, "予約をキャンセルしました。")
    return redirect("reservation_list")
