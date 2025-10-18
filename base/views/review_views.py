# nagoyameshi/base/views/review_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from base.utils.decorators import subscribe_required
from base.services.review_service import (
    get_member_reviews,
    create_review,
    update_review,
    delete_review,
    get_review,
)


@subscribe_required
def review_list(request):
    reviews = get_member_reviews(request.user)
    return render(request, "pages/review_list.html", {"reviews": reviews})


@subscribe_required
def review_create(request, restaurant_id):
    if request.method == "POST":
        success, msg = create_review(request.user, restaurant_id, request.POST)
        if success:
            messages.success(request, msg)
        else:
            messages.error(request, msg)
        return redirect("review_list")
    return render(request, "pages/review_create.html", {"restaurant_id": restaurant_id})


@subscribe_required
def review_edit(request, review_id):
    review = get_review(review_id, request.user)
    if request.method == "POST":
        success, msg = update_review(request.user, review, request.POST)
        if success:
            messages.success(request, msg)
        else:
            messages.error(request, msg)
        return redirect("review_list")
    return render(request, "pages/review_edit.html", {"review": review})


@subscribe_required
def review_delete(request, review_id):
    review = get_review(review_id, request.user)
    delete_review(request.user, review)
    messages.success(request, "レビューを削除しました。")
    return redirect("review_list")
