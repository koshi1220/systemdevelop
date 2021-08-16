from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from .models import Employee,m_department, m_skill, m_training
import datetime

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput(), min_length=4, max_length=20)
    password2 = forms.CharField(label='確認用パスワード', widget=forms.PasswordInput(), min_length=4, max_length=20)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'email', 'date_of_birth', 'password1', )
        labels = {
            'first_name': "名",
            'last_name': "姓",
            'email': "メールアドレス",
            'date_of_birth':"生年月日"  
        }
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=[x for x in reversed(range(1900,datetime.datetime.now().date().year+1))])
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("パスワードが一致しておりません")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    #password = ReadOnlyPasswordHashField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # formの項目ごとにBootstrapのcssクラスを指定できる
        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["date_of_birth"].widget.attrs["class"] = "form-control"
        self.fields["department"].widget.attrs["class"] = "form-control"
        self.fields["training"].widget.attrs["class"] = "form-control"
        self.fields["skill"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Employee
        fields = ('last_name', 'first_name', 'email', 'date_of_birth','department', 'training', 'skill')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin','department')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth','department', 'training', 'skill')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # readonly_fields = ('last_name', 'first_name')
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Employee, UserAdmin)
admin.site.register(m_department)
admin.site.register(m_skill)
admin.site.register(m_training)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)