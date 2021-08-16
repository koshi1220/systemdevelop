from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import m_department, Employee, m_skill, m_training

class LoginForm(AuthenticationForm):
    pass

class SearchForm(forms.Form):
    """
    ListViewの検索フォーム
    """
    # Djangoの要素にCSSを適用したいときにオーバーライド
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # formの項目ごとにBootstrapのcssクラスを指定できる
        self.fields["name"].widget.attrs["placeholder"] = "検索ワード"
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["department"].initial = "部署"
        self.fields["department"].widget.attrs["class"] = "btn btn-outline-info dropdown-item-text"
        self.fields["skill"].widget.attrs["class"] = "btn btn-outline-info dropdown-item-text"
        self.fields["training"].widget.attrs["class"] = "btn btn-outline-info dropdown-item-text"

    name = forms.CharField(
        label='社員情報', max_length=20, required=False)
    department = forms.ModelChoiceField(
        queryset=m_department.objects, label="部署", empty_label="部署", required=False)
    skill = forms.ModelChoiceField(
        queryset=m_skill.objects, label="スキル", empty_label="スキル", required=False)    
    training = forms.ModelChoiceField(
         queryset=m_training.objects, label="トレーニング", empty_label="トレーニング", required=False)