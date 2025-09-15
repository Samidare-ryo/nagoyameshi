# account/views/account_views.py
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from base.services.member_service import send_verification_email, verify_email_token


# ログイン後のパスワード変更
class CustomPasswordChangeView(PasswordChangeView):
    template_name = "account/password_change.html"
    success_url = reverse_lazy("mypage")

    def form_valid(self, form):
        response = super().form_valid(form)
        # 成功メッセージ（OKボタン付ポップアップ）
        messages.success(
            self.request,
            mark_safe(
                '<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">'
                '<div class="bg-white p-6 rounded-lg shadow-lg text-center max-w-sm">'
                '<p class="mb-4 text-gray-800 font-semibold">パスワードの変更が完了しました</p>'
                f'<a href="{reverse_lazy("mypage")}" class="bg-accent2 text-white px-4 py-2 rounded-lg shadow hover:bg-accent2/80 transition">OK</a>'
                "</div></div>"
            ),
        )
        return response

    def form_invalid(self, form):
        # エラー時もポップアップ
        messages.error(
            self.request,
            mark_safe(
                '<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">'
                '<div class="bg-white p-6 rounded-lg shadow-lg text-center max-w-sm">'
                '<p class="mb-4 text-red-600 font-semibold">パスワードの変更に失敗しました。入力内容を確認してください。</p>'
                f'<a href="{reverse_lazy("password_change")}" class="bg-accent2 text-white px-4 py-2 rounded-lg shadow hover:bg-accent2/80 transition">OK</a>'
                "</div></div>"
            ),
        )
        return self.render_to_response(self.get_context_data(form=form))


# パスワードリセット（メール送信）
class CustomPasswordResetView(PasswordResetView):
    template_name = "account/password_reset.html"
    email_template_name = "account/password_reset_email.html"
    subject_template_name = "account/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            mark_safe(
                '<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">'
                '<div class="bg-white p-6 rounded-lg shadow-lg text-center max-w-sm">'
                '<p class="mb-4 text-gray-800 font-semibold">リセットメールを送信しました</p>'
                f'<a href="{reverse_lazy("password_reset_done")}" class="bg-accent2 text-white px-4 py-2 rounded-lg shadow hover:bg-accent2/80 transition">OK</a>'
                "</div></div>"
            ),
        )
        return response


def email_verification_request(request):
    if request.method == "POST":
        member = request.user
        send_verification_email(member)
        messages.success(
            request, "確認メールを送信しました。メールのリンクをクリックしてください。"
        )
        return redirect("mypage")
    return render(request, "pages/email_verification_request.html")
