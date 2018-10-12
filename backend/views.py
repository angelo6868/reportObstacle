from django.shortcuts import render,HttpResponse,redirect
from repository import models
from web import webForm
import uuid
import json
from django.db.models import Q
import datetime
# Create your views here.


def add_article(request,username):
    """
    创建文章，GET请求返回创建文章页面
    :param request:
    :param username:url中传递过来的用户名，当然登录后也可以从session中拿
    :return:
    """
    if request.method == "GET":
        # 在前端页面中，页面跳转的地址需要有用户名和用户对象
        user_obj = models.UserTable.objects.filter(username=username).first()
        # 需要选择文章标签和文章分类在前端页面显示，为radio类型,标签和分类为具体登录用户的标签和分类
        tag = models.Label.objects.filter(user__username=username)
        classification = models.Classification.objects.filter(user__username=username)
        return render(request,"add_article.html",locals())
    else:
        # 从表单中拿到文章的标题，内容，标签名和分类名
        condition = {}
        article_title = request.POST.get("article_title")
        condition["title"] = article_title
        article_content = request.POST.get("article_content")
        tag_id = request.POST.get("inlineRadioOptions1")
        if tag_id:
            condition["label_id"] = tag_id
        classification_id = request.POST.get("inlineRadioOptions2")
        if classification_id:
            condition["classification_id"] = classification_id
        print(tag_id,classification_id)
        # url中传递有用户名，不用获取了
        # username = request.session.get("username")
        user_blog = models.BlogTable.objects.filter(user__username=username).first()
        condition["user"] = user_blog
        print(condition)
        # 根据表单中输入的值，创建文章对象
        article_obj = models.Article.objects.create(**condition)
        # 创建文章详细对象
        models.ArticleDetail.objects.create(detail=article_content,article=article_obj)
        return redirect("/%s/backend/add-article/"%username)


def add_tag(request,username):
    """
    用户添加文章的标签
    :param request:
    :param username:
    :return:
    """
    # 共用的base模板中，需要传入用户对象，标签添加页面没有其他需要传入的变量了
    user_obj = models.UserTable.objects.filter(username=username).first()
    if request.method == "GET":
        return render(request,"add_tag.html",locals())
    else:
        # 拿到标签的名字，标签字段只有caption和自增的id
        caption = request.POST.get("caption")
        # 检测数据库中是否有和拿到的标签名重名,并且是同一个人的标签
        caption_num = models.Label.objects.filter(caption=caption,user__username=username).count()
        if not caption_num:
            # 没有，则在数据库中创建标签
            models.Label.objects.create(caption=caption,user=user_obj)
            return redirect("/%s/manage_tag/"%username)
        else:
            # 有重名的，则重新返回增加标签页面
            return render(request,"add_tag.html",locals())


def add_classification(request,username):
    """
    添加用户的分类，
    :param request:
    :param username:
    :return:
    """
    user_obj = models.UserTable.objects.filter(username=username).first()
    if request.method == "GET":
        return render(request,"add_classification.html",locals())
    else:
        caption = request.POST.get("caption")
        caption_num = models.Classification.objects.filter(caption=caption,user__username=username).count()
        if not caption_num:
            models.Classification.objects.create(caption=caption,user=user_obj)
            return redirect("/%s/manage_classification/"%username)
        else:
            return render(request,"add_classification.html",locals())


def add_obstacle(request,username):
    """
    创建报账单，先返回页面填写报障信息，再提交报障信息保存在数据库中
    :param request:
    :param username:
    :return:
    """
    if request.method == "GET":
        return render(request,"add_obstacle.html",locals())
    else:
        obstacle_title = request.POST.get("obstacle_title")
        obstacle_content = request.POST.get("obstacle_content")
        user_obj = models.UserTable.objects.filter(username=username).first()
        models.ReportTable.objects.create(title=obstacle_title,user_report=user_obj,content=obstacle_content)
        return redirect("/%s/manage_user_obstacle-3/"%username)


def edit_tag(request,nid):
    username = request.session.get("username")
    print(nid)
    if request.method == "GET":
        tag_obj = models.Label.objects.filter(id=nid).first()
        user_obj = models.UserTable.objects.filter(username=username).first()
        return render(request,"edit_tag.html",locals())
    else:
        caption = request.POST.get("caption")
        models.Label.objects.filter(id=nid).update(caption=caption)
        return redirect("/%s/manage_tag/"%username)


def edit_obstacle(request,nid):
    """
    报障单提交者编辑报障单，在报障单还未被接单时可以对报障单进行编辑
    :param request:
    :param nid:
    :return:
    """
    username = request.session.get("username")
    print(nid)
    if request.method == "GET":
        user_obj = models.UserTable.objects.filter(username=username).first()
        user_obstacle_obj = models.ReportTable.objects.filter(user_report=user_obj,id=nid,status=1).first()
        if not user_obstacle_obj:
            return HttpResponse("该报障单已被接单，无法重新编辑，如需提交报障，请重写报障单！")
        return render(request,"edit_obstacle.html",locals())
    else:
        obstacle_title = request.POST.get("obstacle_title")
        obstacle_content = request.POST.get("obstacle_content")
        user_obj = models.UserTable.objects.filter(username=username).first()
        models.ReportTable.objects.filter(id=nid).update(title=obstacle_title,content=obstacle_content)
        return redirect("/%s/manage_user_obstacle-3/"%username)


def check_obstacle(request,nid):
    """
    报障单提交者查看报障单
    :param request:
    :param nid:
    :return:
    """
    username = request.session.get("username")
    print(nid)
    if request.method == "GET":
        user_obj = models.UserTable.objects.filter(username=username).first()
        user_obstacle_obj = models.ReportTable.objects.filter(user_report=user_obj,id=nid).first()
        return render(request,"check_obstacle.html",locals())


def delete_obstacle(request,nid):
    models.ReportTable.objects.filter(id=nid).delete()
    username = request.session.get("username")
    return redirect("/%s/manage_user_obstacle-0/"%username)


def edit_classification(request,nid):
    username = request.session.get("username")
    if request.method == "GET":
        classification_obj = models.Classification.objects.filter(id=nid).first()
        user_obj = models.UserTable.objects.filter(username=username).first()
        return render(request,"edit_classification.html",locals())
    else:
        caption = request.POST.get("caption")
        models.Classification.objects.filter(id=nid).update(caption=caption)
        return redirect("/%s/manage_classification/"%username)


def delete_tag(request,nid):
    models.Label.objects.filter(id=nid).delete()
    username = request.session.get("username")
    return redirect("/%s/manage_tag/"%username)


def delete_classification(request,nid):
    models.Classification.objects.filter(id=nid).delete()
    username = request.session.get("username")
    return redirect("/%s/manage_classification/"%username)


def manage_tag(request,username):
    tag_obj = models.Label.objects.filter(user__username=username)
    user_obj = models.UserTable.objects.filter(username=username).first()
    return render(request,"manage_tag.html",locals())


def manage_classification(request,username):
    classification_obj = models.Classification.objects.filter(user__username=username)
    user_obj = models.UserTable.objects.filter(username=username).first()
    return render(request,"manage_classification.html",locals())


def manage_user_info(request,username):
    if request.method == "GET":
        user_info_obj = webForm.UserInfoForm(username)
        user_obj = models.UserTable.objects.filter(username=username).first()
        return render(request,"manage_user_info.html",locals())
    else:
        print(request.POST)
        url_username = username
        user_info_obj = webForm.UserInfoForm(username,request.POST)
        if user_info_obj.is_valid():
            print(user_info_obj.cleaned_data)
            user_dict = {}
            blog_title_dict = {}
            if user_info_obj.cleaned_data["username"]:
                user_dict["username"] = user_info_obj.cleaned_data["username"]
                url_username = user_info_obj.cleaned_data["username"]
            if user_info_obj.cleaned_data["email"]:
                user_dict["email"] = user_info_obj.cleaned_data["email"]
            if user_info_obj.cleaned_data["user_nickname"]:
                user_dict["user_nickname"] = user_info_obj.cleaned_data["user_nickname"]
            if user_info_obj.cleaned_data["blog_title"]:
                blog_title_dict["blog_title"] = user_info_obj.cleaned_data["blog_title"]
            print("user_dict",user_dict)
            models.UserTable.objects.filter(username=username).update(**user_dict)
            models.BlogTable.objects.filter(user__username=username).update(**blog_title_dict)
            request.session["username"] = url_username
            return redirect("/%s/manage_user_info/"%url_username)
        else:
            print(user_info_obj.errors)
            return HttpResponse("出错了")


def manage_user_obstacle(request,username,*args,**kwargs):
    """
    普通用户管理报障单页面
    :param request:
    :param username: 用户名
    :return:
    """
    if request.method == "GET":
        condition = {}
        # status为选择状态，1待处理，2处理中，3已处理，传到前端显示到页面上
        status = models.ReportTable.choices
        # status_id为根据url拿到的选择相应状态的id值,0为全部
        status_id = int(kwargs['status_id'])
        user_obj = models.UserTable.objects.filter(username=username).first()
        # 往筛选条件condition中填充值，筛选出符合条件的报障单
        condition["user_report"] = user_obj
        if status_id:
            condition["status"] = status_id
        user_obstacle_obj = models.ReportTable.objects.filter(**condition)
        return render(request,"manage_user_obstacle.html",locals())


def upload_avatar(request,username):
    """
    上传用户的头像
    在前端采用的方式是，伪ajax的方式，即iframe加form表单的形式
    :param request: 提交过来的请求对象，在Files中有文件
    :param username: 操作者的用户名，用于保存提交的图片文件创建文件名。
    :return:
    """
    # 引入uuid确保传入文件的文件名的唯一性
    nid = str(uuid.uuid4())
    data = {"status": "","index":None}
    avatar_obj = request.FILES.get("avatar_img")
    file_name = nid + avatar_obj.name
    print(avatar_obj.name)
    print(file_name)
    f = open("statics/userphoto/%s"%file_name,"wb")
    for line in avatar_obj.chunks():
        f.write(line)
    f.close()
    # 更改存在用户表中，用户图片的路径
    models.UserTable.objects.filter(username=username).update(img="statics/userphoto/%s"%file_name)
    data["index"] = "/statics/userphoto/%s"%file_name
    data_send = json.dumps(data)
    return HttpResponse(data_send)


def handel_obstacle_list(request,nid):
    """
    报障单处理者；返回报障单列表,首先拿到报障列表，分类为1、全部；2、未处理；3、处理中；4、已处理
    未处理看到所有人没有被处理的报障单；
    处理中是自己接单的报障单
    已处理是自己已经处理的报障单
    :param request:
    :param nid:分类选择的标志0-全部；1-未处理；2-处理中；3-已处理
    :return:
    """
    status_id = int(nid)
    # 拿到登陆者的用户名和用户对象
    username = request.session.get("username")
    user_obj = models.UserTable.objects.filter(username=username).first()
    if not status_id:
        # status_id=0表示查看所有情况的报障单，处理者是自己的包括已处理和处理中的，或者报障单状态为未处理的情况
        obstacle_obj = models.ReportTable.objects.filter(Q(processor__username=username) | Q(status=1) )
    elif status_id == 3:
        # status_id == 3表示查看已处理的报障单，需要两个限制条件，1、处理者是自己；2、状态为已处理
        obstacle_obj = models.ReportTable.objects.filter(processor__username=username,status=status_id)
    elif status_id == 2:
        # status_id == 2表示查看处理中的报障单，需要两个限制条件，1、处理者是自己；2、状态为处理中
        obstacle_obj = models.ReportTable.objects.filter(processor__username=username,status=status_id)
    else:
        # 剩下status_id == 1的情况，表示查看所有未处理的报障单
        obstacle_obj = models.ReportTable.objects.filter(status=status_id)
    # status传到前端，为搜索报障单的4个条件
    status = models.ReportTable.choices
    return render(request,"handel_obstacle_list.html",locals())


def handel_obstacle(request,nid):
    """
    在handel_obstacle_list.html页面中点击查看，进入到该view函数，查看报障单的具体报障内容
    处理者查看报障单的内容，确定自己能否处理，以决定是否接单或者取消接单
    :param request:
    :param nid:url传递过来的报障单的id号，id在数据库中为主键，自增，唯一的，因此查看时，根据该id查看点击的唯一报障单
    :return:
    """
    username = request.session.get("username")
    if request.method == "GET":
        user_obj = models.UserTable.objects.filter(username=username).first()
        user_obstacle_obj = models.ReportTable.objects.filter(id=nid).first()
        return render(request,"handel_obstacle.html",locals())


def handel_obstacle_solution(request,nid):
    """
    处理者点击页面上的处理，进入到具体的报障单页面中，查看报障信息并填写报障的解决方案，提交解决方案的内容。
    进入后，只能对还是处理中的报障单进行解决方案的填写
    :param request:
    :param nid:
    :return:
    """
    username = request.session.get("username")
    user_obj = models.UserTable.objects.filter(username=username).first()
    if request.method == "GET":
        # 只能拿到该报障单处于处理中的状态，否则什么也拿不到，前端应限制点击
        user_obstacle_obj = models.ReportTable.objects.filter(id=nid,status=2).first()
        return render(request,"handel_solution_obstacle.html",locals())
    else:
        solution = request.POST.get("obstacle_solution")
        solution_time = datetime.datetime.now()
        print("solution_time",solution_time)
        models.ReportTable.objects.filter(id=nid,status=2).update(status=3,solution=solution,processor=user_obj,solution_time=solution_time)
        return redirect("/backend/handel_user_obstacle-0/")


def handel_obstacle_add(request,nid):
    username = request.session.get("username")
    user_solution_obj = models.UserTable.objects.filter(username=username).first()
    models.ReportTable.objects.filter(status=1,id=nid).update(status=2,processor=user_solution_obj)
    return redirect("/backend/handel_user_obstacle-0/")