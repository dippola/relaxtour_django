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
    path('user/test/delete/', views.testDeleteStorage),
    path('users/delete/', views.deleteAllUser),#will delete
    path('user/create/', views.createUser),#
    path('user/searchemail/<str:email>/', views.searchEmail),#
    path('user/searchnickname/<str:nickname>/', views.searchNickname),#
    path('user/<str:id>/', views.getUser),#
    path('user/<str:uid>/update/', views.updateUser),#
    path('user/<str:uid>/delete/', views.deleteUser),#
    path('user/<str:id>/updatenotification/', views.updateUserNotification),#

    path('posts/', views.getMains),#
    path('posts/delete/', views.deleteAllMain),#will delete
    path('posts/page=<str:page>/', views.getMainsPage),#
    path('post/create=<str:id>/', views.createMain),#
    path('post/comment/update=<str:id>/', views.updateMainComment),
    path('post/comment/delete=<str:id>/', views.deleteMainComment),
    path('post/<str:pk>/', views.getMainDetail),#
    path('post/<str:pk>/update/', views.updateMain),#
    path('post/<str:pk>/delete/', views.deleteMain),#
    path('post/<str:pk>/comment/create=<str:id>/', views.createMainComment),#
    path('post/<str:pk>/comments/', views.getMainAllComments),#
    path('post/<str:pk>/comments/page=<str:page>/', views.getMainComments),#
    path('post/<str:pk>/comments/more=<str:lastid>/', views.getMainCommentsMore),

    path('qnas/', views.getQnas),
    path('qnas/page=<str:page>/', views.getQnasPage),
    path('qna/create=<str:uid>/', views.createQna),
    path('qna/<str:uid>', views.getQna),
    path('qna/<str:pk>/update/', views.updateQna),
    path('qna/<str:pk>/delete/', views.deleteQna),
    path('qna/<str:pk>/comment/create/', views.createQnaComment),
    path('qna/<str:pk>/comment/update/', views.updateQnaComment),
    path('qna/<str:pk>/comment/delete/', views.deleteQnaComment),
    path('qna/<str:pk>/comments/page=<str:page>/', views.getQnaComments),
]