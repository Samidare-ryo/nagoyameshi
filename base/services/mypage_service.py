# nagoyameshi/base/services/mypage_service.py


def get_mypage_data_for_subscribed(user, section=None):
    """
    サブスク会員のマイページ用データを返すサービス関数
    section: "reservations" | "reviews" | "favorites"
    """
    context = {}

    if section == "reservations":
        context["reservations"] = user.reservation_set.all()
    elif section == "reviews":
        context["reviews"] = user.review_set.all()
    elif section == "favorites":
        context["favorites"] = user.favorites.all()

    return context
