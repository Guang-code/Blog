from django.db import models
from django.utils import timezone
from datetime import date

# 添加新的模块 """评论模型"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

class BlogUser(models.Model):
    """ 用户信息表 """
    # unique如果设置为True，这个字段必须在整个表中保持值唯一。
    # blank如果是 True ，该字段允许为空。默认为 False 。
    username = models.CharField(max_length=10, primary_key=True, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=15, null=False, verbose_name='密码')
    SEX_ITEMS = [
        (0, '女'),
        (1, '男'),
        (2, '未知')
    ]
    gender = models.CharField(max_length=1, choices=SEX_ITEMS, default='2', verbose_name='性别')
    career = models.CharField(max_length=30, null=True, verbose_name='职业')
    email = models.EmailField(null=False, verbose_name='邮箱')
    createTime = models.DateTimeField('创建时间',  default=timezone.now)

class Token(models.Model):
    username = models.OneToOneField(to=BlogUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True, verbose_name='token')

class Blog(models.Model):
    """ 博客创建信息表 """
    id = models.AutoField(primary_key=True, verbose_name='博客ID')
    title = models.CharField(max_length=255, null=False, verbose_name='博客标题')
    createtime = models.DateTimeField('创建时间',  default=timezone.now)
    # lable = models.CharField(max_length=20, null=False, verbose_name='博客标签')
    summary = models.TextField(null=False, verbose_name='博客简介')
    text = models.TextField(null=False, verbose_name='博客内容')
    username = models.ForeignKey("BlogUser", on_delete=models.CASCADE)
    admin = models.ForeignKey("Review", on_delete=models.CASCADE, null=True, blank=True)
    STATUS_ITEMS = [
        (0, '未通过'),
        (1, '通过'),
        (2, '审核中')
    ]
    status = models.CharField(max_length=1, choices=STATUS_ITEMS, default='2', verbose_name='博客状态')
    feedback = models.TextField(null=True, verbose_name='反馈内容')
    classification = models.ManyToManyField(to='Category', blank=True, related_name='blog')
    # comment_count = models.IntegerField(default=0, verbose_name='评论数量')


""" 点赞 不喜欢 收藏表 附属信息表 """
class Bloglike(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    like = models.BooleanField(default=False, verbose_name='点赞')
    dislike = models.BooleanField(default=False, verbose_name='点踩')
    collect = models.BooleanField(default=False, verbose_name='收藏')
    username = models.ForeignKey("BlogUser", on_delete=models.CASCADE, to_field='username', db_column='username_username')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

# 定义信号接收函数
@receiver(post_save, sender=Bloglike)
def update_attached(sender, instance, **kwargs):
    """
    每当有新的Bloglike记录被创建时，更新Attached表中对应博客的数据统计
    """
    blog = instance.blog
    attached, created = Attached.objects.get_or_create(blog=blog)
    # if instance.like:
    #     attached.like += 1
    # else:
    #     attached.like -= 1 if attached.like > 0 else 0
    # if instance.dislike:
    #     attached.dislike += 1
    # else:
    #     attached.dislike -= 1 if attached.dislike > 0 else 0
    # if instance.collect:
    #     attached.collect += 1
    # else:
    #     attached.collect -= 1 if attached.collect > 0 else 0
    # attached.save()
    # update_fields = kwargs.get('update_fields', set())
    #
    # if instance.like:
    #     attached.like += 1
    # elif 'like' in update_fields and attached.like > 0:
    #     attached.like -= 1
    #
    # if instance.dislike:
    #     attached.dislike += 1
    # elif 'dislike' in update_fields and attached.dislike > 0:
    #     attached.dislike -= 1
    #
    # if instance.collect:
    #     attached.collect += 1
    # elif 'collect' in update_fields and attached.collect > 0:
    #     attached.collect -= 1
    #
    # attached.save()
    # 获取传递了的参数
    update_fields = kwargs.get('update_fields', set())
    if instance.like:
        attached.like += 1
    elif update_fields and 'like' in update_fields and attached.like > 0:
        attached.like -= 1

    if instance.dislike:
        attached.dislike += 1
    elif update_fields and 'dislike' in update_fields and attached.dislike > 0:
        attached.dislike -= 1

    if instance.collect:
        attached.collect += 1
    elif update_fields and 'collect' in update_fields and attached.collect > 0:
        attached.collect -= 1

    attached.save()

class Category(models.Model):
    """分类表"""
    classification = models.AutoField(primary_key=True, verbose_name='分类ID', )
    title = models.CharField(max_length=10, null=False, unique=True, verbose_name='分类名称')
    STATUS_ITEMS = [
        (0, '未通过'),
        (1, '通过'),
        (2, '审核中')
    ]
    status = models.CharField(max_length=1, choices=STATUS_ITEMS, default=2, verbose_name='分类状态')
    createtime = models.DateTimeField('创建时间', default=timezone.now)


class Comment(models.Model):
    """评论模型"""
    id = models.AutoField(primary_key=True, verbose_name='评论ID')
    text = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='点赞数量')
    dislikes_count = models.PositiveIntegerField(default=0, verbose_name='不喜欢数量')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name='所属博客')
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name='评论用户')
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='父评论')
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies',
    #                                    verbose_name='父评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return f'评论ID: {self.id}'

# @receiver(post_save, sender=Comment)
# @receiver(post_delete, sender=Comment)
# def update_comment_count(sender, instance, **kwargs):
#     """更新博客的评论数量"""
#     blog = instance.blog
#     blog.comment_count = blog.comments.count()
#     blog.save()


class Review(models.Model):
    """ 管理员用户表 """
    admin = models.CharField(max_length=10, primary_key=True, verbose_name='审核员用户名')
    password = models.CharField(max_length=15, null=False, verbose_name='密码')
    name = models.CharField(max_length=20, null=False, verbose_name='姓名')


class Attached(models.Model):
    """ 可视化信息表 """
    attachid = models.AutoField(primary_key=True, verbose_name='附属ID')
    like = models.IntegerField(default=0, verbose_name='点赞')
    dislike = models.IntegerField(default=0, verbose_name='点踩')
    collect = models.IntegerField(default=0, verbose_name='收藏')
    comment = models.IntegerField(default=0, verbose_name='评论')
    blog = models.ForeignKey(to="Blog",on_delete=models.CASCADE, to_field='id', db_column='id_id')

# 定义信号接收函数
@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def update_attached_comment_count(sender, instance, **kwargs):
    """
    更新 Attached 模型中的评论数量
    """
    blog = instance.blog
    attached, _ = Attached.objects.get_or_create(blog=blog.id)
    attached.comment = blog.comments.count()
    attached.save()

