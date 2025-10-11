# nagoyameshi/base/utils/decorators.py

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from base.models.member_models import Member, MembershipType

"""
有料会員のみの制限
"""


def subscribe_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            member_info = Member.objects.get(id=request.user.id)
            if member_info.membership_type.code == MembershipType.SUBSCRIBED:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "この機能は有料会員のみ利用可能です。")
                return redirect("landing")
        else:
            return redirect("account_login")

    return _wrapped_view
