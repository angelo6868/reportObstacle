from django.shortcuts import render,HttpResponse,redirect
from repository import models
from web.webForm import BlogForm,VerifyBlogForm
from genCode.check_code import CheckCode
from io import BytesIO
import json
from backend import pager


def homepage(request,*args,**kwargs):
    """
    博客主页面
    开始搜索，或者输入博客url请求进入博客系统的主页
    :param request: 输入博客的url
    :param args:
    :param kwargs:
    :return: 返回博客的首页页面
    """
    if kwargs:
        # 根据分类来选择在博客系统主页面显示的文章
        if kwargs["label_id"] == '0':
            kwargs.pop("label_id")
    # 在博客页面中会显示博客中注册了的博客用户，博客系统中的文章，分类和标签，先占时把数据库中所有的这些内容都拿出来显示
    # 在页面上
    user = models.UserTable.objects.all()
    classification = models.Classification.objects.all()
    article = models.Article.objects.filter(**kwargs)
    label = models.Label.objects.all()
    return render(request,"homepage.html",locals())


def register(request):
    """
    注册页面
    在主页面中点击注册会进入到该视图处理函数，请求处理分为get和post两种处理
    :param request:
    :return:返回注册的页面（用单独的页面注册，form表单提交，然后刷新页面，没有采用ajax方式）
    注册页面有各个字段的填写，还有请求加载验证码
    """
    # 1、get请求时，用BlogForm生成html代码
    if request.method == "GET":
        obj = BlogForm()
        return render(request,"register.html",locals())
    # 2、post请求时，用BlogForm验证数据
    elif request.method == "POST":
        obj = BlogForm(request.POST)
        if obj.is_valid():
            # 加入验证码验证功能，cd_check为用户注册时输入放入验证码
            cd_check = request.POST.get("code_confirm")
            # 页面上生成验证码时，将验证码上的字符串先保存到session中
            # 取得保存在session中的验证码，和用户输入的验证码对比
            if request.session.get("check_code") == cd_check:
                # 相同时，这儿代码验证码输入正确，注册信息验证通过，在数据库中创建用户数据
                # 创建数据成功后，页面重定向到博客系统主页面
                obj.cleaned_data.pop("pwdConfirm")
                models.UserTable.objects.create(**obj.cleaned_data)
                return redirect("/homepage/")
            else:
                # 验证码输入错误时，返回注册页面
                code_check_error = "验证码错误"
                return render(request,"register.html",locals())
        # 用户注册字段输入错误时，返回注册页面
        else:
            return render(request,"register.html",locals())


def login(request):
    """
    登录页面
    如果session中is_login为true，则不用验证，直接登录。
    在session中保留两个东西，1、登录状态，2、登录者的用户名
    :param request:请求，带着sessionid过来
    :return:1、未登录返回登录页面；2、登录成功重定向到自己的主页面；3、session上登录状态为true，重定向
                到自己主页面。
    """
    if request.session.get("is_login") == "true":
        username = request.session.get("username")
        return redirect("/%s.html/" % username)
    else:
        if request.method == "GET":
            # 登录验证，用form组件生成html代码
            obj = VerifyBlogForm()
            return render(request,"login.html",locals())
        elif request.method == "POST":
            # 提交表单后，用form组件验证输入字段的正确性
            obj = VerifyBlogForm(request.POST)
            username = request.POST.get("username")
            if obj.is_valid():
                request.session["is_login"] = "true"
                request.session["username"] = username
                return redirect("/%s.html/"%username)
            else:
                return render(request,"login.html",locals())


def test(request):
    return render(request,"test.html")


def identify_code(request):
    """
    功能：img标签中src根据url请求，生成验证码图片
    :param request:
    :return:内存中保存的图片供img标签使用
    """
    # 使用io和使用文件的方式一样，相当于打开一个文件
    f = BytesIO()
    # 创建验证码，得到图片对象和验证码的字符串
    code_identify = CheckCode(70,30,25)
    img,code = code_identify.picture_generator()
    # 将图片写入到文件f中
    img.save(f,'PNG')
    # 将验证码字符串保存在sessionid对应的session中
    request.session["check_code"] = code
    return HttpResponse(f.getvalue())


def personal_page(request):
    """
    直接url请求，未登录时，不返回用户页面
    :param request:
    :return: 登录状态为true，根据request请求返回用户主页面，否则返回登录页面。
    """
    if request.session.get("is_login") == "true":
        # 根据传递的url拿到用户名，可以采用另外一种方式拿到用户名
        username = request.path.split(".")[0].replace("/","")
        # 拿到标签的queryset对象
        tag = models.Label.objects.filter(user__username=username)
        # 拿到文章的queryset对象
        obj = models.Article.objects.filter(user__user__username=username)
        # 拿到分类的queryset对象
        classification = models.Classification.objects.filter(user__username=username)
        # 拿到该用户名的model对象，并拿到该用户关注的用户数量和粉丝数量
        user_obj = models.UserTable.objects.filter(username=username).first()
        care = user_obj.user_fans.filter().count()
        fans = user_obj.user_flower.filter().count()
        # select id,date_format(create_time,'%Y-%m') as ctime,count(id) from article group by date_format(create_time,'%Y-%m')"
        # 在python中写sql语句注意，"%Y-%m"需要写成"%%Y-%%m"
        ctime_list = models.Article.objects.raw('select id,date_format(create_time,"%%Y-%%m") as ctime,count(id) as c_d from article group by date_format(create_time,"%%Y-%%m")')
        return render(request,"personpage.html",locals())
    else:
        obj = VerifyBlogForm()
        return render(request,"login.html",{"obj": obj})


def personal_choose_page(request,username,option,id):
    """
    根据点击的标签，分类，时间选择对应的文章
    :param request:
    :param username: 用户名
    :param option: 选项，点击的是标签，分类还是时间
    :param id: 标签，分类的id
    :return: 用户主页面
    """
    if option == "tag":
        flag = models.Label.objects.filter(id=id).first()
        obj = models.Article.objects.filter(user__user__username=username,label=flag)
    elif option == "classification":
        flag = models.Classification.objects.filter(id=id).first()
        obj = models.Article.objects.filter(user__user__username=username,classification=flag)
    elif option == "ctime":
        obj = models.Article.objects.filter(user__user__username=username).extra(where=["date_format(create_time,'%%Y-%%m')= %s", ],params=[id,])
    tag = models.Label.objects.filter(user__username=username)
    classification = models.Classification.objects.filter(user__username=username)
    user_obj = models.UserTable.objects.filter(username=username).first()
    care = user_obj.user_fans.filter().count()
    fans = user_obj.user_flower.filter().count()
    ctime_list = models.Article.objects.raw(
        'select id,date_format(create_time,"%%Y-%%m") as ctime,count(id) as c_d from article group by date_format(create_time,"%%Y-%%m")')
    return render(request,"personal_choose_page.html",locals())


def article_page(request,*args,**kwargs):
    """
    文章最终页
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    # url中传递过来两值，1、用户名；2、用户的文章id
    username = kwargs["username"]
    id = kwargs["id"]
    # 根据文章id取得具体的文章详细内容，和这篇文章相关的评论，文章对象
    article = models.ArticleDetail.objects.filter(article__id=id).first()
    comment = models.CommentTable.objects.filter(article_id=id)
    article_obj = models.Article.objects.filter(user__user__username=username)
    return render(request,"article_page.html",locals())


def manage_edit(request,username,*args,**kwargs):
    tc_id = {}
    tc_id["tag_id"] = int(kwargs["tag_id"])
    tc_id["classification_id"] = int(kwargs["classification_id"])
    id_lable_class = {}
    if tc_id["tag_id"] != 0:
        id_lable_class["label_id"] = tc_id["tag_id"]
    if tc_id["classification_id"] != 0:
        id_lable_class["classification_id"] = tc_id["classification_id"]
    user_obj = models.UserTable.objects.filter(username=username).first()
    tag = models.Label.objects.filter(user__username=username)
    classification = models.Classification.objects.filter(user__username=username)
    article_obj = models.Article.objects.filter(user__user__username=username,**id_lable_class)
    current_page = 1
    total_number = article_obj.count()
    page_obj = pager.Pagination(total_number,current_page,13,5)
    page_obj.pageStr()
    # current_page = request.GET.get("p")
    # obj = Pagination(199,current_page,10,11)
    # user_l = user_list[obj.start():obj.end()]
    # obj.pageStr()
    return render(request,"manage_edit.html",locals())


def logoff(request):
    """
    注销，如果登录状态为true则清楚保存在session中的登录状态和用户名
    :param request:
    :return:
    """
    if request.session.get("is_login") == "true":
        del request.session["is_login"]
        del request.session["username"]
    return HttpResponse("ok")


def up_down(request,*args,**kwargs):
    """
    赞踩后，对数据库执行响应的操作.接收ajax发送过来的请求，返回data_send
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    username = request.session.get("username")
    data = {"status":"","up_count":0,"down_count":0}
    # 用户登录后才能对文章进行赞和踩，采用保存在session中，通过判断session来判断是否登录
    if username:
        article_id = request.GET.get("article_id")
        is_up = json.loads(request.GET.get("is_up"))
        article = models.Article.objects.filter(id=article_id).first()
        data["up_count"] = article.up_count
        data["down_count"] = article.down_count
        if article.user.user.username == username:
            # 用户名和文章的用户名相同，返回false，表示用户自己不能对自己的文章进行赞或者踩的操作
            return HttpResponse("false")
        user = models.UserTable.objects.filter(username=username).first()
        print(article_id, is_up)
        try:
            models.PraiseOrBelittleArticle.objects.create(article_id=article_id, value=is_up, user=user)
        except Exception as e:
            data["status"] = str(e)
            data_send = json.dumps(data)
            return HttpResponse(data_send)
        if is_up:
            article.up_count += 1
            article.save()
            data["up_count"] += 1
        else:
            article.down_count += 1
            article.save()
            data["down_count"] +=1
        data["status"] = "ok"
        data_send = json.dumps(data)
        return HttpResponse(data_send)
    else:
        # 用户没有登录时，也不能对文章进行赞或者踩
        data["status"] = "请先登录"
        data_send = json.dumps(data)
        return HttpResponse(data_send)


def process_comment(request):
    """
    对评论的处理，还差有父评论的情况
    :param request:
    :return:
    """
    article_id = request.POST.get("article_id")
    comment_value = request.POST.get("comment_value")
    username = request.session.get("username")
    user = models.UserTable.objects.filter(username=username).first()
    print(article_id,comment_value,username,user)
    models.CommentTable.objects.create(article_id=article_id,content=comment_value,user=user)
    return HttpResponse("ok")


def upload_pictures(request,*args,**kwargs):
    print(request.POST)
    print(request.FILES)
    print(args)
    print(kwargs)
    username = request.session.get("username")
    imgFile = request.FILES.get("imgFile")
    picture_name = imgFile.name
    print(picture_name)
    f = open("statics/pictures/%s/%s"%(username,picture_name),"wb+")
    for line in imgFile.chunks():
        f.write(line)
    f.close()
    dic_data = {
        'error': 0,
        'url': '/statics/pictures/%s/%s'%(username,picture_name),
        'message': '错误了...'
    }
    dic_data_send = json.dumps(dic_data)
    return HttpResponse(dic_data_send)


def edit_article(request,nid,*args,**kwargs):
    if request.method == "GET":
        article_obj = models.Article.objects.filter(id=nid).first()
        tag = models.Label.objects.all()
        classification = models.Classification.objects.all()
        return render(request,"edit_article.html",locals())
    else:
        print(request.POST.get("article_title"))
        print(request.POST.get("article_content"))
        username = request.session.get("username")
        article_title = request.POST.get("article_title")
        article_content = request.POST.get("article_content")
        tag_id = request.POST.get("inlineRadioOptions1")
        classification_id = request.POST.get("inlineRadioOptions2")
        obj_article = models.Article.objects.filter(id=nid).first()
        models.Article.objects.filter(id=nid).update(title=article_title,classification_id=classification_id,label_id=tag_id)
        models.ArticleDetail.objects.filter(article=obj_article).update(detail=article_content)
        return redirect("/%s/manage_edit-0-0/"%username)