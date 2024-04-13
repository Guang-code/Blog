from django.shortcuts import render

# Create your views here.

from django.shortcuts import HttpResponse, redirect
from django.core.serializers import serialize
import json

from . import models
from django.http import JsonResponse
# 导入 Django 的聚合函数
from django.db.models import Count
# blog中有个外键字段它无法被json化 所以导入下面的
from django.forms.models import model_to_dict
# token的编写
from django.views import View

from .models import Bloglike
# 分页器
from django.core.paginator import Paginator, EmptyPage
# 删除操作
from django.db import transaction
# 导入聚合函数
from django.db.models import Count
# 导入F函数
from django.db.models import F
# 导入redis相关宝
from django.core.cache import cache

"""
Django REST Framework（简称DRF）是一个基于 Django 的强大框架，用于构建 Web API。它提供了一整套工具和库，
帮助开发者轻松地构建和管理Web API，包括序列化、验证、视图、路由、认证、权限控制、文档生成等功能。
"""
# 参考 https://www.django-rest-framework.org/
# 这行代码意味着您正在从 Django REST Framework 中导入 APIView 类，以便创建自定义的 API 视图类。
from rest_framework.decorators import APIView

"""
BaseAuthentication 是 Django REST Framework 中用于实现认证机制的基础类。通过继承 BaseAuthentication 类，并实现其中的 authenticate 方法，可以自定义认证逻辑。
这样，可以在 Django REST Framework 中实现各种认证方式，比如基于令牌、基于 session 的认证等。
"""
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from functools import wraps


def auth(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if 'HTTP_TOKEN' in request.META:
            token = request.META['HTTP_TOKEN'][7:]
        elif 'HTTP_AUTHORIZATION' in request.META:
            token = request.META['HTTP_AUTHORIZATION'][7:]
        else:
            return JsonResponse({'status': 401, 'message': '缺少token'}, status=401)
        if token:
            token_obj = models.Token.objects.filter(token=token).first()
            if token_obj:
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({'status': 401, 'message': '没有查找到对应的token'}, safe=False)
        else:
            print(request.META)
            return JsonResponse({'status': 403, 'message': "没有权限访问"}, status=401, safe=False)

    return wrapper


@auth
def login(request):
    if request.method == "GET":
        return JsonResponse({'status': 200, 'message': "访问成功"}, safe=False)
    return JsonResponse({'status': 400, 'message': "请求参数错误"}, safe=False)


class testView(View):
    def get(self, request):
        return HttpResponse('222')


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print(123)
        token = request.query_params.get('token')
        token_obj = models.Token.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('auth failure!')
        return (token_obj.username.username, None)


class AuthView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {
            'code': 1000,
            'msg': 'None'
        }
        # user=request._request.POST.get('user')
        try:
            user = request.data.get('username')
            pwd = request.data.get('password')
            user_obj = models.BlogUser.objects.filter(username=user, password=pwd).first()
            if not user_obj:
                ret['code'] = 1001
                ret['msg'] = 'user or pwd erroe!'
            else:
                import hashlib
                m = hashlib.md5(bytes(user, 'utf-8'))
                import time
                ctime = str(time.time())
                m.update(bytes(ctime, encoding='utf-8'))
                # hexdigest()将计算出的 MD5 散列值转换为十六进制字符串表示。
                token = m.hexdigest()
                models.Token.objects.update_or_create(username=user_obj, defaults={'token': token})
                print(token)
                ret['code'] = 200
                ret['msg'] = 'auth success'
        except:
            ret['code'] = 1001
            ret['msg'] = 'user or pwd erroe!'

        return JsonResponse(ret)


class OrderView(APIView):
    authentication_classes = [MyAuthentication, ]

    def get(self, request, *args, **kwargs):
        print(123)
        ret = {
            'code': 1000,
            'msg': None,
        }
        ret['data'] = {
            1: {
                'name': 'apple',
                'price': 12.3
            },
            2: {
                'name': 'banana',
                'price': 29.9
            }
        }
        print(ret)
        return JsonResponse(ret)


def bloguser(request):
    """ 用户信息添加API,获取POST请求中的信息添加到数据库 """
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        username = request.POST.get("username")
        res = models.BlogUser.objects.filter(username=username)
        print(res)
        if res.exists():
            return JsonResponse({'message': "账号已注册", 'status': False}, safe=False)
        else:
            password = request.POST.get("password")
            career = request.POST.get("career")
            email = request.POST.get("email")
            user = models.BlogUser.objects.create(username=username, password=password, career=career, email=email)
            user.save()
            res = models.BlogUser.objects.filter(username=username)
            serialized_data = [{'username': item.username, 'password': item.password, 'gender': item.gender,
                                'career': item.career, 'email': item.email, 'createTime': item.createTime}
                               for item in res]
            return JsonResponse({'status': True, 'message': "注册成功", 'data': serialized_data}, safe=False)


def bloguser_delete(request):
    """ 用户信息删除 """
    username = request.POST.get("username")
    models.BlogUser.objects.filter(pk=username).delete()


def bloguser_update(request):
    """ 用户信息修改 """
    username = request.POST.get("username")
    password = request.POST.get("password")
    gender = request.POST.get("gender")
    career = request.POST.get("career")
    email = request.POST.get("email")
    models.BlogUser.objects.filter(username=username).update(password=password, gender=gender, career=career,
                                                             email=email)


def bloguser_search(request):
    """ 用户信息查询 """
    ret = {
        'code': 1000,
        'msg': 'None'
    }
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        print(request.POST)
        print("这是body", request.body)
        username = request.POST.get("username")
        password = request.POST.get("password")

        # res = models.BlogUser.objects.filter(username=username)
        # user_obj 这是一个对象
        user_obj = models.BlogUser.objects.filter(username=username, password=password).first()
        print(user_obj)

        # if res is not None:
        #     print("这是res", res)
        #     for obj in res:
        #         if obj.password == password:
        #             print(obj.password)
        #             serialized_data = [{'username': item.username, 'password': item.password, 'gender': item.gender,
        #                                 'career': item.career, 'email': item.email, 'createTime': item.createTime}
        #                                for item in res]
        #             print("这是循环后的数据", serialized_data)
        #             return JsonResponse({'status': True, 'data': serialized_data}, safe=False)
        if not user_obj:
            ret['code'] = 1001
            ret['msg'] = 'user or pwd erroe!'
        else:
            import hashlib
            m = hashlib.md5(bytes(username, 'utf-8'))
            import time
            ctime = str(time.time())
            m.update(bytes(ctime, encoding='utf-8'))
            # hexdigest()将计算出的 MD5 散列值转换为十六进制字符串表示。
            token = m.hexdigest()
            models.Token.objects.update_or_create(username=user_obj, defaults={'token': token})
            print(token)
            ret['code'] = 200
            ret['msg'] = 'auth success'
            serialized_data = [
                {'username': user_obj.username, 'password': user_obj.password, 'gender': user_obj.gender,
                 'career': user_obj.career, 'email': user_obj.email, 'createTime': user_obj.createTime}
            ]
            # serialized_data = [{'username': item.username, 'password': item.password, 'gender': item.gender,
            #                                  'career': item.career, 'email': item.email, 'createTime': item.createTime}
            #                                 for item in user_obj]
            return JsonResponse({'status': True, 'token': token, 'data': serialized_data}, safe=False)
        return JsonResponse(ret, safe=False)


@auth
# 博客信息添加API，获取POST请求中的信息添加到数据库
def bloginfo(request):
    """ 博客信息添加API，获取POST请求中的信息添加到数据库 """
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        print(request.POST)
        title = request.POST.get("title")
        summary = request.POST.get("summary")
        text = request.POST.get("text")
        # 将 GBK 编码的字符转换为 UTF-8 编码
        username = request.POST.get("username")
        classification = request.POST.get("classification")
        user = models.BlogUser.objects.filter(username=username).first()
        classification = json.loads(classification)
        print(classification, type(classification))

        # classifications = request.POST.getlist('classification')
        # print(request.POST.getlist('classification'))
        def add_tags_to_blog(blog, classification):
            # classification = tuple(classification)
            # print(type(classification))
            for tag in classification:
                print(tag)
                tag, created = models.Category.objects.get_or_create(title=tag)
                print(tag)
                if created:
                    print(f"标签{tag}不存在，已创建")
                blog.classification.add(tag)

        # 创建博客实例
        blog = models.Blog.objects.create(title=title, summary=summary, text=text, username=user)
        add_tags_to_blog(blog, classification)
        blog.save()
        # for item in classification:
        #     if item in models.Category.objects.all():
        #     tag = models.Category.objects.create(title=item)
        #     blog.tags.add(tag)
        return JsonResponse({'status': True, 'message': "博客添加成功"}, safe=False)

# 博客信息删除
@transaction.atomic
def bloginfo_delete(request):
    """ 博客信息删除 """
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        print(request.POST)
        # blog_id = request.POST.get("blog_id")
    try:
        blog = models.Blog.objects.get(id=request.POST.get("blog_id"))
        # 删除与博客相关的评论
        blog.comments.all().delete()
        # 删除与博客相关的附属信息
        models.Attached.objects.filter(blog=blog).delete()
        # 删除博客本身
        blog.delete()

        return JsonResponse({'status': True, 'message': "博客删除成功"}, status=204, safe=False)
    except models.Blog.DoesNotExist:
        return JsonResponse({'status': False, 'message': "博客删除成功"}, status=404, safe=False)
    except Exception as e:
        return False, str(e)


def bloginfo_update(request):
    """ 博客信息更新 """
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        title = request.POST.get("title")
        summary = request.POST.get("summary")
        text = request.POST.get("text")
        username = request.POST.get("username")
        classification = request.POST.get("classification")
        user = models.BlogUser.objects.filter(username=username).first()
        classification = json.loads(classification)

        # 获取博客ID，用于判断是添加还是修改
        blog_id = request.POST.get("blog_id")

        if blog_id:
            # 如果有博客ID，则是修改操作
            blog = models.Blog.objects.filter(id=blog_id).first()
            if not blog:
                return JsonResponse({'status': False, 'message': "博客不存在"}, safe=False)

            # 更新博客信息
            blog.title = title
            blog.summary = summary
            blog.text = text
            blog.username = user
            blog.classification.clear()  # 清除原有分类信息
            add_tags_to_blog(blog, classification)  # 添加新的分类信息
            blog.save()
            return JsonResponse({'status': True, 'message': "博客修改成功"}, safe=False)
        else:
            # 没有博客ID，则是添加操作
            blog = models.Blog.objects.create(title=title, summary=summary, text=text, username=user)
            add_tags_to_blog(blog, classification)
            return JsonResponse({'status': True, 'message': "博客添加成功"}, safe=False)


def add_tags_to_blog(blog, classification):
    """将分类信息添加到博客中"""
    for tag in classification:
        tag_obj, created = models.Category.objects.get_or_create(title=tag)
        if created:
            print(f"标签{tag_obj}不存在，已创建")
        blog.classification.add(tag_obj)

# 采用了 redis
# """ 博客信息查询 在首页展示 """
def bloginfo_search(request):
    """ 博客信息查询 在首页展示 """
    if request.method == "GET":
        # 判断Redis中是否有缓存数据
        redis_key = 'attached'
        redis_value = cache.get(redis_key)
        # object_list = None
        # if redis_value and len(redis_value) > 0:
        #     #     object_list = redis_value
        #     return JsonResponse({'status': True, 'data': redis_value,'msg':'这是来自redis的数据'}, safe=False)
        # else:
        attached_records = models.Attached.objects.filter(like__gt=1)
        top_blogs_ids = [attached_record.blog for attached_record in attached_records]
        # 从 top_blogs_ids 中提取每个 Blog 对象的 id
        top_blogs_ids = [blog.id for blog in top_blogs_ids]
        # 获取这些博客对象
        top_blogs = models.Blog.objects.filter(id__in=top_blogs_ids)
        print(top_blogs)
        # 构建博客数据列表，同时获取每个博客的所有相关标签信息
        blogs_data = []
        for blog in top_blogs:
            # 获取博客对象的所有标签信息
            labels = blog.classification.all()
            labels_data = [{'classification': label.classification, 'name': label.title} for label in labels]
            # 获取博客对象对应的用户信息，并转换为字典格式
            user_data = blog.username.username
            # user_data = model_to_dict(blog.username)
            # 构建博客数据字典
            blog_data = {
                'id': blog.id, 'title': blog.title,
                'createtime': blog.createtime, 'text': blog.text,
                'summary': blog.summary, 'username': user_data,
                # 其他字段
                'labels': labels_data
            }
            blogs_data.append(blog_data)

            # 将数据放入Redis缓存
            # cache.set(redis_key, blogs_data)

        return JsonResponse({'status': True, 'data': blogs_data}, safe=False)

    return JsonResponse({'status': False, 'message': '没有找到内容'}, safe=False)


# """ 查询该博客的所有信息 """
@auth
def bloginfo_search_all(request):
    """ 查询该博客的所有信息 """
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        # 获取请求体中的原始数据
        # decode将字节序列变量 将其解码为Unicode字符串：
        # body_unicode = request.body.decode('utf-8')
        # 解析JSON数据 将JSON字符串解析为Python对象
        # body_data = json.loads(body_unicode)
        # print(body_data,type(body_data))
        id = request.POST.get("id")
        # print(id, type(id))
        if not id:
            return HttpResponse("缺少必要的ID参数")
        id = int(id)
        blog_with_labels = models.Blog.objects.filter(pk=id).first()
        if blog_with_labels:
            # print(blog_with_labels)
            # serialize() 方法将数据进行json化，JsonResponse也会将一个数据进行json化
            serialized_blog = serialize('json', [
                blog_with_labels])  # , fields=('title', 'createtime', 'summary', 'text', 'username', 'classification')
            return JsonResponse({'status': 201, 'data': serialized_blog}, safe=False)
        else:
            return JsonResponse({'status': 404, 'data': "没有查找到该对象"}, safe=False)


# 根据主键查找blog的所有信息
@auth
def blog_id_search(request):
    if request.method == "GET":
        return HttpResponse("重新请求")
    elif request.method == "POST":
        id = request.POST.get('id')
        abc = models.Blog.objects.filter(pk=int(id)).first()
        print(abc.id, abc.title)
        return JsonResponse({'status': 201, 'data': "成功"})


def bloginfo_feedback(request):
    """ 博客审核信息 """
    id = request.POST.get("id")
    status = request.POST.get("status")
    feedback = request.POST.get("feedback")
    models.Blog.objects.filter(id=id).update(status=status, feedback=feedback)


def category(request):
    """ 分类标签添加 """
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        title = request.POST.get("title")
        status = request.POST.get("status")
        category = models.Category.objects.create(title=title, status=status)
        category.save()
        return JsonResponse({'status': True, 'message': "标签添加成功"}, safe=False)


def category_delete(request):
    """ 分类标签删除 """
    classification = request.POST.get("classification")
    category = models.Category.objects.filter(pk=classification)
    category.delete()
    return JsonResponse({'status': True, 'message': "标签删除成功"}, safe=False)


def category_update(request):
    """ 分类标签更新 """
    classification = request.POST.get("classification")
    title = request.POST.get("title")
    status = request.POST.get("status")
    models.Category.objects.filter(classification=classification).update(title=title, status=status)


# """ 单个分类标签查询 """
def category_search(request):
    """ 单个分类标签查询 """
    classification = request.POST.get("classification")
    res = models.Category.objects.filter(classification=classification).values('classification', 'title', 'status',
                                                                               'create_time')
    return JsonResponse({'status': True, 'data': list(res)})


def category_title_all(request):
    """展示所有标签的标题"""
    res = models.Category.objects.all()
    serialized_data = [{'title': item.title} for item in res]
    # for obj in res:
    #     print(obj.classification, obj.title, obj.status, obj.create_time)
    return JsonResponse({'status': True, 'data': serialized_data}, safe=False)
    # return JsonResponse({'status': True, 'data': list(serialized_data)}, safe=False)
    # return JsonResponse(serialized_data, safe=False)


def category_detail(request):
    """展示所有标签的详细信息"""
    res = models.Category.objects.all()[:15]
    serialized_data = [{'classification': item.classification, 'title': item.title} for
                       item in res]
    return JsonResponse({'status': 200, 'data': serialized_data}, safe=False)
    # return JsonResponse({'status': True, 'data': list(serialized_data)}, safe=False)
    # return JsonResponse(serialized_data, safe=False)


# 根据标签的名字搜索所有博客
def category_blog_all(request):
    """根据标签的名字搜索所有博客"""
    if request.method == 'POST':
        print(request.POST)
        try:
            title = request.POST.get("title")
            # 获取标签对象
            label = models.Category.objects.get(title=title)
            # 使用反向关联查询获取拥有该标签的所有博客
            blogs = label.blog_set.all()[:15]
            # 将查询到的博客信息转换为字典列表
            blogs_data = [{'id': blog.id, 'title': blog.title} for blog in blogs]
            return JsonResponse({'status': True, 'data': blogs_data}, safe=False)
        except models.Category.DoesNotExist:
            return JsonResponse({'error': 'Label not found'}, status=404)
    else:
        return JsonResponse({'error': 'Label not found', 'msg': '访问方式错误'}, safe=False)


# 根据标签名字进行模糊查询
def category_blog_mohu_all(request):
    try:
        title = request.GET.get("title")
        # 使用 __icontains 查询条件进行模糊匹配
        labels = models.Category.objects.filter(name__icontains=title)
        # 获取拥有匹配标签的所有博客
        blogs_data = []
        for label in labels:
            # 使用反向关联查询获取拥有该标签的所有博客 前15个
            blogs = label.blog_set.all()[:15]
            # 将查询到的博客信息转换为字典列表 'title', 'createtime', 'summary', 'username', 'classification'
            blogs_data += [{'id': blog.id, 'title': blog.title, 'createtime': blog.createtime, 'summary': blog.summary,
                            'username': blog.username, 'classification': blog.classification} for blog in blogs]

        return JsonResponse({'blogs': blogs_data})
    except models.Category.DoesNotExist:
        return JsonResponse({'error': 'Label not found'}, status=404, safe=False)

# 使用了   redis数据库
# 根据attached的id字段，修改点赞等数据
@auth
def attached_update(request):
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        # print(request.POST)
        # print(request.body)
        data = request.body.decode('utf-8')
        print(data)
        data = json.loads(data)
        blog_id = int(data.get('id'))
        like = int(data.get('like', int(0)))
        dislike = int(data.get('dislike', int(0)))
        attached_obj = models.Attached.objects.filter(id__id=blog_id).first()
        if attached_obj:
            attached_obj.like = attached_obj.like + like
            print(attached_obj.like, type(attached_obj.like))
            if attached_obj.dislike is None:
                attached_obj.dislike = 0
            print(attached_obj.dislike, dislike)
            attached_obj.dislike = attached_obj.dislike + dislike
            attached_obj.save()
            # print('向后端发送点赞请求', request.body)

            #清楚redis缓存信息,前置条件是like值大于某个数字
            # if attached_obj.like > 5:
            #     redis_keys = cache.keys('attached*')
            #     for k in redis_keys:
            #         cache.delete(k)
            return JsonResponse({'status': True, 'success': "成功"}, status=200, safe=False)
        else:
            return JsonResponse({'status': False, 'msg': "没有查找到该对象"}, status=404, safe=False)
    return HttpResponse("请使用正确的请求方式")


# 根据博客id获取点赞等相关信息
@auth
def attached_search(request):
    # if request.method == "GET":
    #     return HttpResponse("重新登录")
    # elif request.method == "POST":
    #     blog_id = request.POST.get("id")
    #     # 根据 blog_id 获取对应的 Attached 实例
    #     attached_instance = models.Attached.objects.filter(id=blog_id).first()
    #     if attached_instance:
    #         serialized_data = serialize('json', [
    #             attached_instance])
    #         return JsonResponse({'status': True, 'data': serialized_data}, safe=False)
    #     return JsonResponse({'status': 404, 'message': "没有找到"}, safe=False)
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        # print(request.body)
        # print(request.POST)
        id = request.POST.get("id")
        id = int(id)
        # 根据 id 获取对应的 Attached 实例
        attached_instance = models.Attached.objects.filter(blog=id).first()
        # print(attached_instance)
        if attached_instance:
            # 获取关联的博客实例
            blog_instance = attached_instance.blog
            # 获取点赞等相关信息
            serialized_attached_data = serialize('json', [attached_instance])
            # 获取所有标签信息
            classifications = blog_instance.classification.all()
            classification_list = [{'title': classification.title} for classification in classifications]

            # 构建完整的 JSON 数据
            response_data = {
                'status': True,
                'attached_data': serialized_attached_data,
                'classification_data': classification_list
            }

            return JsonResponse(response_data, status=200, safe=False)

        return JsonResponse({'status': 404, 'message': "没有找到"}, status=404, safe=False)


@auth
# 更具博客id获取所有的标签
def attached_search_category(request):
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        blog_id = request.POST.get("id")
        blog_instance = models.Blog.objects.get(id=blog_id)
        classifications = blog_instance.classification.all()
        print(classifications)
        # 将分类信息转换为 JSON 格式
        classification_list = [{'title': classification.title} for classification in classifications]

        # 构建 JSON 响应数据
        # response_data = {'classifications': classification_list}
        return JsonResponse({'status': True, 'data': classification_list}, safe=False)
    return JsonResponse({'status': 404, 'message': "没有找到"}, safe=False)


# 根据用户名和博客ID查找该用户在此博客的点赞等记录
@auth
def search_bloglike(request):
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        blog_id = request.POST.get("blog_id")
        username = request.POST.get("username")
        bloglike = models.Bloglike.objects.filter(username=username, blog=blog_id).first()
        if bloglike:
            print(bloglike)
            data = [
                {'id': bloglike.id, 'like': bloglike.like, 'dislike': bloglike.dislike,
                 'collect': bloglike.collect}
            ]
            # data = serialize('json', [bloglike],)
            return JsonResponse({'status': True, 'data': data}, status=200, safe=False)
        else:
            return JsonResponse({'status': False, 'data': '数据不存在'}, status=404, safe=False)


@auth
# 根据博客id和username外键 添加点赞等信息
def bloglike(request):
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        # print(request.POST)
        blog_id = request.POST.get("blog_id")
        username = request.POST.get("username")
        # 获取或创建 BlogUser 实例
        blog_instance, created = models.Blog.objects.get_or_create(id=blog_id)
        user_instance, created = models.BlogUser.objects.get_or_create(username=username)  # 假设用户名是唯一的
        # 获取现有的 Bloglike 实例（如果存在）
        bloglike_obj, created = models.Bloglike.objects.get_or_create(
            blog=blog_instance, username=user_instance
        )
        # 更新传递了的参数
        if "like" in request.POST:
            bloglike_obj.like = int(request.POST["like"])
        if "dislike" in request.POST:
            bloglike_obj.dislike = int(request.POST["dislike"])
        if "collect" in request.POST:
            bloglike_obj.collect = int(request.POST["collect"])
        # 保存更新后的实例
        bloglike_obj.save()
        # like = int(request.POST.get("like", 0))
        # dislike = int(request.POST.get("dislike", 0))
        # save_flag = int(request.POST.get("collect", 0))
        # 创建attached表信息
        # attached_obj, created = models.Attached.objects.get_or_create(blog=blog_id)
        # print(attached_obj)

        # bloglike_obj, created = models.Bloglike.objects.update_or_create(
        #     blog=blog_instance, username=user_instance,
        #     defaults={ 'like': like, 'dislike': dislike, 'collect': save_flag }
        # )
        # print(bloglike_obj)

        return JsonResponse({'status': True, 'data': "创建数据成功"}, status=201, safe=False)
        # else:
        # return JsonResponse({'status': True, 'data': '数据更新成功'}, status=200, safe=False)


@auth
# comment父评论和子评论的添加
def comment(request):
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        print(request.POST)
        blog_id = request.POST.get("blog_id")
        username = request.POST.get("username")
        # 获取或创建 BlogUser 实例
        blog_instance = models.Blog.objects.get(id=blog_id)
        user_instance = models.BlogUser.objects.get(username=username)  # 假设用户名是唯一的
        # 获取现有的 Bloglike 实例（如果存在）
        # blogcomment_obj, created = models.Comment.objects.get_or_create(
        #     blog=blog_instance, user=user_instance
        # )
        # 检查该用户在该博客下是否已经存在评论
        existing_comment = models.Comment.objects.filter(blog=blog_instance, user=user_instance).first()
        if existing_comment:
            # 如果存在评论，但用户要添加新的评论
            new_comment = models.Comment.objects.create(
                blog=blog_instance,
                user=user_instance,
                text=request.POST.get("text")
            )
            if "parent_comment" in request.POST:
                parent_obj = models.Comment.objects.get(id=int(request.POST["parent_comment"]))
                new_comment.parent_comment = parent_obj
            new_comment.save()
        else:
            # 如果不存在评论，则创建新的评论
            new_comment = models.Comment.objects.create(
                blog=blog_instance,
                user=user_instance,
                text=request.POST.get("text")
            )
            if "parent_comment" in request.POST:
                parent_obj = models.Comment.objects.get(id=int(request.POST["parent_comment"]))
                new_comment.parent_comment = parent_obj
            new_comment.save()

        # if "parent_comment" in request.POST:
        #     blogcomment_obj.parent_comment = int(request.POST["parent_comment"])
        # blogcomment_obj.text = request.POST.get("text")
        # blogcomment_obj.save()
        return JsonResponse({'status': True, 'data': "创建数据成功"}, status=201, safe=False)


@auth
# 查询所有的一级评论
def comment_search(request):
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        print('这是请求的数据111', request.POST)
        blog_id = request.POST.get("blog_id")
        if blog_id is None:
            return JsonResponse({'status': False, 'data': "未提供有效id"}, status=400, safe=False)
        # 获取或创建 BlogUser 实例
        try:
            blog_instance = models.Blog.objects.get(id=blog_id)
        except models.Blog.DoesNotExist:
            return JsonResponse({'status': False, 'message': '未找到匹配的博客'}, status=404, safe=False)

        #     print('这是博客实例', blog_instance)
        #     comment_instance = models.Comment.objects.filter(blog=blog_instance).all()
        #     print(comment_instance)
        #     # data = serialize('json', [comment_instance])
        #     data = [
        #         {'id': obj.id, 'text': obj.text, 'created_at': obj.created_at, 'user': obj.user.username, 'parent_comment': obj.parent_comment} for obj in comment_instance
        #     ]
        #     print(data)
        #     return JsonResponse({'status': True, 'data': data}, status=200, safe=False)
        # return JsonResponse({'status': False, 'data': "没有找到数据"}, status=404, safe=False)
        # 查找所有父评论（一级评论）
        # 获取所有父评论（一级评论）
        parent_comments = models.Comment.objects.filter(blog=blog_instance, parent_comment=None)
        # 使用分页器进行分页，每页显示5条评论
        paginator = Paginator(parent_comments, 3)

        # 获取请求页码，默认为第一页
        page_number = request.POST.get('page', 1)

        try:
            # 获取请求页的评论数据
            parent_comments_page = paginator.page(page_number)
        except EmptyPage:
            # 如果请求的页数超出范围，返回空数据
            parent_comments_page = []

        data = []

        # 遍历每个父评论
        for parent_comment in parent_comments_page:
            # 查找该父评论的所有子评论（二级评论）
            child_comments = models.Comment.objects.filter(parent_comment=parent_comment)

            # 构造父评论的字典
            parent_comment_data = {
                'id': parent_comment.id,
                'text': parent_comment.text,
                'created_at': parent_comment.created_at,
                'user': parent_comment.user.username if parent_comment.user else None,
                'child_comments': []
            }

            # 构造每个子评论的字典，并添加到父评论的字典中
            for child_comment in child_comments:
                child_comment_data = {
                    'id': child_comment.id,
                    'text': child_comment.text,
                    'created_at': child_comment.created_at,
                    'user': child_comment.user.username if child_comment.user else None,
                    'parent_comment': child_comment.parent_comment_id
                }
                parent_comment_data['child_comments'].append(child_comment_data)

            # 将父评论的字典添加到数据列表中
            data.append(parent_comment_data)

        return JsonResponse({'status': True, 'data': data}, status=200)

    return JsonResponse({'status': False, 'message': '不支持的请求方法'}, status=405, safe=False)


@auth
# 博客管理功能，根据username 查找博客
def blogs(request):
    if request.method == "GET":
        return HttpResponse("重新登录")
    elif request.method == "POST":
        print('这是请求的数据111', request.POST)
        username = request.POST.get('username')
        username_instance = models.BlogUser.objects.get(username=username)
        print(username_instance)
        # 获取所有博客实例
        blogs_instance = models.Blog.objects.filter(username=username_instance).order_by('createtime')
        # 使用分页器进行分页，每页显示5条评论
        paginator = Paginator(blogs_instance, 3)

        # 获取请求页码，默认为第一页
        page_number = request.POST.get('page', 1)

        try:
            # 获取请求页的评论数据
            blogs_instance_page = paginator.page(page_number)
        except EmptyPage:
            # 如果请求的页数超出范围，返回空数据
            blogs_instance_page = []

        data = []
        # 遍历每个父评论
        for blog in blogs_instance_page:
            # 获取博客所属的分类名称列表
            classifications = [classification.title for classification in blog.classification.all()]
            blogs_data = {
                'id': blog.id, 'title': blog.title,
                'summary': blog.summary, 'text': blog.text,
                'createtime': blog.createtime, 'username': blog.username.username if blog.username else None,
                'classification': classifications, 'status': blog.status,
                'feedback': blog.feedback
            }
            data.append(blogs_data)
        return JsonResponse({'status': True, 'data': data}, status=200, safe=False)
    return JsonResponse({'status': False, 'message': '不支持的请求方法'}, status=405, safe=False)


#  数据可视化，
def echarts(request):
    if request.method == "POST":
        return HttpResponse("重新请求")
    elif request.method == "GET":
        data = []
        # 统计博客数量
        blog_count = models.Blog.objects.count()
        # 统计用户的评论数量
        user_comment = models.Comment.objects.count()
        # 统计所有博客的点赞数量
        like_count = models.Bloglike.objects.filter(like=True).count()
        # 统计所有博客的不喜欢数量
        dislike_count = models.Bloglike.objects.filter(like=True).count()
        # 统计所有的分类，也就是标签数量
        category_count_all = models.Category.objects.count()
        # 统计前5个标签的博客数量
        # 查询每个标签下的博客数量，
        # Count('blog')是一个聚合函数，它会计算每个分类对象下关联的博客数量
        category_counts = models.Category.objects.annotate(blog_count=Count('blog')).order_by('-blog_count')
        # 获取前五个标签
        top_five_categories = category_counts[:5]
        category_count = [{'id': category.classification, 'title': category.title, 'count': category.blog_count} for
                          category in top_five_categories]
        # 查询点赞量前五博客的like dislike save 评论
        # 查询点赞最多的五个博客
        top_blogs_attached = models.Attached.objects.annotate(
            total_likes=F('like'),
            total_dislikes=F('dislike'),
            total_comments=F('comment'),
            total_collect=F('collect'),
        ).order_by('total_likes')[:3]
        blog_data = [
            {'blog_id': attached.blog.id, 'blog': attached.blog.title, 'likes': attached.total_likes,
             'dislikes': attached.total_dislikes, 'comments': attached.total_comments,
             'collect': attached.total_collect} for attached in top_blogs_attached]
        data_child = {
            'blog_count': blog_count, 'user_comment': user_comment, 'category_count_all': category_count_all,
            'like_count': like_count, 'dislike_count': dislike_count,
        }
        data.append(data_child)
        showdata = {'data': data, 'blog_data': blog_data, 'category_count': category_count}
        return JsonResponse({'status': True, 'data': showdata}, status=200, safe=False)
