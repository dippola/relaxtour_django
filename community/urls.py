from django.urls import path
from . import views

urlpatterns = [
    # path('boards/', views.getBoards),
    # path('board/create/', views.createBoard),
    # path('board/<str:pk>/', views.getBoard),
    # path('board/<str:pk>/update/', views.updateBoard),
    # path('board/<str:pk>/delete/', views.deleteBoard),
    # path('board/<str:pk>/comment/', views.getComments),
    # path('board/<str:pk>/comment/create/', views.createComment),
    # path('board/<str:board_pk>/comment/<str:comment_pk>/delete/', views.deleteComment),
    # path('board/<str:board_pk>/comment/<str:comment_pk>/update/', views.updateComment),
    # path('boards/page=<str:page>/', views.getBoardsPage),
    # path('comments', views.getAllComments)

    path('users/', views.getUsers),#
    path('users/delete/', views.deleteAllUser),#will delete
    path('user/create/', views.createUser),#
    path('user/searchemail/<str:email>/', views.searchEmail),#
    path('user/searchnickname/<str:nickname>/', views.searchNickname),#
    path('user/<str:id>/', views.getUser),#
    path('user/<str:uid>/update/', views.updateUser),#
    path('user/<str:uid>/delete/', views.deleteUser),#
    path('user/<str:id>/updatenotification/', views.updateUserNotification),#

    path('posts/page=<str:page>/', views.getPostsPageAll),
    path('posts/category=<str:category>/page=<str:page>/', views.getPostsPageWithCategory),
    path('post/create=<str:id>/', views.createPost),
    path('post/<str:pk>/', views.getPostDetail),
    path('post/<str:pk>/update/', views.updatePost),
    path('post/<str:pk>/delete/', views.deletePost),
    path('post/<str:pk>/comments/', views.getPostAllComments),
    path('post/<str:pk>/comments/page=<str:page>/', views.getPostComments),
    path('post/<str:pk>/comments/more=<str:lastid>/', views.getPostCommentsMore),
    path('post/<str:pk>/comment/create=<str:id>/', views.createPostComment),
    path('post/<str:pk>/comment/<str:id>/update/', views.updatePostComment),
    path('post/<str:pk>/comment/<str:id>/delete/', views.deletePostComment),



    # path('posts/', views.getMains),#
    # path('posts/delete/', views.deleteAllMain),#will delete
    # path('posts/page=<str:page>/', views.getMainsPage),#
    # path('post/create=<str:id>/', views.createMain),#
    # path('post/comment/update=<str:id>/', views.updateMainComment),
    # path('post/comment/delete=<str:id>/', views.deleteMainComment),
    # path('post/<str:pk>/', views.getMainDetail),#
    # path('post/<str:pk>/update/', views.updateMain),#
    # path('post/<str:pk>/delete/', views.deleteMain),#
    # path('post/<str:pk>/comment/create=<str:id>/', views.createMainComment),#
    # path('post/<str:pk>/comments/', views.getMainAllComments),#
    # path('post/<str:pk>/comments/page=<str:page>/', views.getMainComments),#
    # path('post/<str:pk>/comments/more=<str:lastid>/', views.getMainCommentsMore),

]