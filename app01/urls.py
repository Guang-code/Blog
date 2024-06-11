"""
conding: utf-8
@time:2024/3/7 17:23
"""
from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login),
    # 将一个类作为一个路由视图
    path('test/', views.testView.as_view()),
    path('auth/', views.AuthView.as_view()),
    path('order/', views.OrderView.as_view()),

    # 博客用户添加
    path('bloguser/', views.bloguser),
    # 博客用查询
    path('bloguser/search/', views.bloguser_search),
    # 用户相关博客查询
    path('bloguser/blog/', views.bloguser_blog),
    # 博客信息添加
    path('bloginfo/', views.bloginfo),
    # 博客更新
    path('bloginfo/update/', views.bloginfo_update),
    # 博客信息删除
    path('bloginfo/delete/', views.bloginfo_delete),
    # 博客首页简要信息获取
    path('bloginfo/search/', views.bloginfo_search),
    # 博客详细信息查找
    path('bloginfo/search/all/', views.bloginfo_search_all),
    path('blog/id/search/', views.blog_id_search),

    # 所有分类信息查找
    path('category/title/all/', views.category_title_all),
    # 首页及推荐标签展示
    path('category/detail/', views.category_detail),
    # 根据标签查找相关的blog
    path('category/blog/tuijian/', views.category_blog_all),
    path('category/tuijian/', views.category_blog_mohu_all),
    # 根据博客id查找相关的点赞数等
    path('attached/search/', views.attached_search),
    # 根据博客id查找相关的标签
    path('attached/search/category/', views.attached_search_category),
    # 根据attached的id字段，更新点赞等数据
    path('attached/update/', views.attached_update),
    # bloglike,创建点赞等信息。
    path('bloglike/', views.bloglike),
    # # 根据用户名和博客ID查找该用户在此博客的点赞等记录
    path('search/bloglike/', views.search_bloglike),
    # 用户在博客创建评论
    path('comment/', views.comment),
    # 搜索该博客的所有评论
    path('comment/search/', views.comment_search),
    # 博客管理功能，根据usernam查找该用户的所有博客
    path('blogs/', views.blogs),
    # 数据可视化
    path('echarts/', views.echarts)

]