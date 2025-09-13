# nagoyameshi/base/utils/pk_fix_generator.py
from django.utils.crypto import get_random_string

"""
会員・レストラン用ID作成（11桁ランダム英数文字×２）
"""


def create_pk(prefix: str) -> str:
    """PREFIX + ランダム11文字 + ランダム11文字のPKを生成"""
    return f"{prefix}-{get_random_string(11)}-{get_random_string(11)}"
