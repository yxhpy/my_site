from django import forms
from .models import UserExtension, Comment
from django.contrib.auth.models import User


class BaseForm(object):
    def get_errors(self):
        errors = {}
        for error_name, error_values in self.errors.get_json_data().items():
            errors[error_name] = []
            for error_value in error_values:
                errors[error_name].append(error_value['message'])
        return errors


class RegisterForm(forms.ModelForm, BaseForm):
    email = forms.EmailField(error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})

    username = forms.CharField(min_length=6,
                               error_messages={'required': '账号不能为空',
                                               'min_length': '密码最短为6'})
    password = forms.CharField(min_length=8,
                               error_messages={'required': '密码不能为空',
                                               'min_length': '密码最短为8'})
    re_password = forms.CharField(min_length=8,
                                  error_messages={'required': '重复密码不能为空',
                                                  'min_length': '重复密码密码最短为8'})

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError(message='两次密码不一样', code='pass_different')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class LoginForm(forms.Form, BaseForm):
    email = forms.EmailField(error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    password = forms.CharField(min_length=8,
                               error_messages={'required': '密码不能为空',
                                               'min_length': '密码最短为8'})


from DjangoUeditor.forms import UEditorField


class ArticleForm(forms.Form):
    content = UEditorField("", initial="", width='', height=200, toolbars='full', imagePath='ueimages/',
                           filePath='files_ue/')


class CommentForm(forms.Form):
    content = UEditorField("", initial="", width='', height=200, toolbars='mini', imagePath='ueimages/',
                           filePath='files_ue/')
