# nagoyameshi/base/utils/pk_dit_generator.py

from django.utils.crypto import get_random_string
from datetime import datetime

"""
レビュー・お気に入り用ID作成（年月日時分＋10桁ランダム英数文字）
"""


def create_dt_pk(prefix: str) -> str:
    """接頭辞 + 年月日時分（12文字）+ ランダム10文字のPKを生成"""
    date_str = datetime.now().strftime("%Y%m%d%H%M")
    return f"{prefix}-{date_str}-{get_random_string(10)}"
