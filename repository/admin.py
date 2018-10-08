from django.contrib import admin
from repository import models
# Register your models here.

admin.site.register(models.UserTable)
admin.site.register(models.Article)
admin.site.register(models.Label)
admin.site.register(models.Classification)
admin.site.register(models.BlogTable)
admin.site.register(models.ArticleDetail)
admin.site.register(models.CommentTable)
admin.site.register(models.PraiseOrBelittleArticle)
admin.site.register(models.ReportTable)