from django import forms
from django.forms import fields
from django.forms import widgets
from repository import models
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
"""
模块功用：该模块用于注册，登录，用户信息修改时，form表单的html代码生成，输入字段信息的验证。
"""


class BlogForm(forms.Form):
    """
    功能：Django中的form组件，用于生成html代码和验证输入的字段；用于用户祖册博客时用。
    需要生成和验证的字段有：
    username：用户名
    pwd：密码
    email：邮箱
    pwdConfirm：密码确认
    """
    # 用户名字段，需要提供该字段，最大长度为64字节，参数error_messages为对错信息的定制
    username = fields.CharField(
        max_length=64,
        required=True,
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"用户名"}),
        error_messages={
                "max_length":"用户名太长了",
                "required":"需要提供用户名",
    })
    # 密码字段，需要提供该字段，最小长度6字节，最大长度32字节，widget用于向生成的html代码增加属性。
    # widget不是很懂可以看源码
    pwd = fields.CharField(
        max_length=32,
        min_length=6,
        required=True,
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"密码","type":"password"}),
        error_messages={
                "max_length": "密码太长",
                "min_length": "密码太短",
                "required": "需要设置密码",
    })
    # 邮箱字段，需要提供该字段，输入需要为邮箱格式，封装在字段中
    email = fields.EmailField(
        required=True,
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"邮箱"}),
        error_messages={
                "required":"需要提供邮箱",
                "invalid":"邮箱格式不正确"
    })
    # 确认密码字段，和密码字段要求相同
    pwdConfirm = fields.CharField(
        max_length=32,
        min_length=6,
        required=True,
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"确认密码","type":"password"}),
        error_messages={
                "max_length": "密码太长",
                "min_length": "密码太短",
                "required": "需要确认密码",
    })

    # 在上述的用户名要求字段验证完成后还可以对一些其他要求验证的东西进行验证
    def clean_username(self):
        """
        验证注册的用户名是否存在在数据库中，即是否已经注册过。如果已经存在，则抛出异常，用户名已经存在
        :return: 验证通过后的数据
        """
        user = self.cleaned_data.get("username")
        if user:
            if models.UserTable.objects.filter(username=user).count():
                raise ValidationError("用户名已经存在")
            else:
                return self.cleaned_data["username"]

    # 在上述的验证后还有需要进行验证的，可以重写clean方法，如：确认密码是否一致
    def clean(self):
        """
        验证通过返回正确数据；没通过，在pwdConfirm字段加入错误信息
        :return: 所有验证后的数据
        """
        if self.cleaned_data.get("pwd") is not None and self.cleaned_data.get("pwdConfirm") is not None:
            if self.cleaned_data["pwd"] == self.cleaned_data["pwdConfirm"]:
                return self.cleaned_data
            else:
                self.add_error("pwdConfirm","确认密码失败，两次输入密码不一致")


class VerifyBlogForm(forms.Form):
    """
    功能：用户登录信息的验证，生成登录页面的html代码和字段验证，字段验证输入是否和服规范
    """
    username = fields.CharField(
        max_length=64,
        required=True,
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"用户名"}),
        error_messages={
                "max_length":"用户名太长了",
                "required":"请填写登录用户名",
    })
    pwd = fields.CharField(
        max_length=32,
        required=True,
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"密码","type":"password"}),
        error_messages={
                "max_length": "密码太长",
                "required": "需要设置密码",
    })

    def clean(self):
        """
        验证该用户是否已经注册，没有注册则抛出用户名不存在异常，注册，输入密码不对抛出密码错误异常
        如果用户名和密码都正确，则返回验证通过后的数据。
        :return: 对用户名和密码验证通过后的数据
        """
        username = self.cleaned_data.get("username")
        user_obj = models.UserTable.objects.filter(username=username).first()
        if user_obj:
            password = self.cleaned_data.get("pwd")
            if password == user_obj.pwd:
                self.cleaned_data["username"] = username
                return self.cleaned_data
            else:
                self.add_error("pwd","密码错误")
        else:
            self.add_error("username","用户名不存在")


class UserInfoForm(forms.Form):
    """
    UserInfoForm用于1、生成后台管理中，用户信息填写的input表单代码
                    2、帮助验证用户输入的信息是否合乎规范
                    username：用户名
                    email：用户邮箱
                    user_nickname：用户昵称
                    blog_title：博客标题
                    上述四个字段在用户信息管理页面中都可输入为空，输入为空点击保存表示对用户信息不予修改
    """
    username = fields.CharField(
        max_length=64,
        required=False,
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"请输入用户名"}),
        error_messages={
                "max_length":"用户名太长了",
    })
    email = fields.EmailField(
        required=False,
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"请输入邮箱"}),
        error_messages={
                "invalid":"邮箱格式不正确"
    })
    user_nickname = fields.CharField(
        max_length=32,
        required=False,
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"请输入昵称"}),
        error_messages={
            "max_length":"昵称过长",
        })
    blog_title = fields.CharField(
        max_length=128,
        required=False,
        widget=widgets.Textarea(attrs={"class":"form-control","style":"height: 120px"}),
        error_messages={
            "max_length": "博客标题太长",
        })

    def __init__(self,username,*args,**kwargs):
        self.username = username
        super(UserInfoForm, self).__init__(*args,**kwargs)
        print(self.fields["username"])
        self.fields["username"].widget = widgets.TextInput(attrs={"class":"form-control","placeholder":"%s"%username})
        user_obj= models.UserTable.objects.filter(username=username).first()
        email = user_obj.email
        nick_name = user_obj.user_nickname
        self.fields["email"].widget = widgets.TextInput(attrs={"class":"form-control","placeholder":"%s"%email})
        self.fields["user_nickname"].widget = widgets.TextInput(attrs={"class":"form-control","placeholder":"%s"%nick_name})

    def clean_username(self):
        """
        对用户名字段进行再次验证，
        1、输入的是原来自己的用户名，返回该用户名
        2、输入的是库中没有存在的用户名，返回该用户名
        3、输入的是已经存在，别人使用的用户名，抛出异常‘用户名已经存在’
        :return:
        """
        user = self.cleaned_data.get("username")
        if user == self.username:
            return self.cleaned_data["username"]
        elif user:
            if models.UserTable.objects.filter(username=user).count():
                raise ValidationError("用户名已经存在")
            else:
                return self.cleaned_data["username"]
