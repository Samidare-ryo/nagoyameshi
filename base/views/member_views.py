# nagoyameshi/base/views/member_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.services.member_service import update_member

@login_required
def member_edit(request):
    """会員情報編集"""
    user = request.user

    if request.method == "POST":
        user.last_name = request.POST.get("last_name", "")
        user.first_name = request.POST.get("first_name", "")
        user.last_name_kana = request.POST.get("last_name_kana", "")
        user.first_name_kana = request.POST.get("first_name_kana", "")
        user.email = request.POST.get("email", "")
        user.phone_number = request.POST.get("phone_number", "")
        user.address = request.POST.get("address", "")

        # 保存
        user.save()
        messages.success(request, "会員情報を更新しました。")
        return redirect("mypage")

    return render(request, "pages/member_edit.html", {"user": user})
