from django import forms    # Djangoのformsモジュールをインポート

# SearchFormクラスを定義
# forms.py
class SearchForm(forms.Form):
    words = forms.CharField(
        label='',
        max_length=50,
        required=False,  # ← これ追加して空でも許可！
        widget=forms.TextInput(attrs={
            'class': 'form-control me-2',
            'placeholder': 'キーワードを入力',
        })
    )