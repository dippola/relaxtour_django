from rest_framework.decorators import api_view
from .models import UserModel, MainModel, QnaModel, MainCommentModel, QnaCommentModel, MainModelView
from .serializers import UserModel_serializer, MainModel_serializer, QnaModel_serializer, MainCommentModel_serializer, QnaCommentModel_serializer, MainModelView_serializer
from django.core.paginator import Paginator

from rest_framework.response import Response

@api_view(['GET'])
def getUsers(request):
    users = UserModel.objects.all()
    serializer = UserModel_serializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteAllUser(request):
    users = UserModel.objects.all()
    users.delete()
    return Response('user was deleted')

@api_view(['GET'])
def getUser(request, id):
    user = UserModel.objects.filter(id=id)
    serializer = UserModel_serializer(user, many=True)
    return Response(serializer.data)

# user생성
@api_view(['POST'])
def createUser(request):
    data = request.data
    main = UserModel.objects.create(
        uid = data['uid'],
        email = data['email'],
        imageurl = data['imageurl'],
        nickname = data['nickname'],
        provider = data['provider'],
        token = data['token'],
    )
    serializer = UserModel_serializer(main, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateUser(request, uid):
    data = request.data
    user = UserModel.objects.filter(uid=uid).first()
    serializer = UserModel_serializer(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['PUT'])
def updateUserNotification(request, id):
    data = request.data
    user = UserModel.objects.filter(id=id).first()
    serializer = UserModel_serializer(user, data=data, partial=True)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def searchEmail(request, email):
    user = UserModel.objects.filter(email=email)
    serializer = UserModel_serializer(user, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def searchNickname(request, nickname):
    user = UserModel.objects.filter(nickname=nickname)
    serializer = UserModel_serializer(user, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteUser(request, uid):
    user = UserModel.objects.filter(uid=uid)
    user.delete()
    return Response('user was deleted')



# get all Main(url)
@api_view(['GET'])
def getMains(request):
    posts = MainModel.objects.all()
    serializer = MainModel_serializer(posts, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteAllMain(request):
    posts = MainModel.objects.all()
    posts.delete()
    return Response("deleted all main")

@api_view(['GET'])
def getMainsPage(request, page):
    posts = MainModel.objects.all()
    page = request.GET.get('page', page)
    paginator =Paginator(posts, 15)
    page_obj = paginator.page(page)
    postview = []
    for i in page_obj:
        model = MainModelView(
            parent_id=i.id,
            parent_user=i.parent_user.id,
            nickname=i.parent_user.nickname,
            user_image=i.parent_user.imageurl,
            date=i.date,
            title=i.title,
            imageurl=i.imageurl,
            commentcount=MainCommentModel.objects.filter(parent_id=i.id).count(),
            like=i.like
        )
        postview.append(model)
    serializer = MainModelView_serializer(postview, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMainDetail(request, pk):
    post = MainModel.objects.filter(id=pk).first()
    comments = MainCommentModel.objects.filter(parent_id=post.id)
    comments_page = request.GET.get('page', 1)
    paginator = Paginator(comments, 3)
    page_obj = paginator.page(comments_page)
    print(">>>" + str([len(page_obj)]))
    model = MainModel(
        id=post.id,
        parent_user=post.parent_user,
        nickname=post.parent_user.nickname,
        user_url=post.parent_user.imageurl,
        date=post.date,
        title=post.title,
        body=post.body,
        imageurl=post.imageurl,
        view=post.view,
        like=post.like,
        list=post.list
    )
    # for i in page_obj:
    #     post.comment.add(i)
    serializer = MainModel_serializer(model)
    return Response(serializer.data)

# Main 하나 가져오기(url)
# @api_view(['GET'])
# def getMain(request, pk):
#     post = MainModel.objects.get(id=pk)
#     serializer = MainModel_serializer(post, many=False)
#     return Response(serializer.data)

# Main글쓰기
@api_view(['POST'])
def createMain(request, id):
    data = request.data
    user = UserModel.objects.get(id=id)
    main = MainModel.objects.create(
        parent_user = user,
        title = data['title'],
        body = data['body'],
        imageurl = data['imageurl'],
        list=data['list']
    )
    serializer = MainModel_serializer(main, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateMain(request, pk):
    data = request.data
    main = MainModel.objects.filter(id=pk).first()
    serializer = MainModel_serializer(main, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def getMainAllComments(request, pk):
    comments = MainCommentModel.objects.filter(parent_id=pk)
    serializer = MainCommentModel_serializer(comments, many=True)
    return Response(serializer.data)

# Main에 comments 가져오기(url)
@api_view(['GET'])
def getMainComments(request, pk, page):
    main_comment = MainCommentModel.objects.filter(parent_id=pk)
    page = request.GET.get('page', page)
    paginator = Paginator(main_comment, 15)
    page_obj = paginator.page(page)
    serializer = MainCommentModel_serializer(page_obj, many=True)
    return Response(serializer.data)

# Main에 Comment 쓰기
@api_view(['POST'])
def createMainComment(request, pk, id):
    user = UserModel.objects.get(id=id)
    main = MainModel.objects.get(id=pk)
    to_id=0
    to_nickname=''
    data = request.data
    if data['to_id'] is not None:
        if UserModel.objects.get(id=data['to_id']) is not None:
            touser = UserModel.objects.get(id=data['to_id'])
            to_id = touser.id
            to_nickname = touser.nickname
    comment = MainCommentModel.objects.create(
        parent_user = user,
        parent_id = main,
        body = data['body'],
        nickname = user.nickname,
        user_url = user.imageurl,
        to_id = to_id,
        to_nickname=to_nickname
    )
    serializer = MainCommentModel_serializer(comment, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteMain(request, pk):
    board = MainModel.objects.get(id=pk)
    board.delete()
    return Response('board was deleted')

@api_view(['PUT'])
def updateMainComment(request, id):
    comment = MainCommentModel.objects.filter(id=id).first()
    serializer = MainCommentModel_serializer(comment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
def deleteMainComment(request, id):
    comment = MainCommentModel.objects.filter(id=id).first()
    comment.delete()
    return Response('comment was deleted')





# get all Qna(url)
@api_view(['GET'])
def getQnas(request):
    qnas = QnaModel.objects.all()
    serializer = QnaModel_serializer(qnas, many=True)
    return Response(serializer.data)

# Qna paginator(url)
@api_view(['GET'])
def getQnasPage(request, page):
    qnas = QnaModel.objects.all()
    page = request.GET.get('page', page)
    paginator =Paginator(qnas, 15)
    page_obj = paginator.page(page)
    serializer = QnaModel_serializer(page_obj, many=True)
    return Response(serializer.data)

# Qna 하나 가져오기(url)
@api_view(['GET'])
def getQna(request, uid):
    qna = QnaModel.objects.filter(uid=uid)
    serializer = QnaModel_serializer(qna, many=False)
    return Response(serializer.data)

# Qna에 comments 가져오기(url)
@api_view(['GET'])
def getQnaComments(request, page):
    qna_comments = QnaCommentModel.objects.all()
    page = request.GET.get('page', page)
    paginator = Paginator(qna_comments, 15)
    page_obj = paginator.page(page)
    serializer = QnaCommentModel_serializer(page_obj, many=True)
    return Response(serializer.data)

# Qna글쓰기
@api_view(['POST'])
def createQna(request, uid):
    user = UserModel.objects.filter(uid=uid)
    data = request.data
    qna = QnaModel.objects.create(
        parent_user = user,
        uid = user['uid'],
        title = data['title'],
        body = data['body'],
        imageurl = data['imageurl'],
    )
    serializer = QnaModel_serializer(qna, many=False)
    return Response(serializer.data)

# Qna에 Comment 쓰기
@api_view(['POST'])
def createQnaComment(request, pk, uid):
    user = UserModel.objects.filter(uid=uid)
    qna = QnaModel.objects.get(id=pk)
    data = request.data
    comment = QnaCommentModel.objects.create(
        parent_user = user,
        parent_id = qna,
        uid = uid,
        title = data['title'],
        body = data['body'],
        to = data['to']
    )
    serializer = QnaCommentModel_serializer(comment, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateQna(request, pk):
    data = request.data
    qna = QnaModel.objects.get(id=pk)
    serializer = QnaModel_serializer(qna, data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteQna(request, pk):
    qna = QnaModel.objects.get(id=pk)
    qna.delete()
    return Response('board was deleted')

@api_view(['PUT'])
def updateQnaComment(request, main_pk, comment_pk):
    comments = QnaCommentModel.objects.get(parent_id=main_pk).parent_id
    comment = comments.get(id=comment_pk)
    serializer = QnaCommentModel_serializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("update comment success")
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteQnaComment(request, main_pk, comment_pk):
    comments = QnaCommentModel.objects.get(parent_id=main_pk).parent_id
    comment = comments.get(id=comment_pk)
    comment.delete()
    return Response('board was deleted')
