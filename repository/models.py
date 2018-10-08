from django.db import models

# Create your models here.


class UserTable(models.Model):
    username = models.CharField(max_length=64,verbose_name="用户姓名")
    pwd = models.CharField(max_length=32,verbose_name="用户密码")
    email = models.EmailField(verbose_name="用户邮箱")
    img = models.ImageField(verbose_name="用户头像",upload_to="statics/userphoto")
    user_fans = models.ManyToManyField("UserTable",blank=True,related_name="user_flower")
    user_nickname = models.CharField(max_length=32,default=None)

    class Meta:
        db_table = "UserTable"
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.username


class BlogTable(models.Model):
    surfix = models.CharField(max_length=128)
    theme = models.CharField(max_length=32,verbose_name="博客主题")
    summary = models.CharField(max_length=128,verbose_name="博客简介")
    user = models.OneToOneField("UserTable",on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=128,default=None)

    class Meta:
        db_table = "BlogTable"
        verbose_name_plural = "博客表"

    def __str__(self):
        return self.surfix


class ReportTable(models.Model):
    choices = (
        (1,"待处理"),
        (2,"处理中"),
        (3,"已处理")
    )
    title = models.CharField(max_length=32,verbose_name="报障标题")
    user_report = models.ForeignKey("UserTable",on_delete=models.CASCADE,verbose_name="报障单提交用户",related_name="user_user_report")
    processor = models.ForeignKey("UserTable",on_delete=models.CASCADE,verbose_name="报障单处理用户",related_name="user_processor",default=None,null=True)
    status = models.IntegerField(choices=choices,verbose_name="处理状态",default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    solution_time = models.DateTimeField(null=True)
    content = models.TextField()
    solution = models.TextField(null=True)

    class Meta:
        db_table="ReportTable"
        verbose_name_plural = "报障表"

    def __str__(self):
        return self.title


class Classification(models.Model):
    caption = models.CharField(max_length=32)
    user = models.ForeignKey("UserTable",null=True,on_delete=models.CASCADE)

    class Meta:
        db_table = "Classification"
        verbose_name_plural = "分类"

    def __str__(self):
        return self.caption


class Label(models.Model):
    caption = models.CharField(max_length=32)
    user = models.ForeignKey("UserTable", null=True,on_delete=models.CASCADE)

    class Meta:
        db_table = "Label"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.caption


class Article(models.Model):
    title = models.CharField(max_length=32,verbose_name="文章标题")
    summary = models.CharField(max_length=128,verbose_name="文章简介",default="")
    user = models.ForeignKey("BlogTable",verbose_name="文章所在博客",on_delete=models.CASCADE)
    classification = models.ForeignKey("Classification",verbose_name="文章分类",on_delete=models.CASCADE)
    label = models.ForeignKey("Label",verbose_name="文章标签",on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True,null=True)
    comment_count = models.IntegerField(verbose_name="评论数",default=0)
    read_count = models.IntegerField(verbose_name="阅读数",default=0)
    up_count = models.IntegerField(verbose_name="点赞数",default=0)
    down_count = models.IntegerField(verbose_name="踩数",default=0)

    class Meta:
        db_table = "Article"
        verbose_name_plural = "文章"

    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    detail = models.TextField()
    article = models.OneToOneField("Article",on_delete=models.CASCADE,related_name="article_detail")

    class Meta:
        db_table = "ArticleDetail"
        verbose_name_plural = "文章详细内容"

    def __str__(self):
        return self.article


class PraiseOrBelittleArticle(models.Model):
    article = models.ForeignKey("Article",on_delete=models.CASCADE,related_name="up_down")
    user = models.ForeignKey("UserTable",on_delete=models.CASCADE)
    value = models.BooleanField()

    class Meta:
        db_table = "PraiseOrBelittleArticle"
        verbose_name_plural = "赞踩文章关系"
        unique_together = (("article","user"),)


class CommentTable(models.Model):
    """
    评论表，字段有：
    1、评论内容
    2、对哪篇文章的评论
    3、评论者是谁
    4、是否有父评论，null表示没有，自相关，
    5、评论时间
    """
    content = models.TextField()
    article = models.ForeignKey("Article",on_delete=models.CASCADE)
    user = models.ForeignKey("UserTable",on_delete=models.CASCADE)
    # 父评论和自己相关，为空表示没有父评论
    parent_comment = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,default=None)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "CommentTable"
        verbose_name_plural = "评论表"