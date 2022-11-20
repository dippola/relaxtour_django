from rest_framework.decorators import api_view
from .models import UserModel, MainModel, QnaModel, MainCommentModel, QnaCommentModel
from .serializers import UserModel_serializer, MainModel_serializer, QnaModel_serializer, MainCommentModel_serializer, QnaCommentModel_serializer
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
def getUser(request, uid):
    user = UserModel.objects.filter(uid=uid)
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
    )
    serializer = UserModel_serializer(main, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateUser(request, uid):
    data = request.data
    user = UserModel.objects.filter(uid=uid).first()
    serializer = UserModel_serializer(user, data=data)
    if serializer.is_valid():
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

# Main paginator(url)
@api_view(['GET'])
def getMainsPage(request, page):
    posts = MainModel.objects.all()
    page = request.GET.get('page', page)
    paginator =Paginator(posts, 15)
    page_obj = paginator.page(page)
    serializer = MainModel_serializer(page_obj, many=True)
    return Response(serializer.data)

# Main 하나 가져오기(url)
@api_view(['GET'])
def getMain(request, pk):
    post = MainModel.objects.get(id=pk)
    serializer = MainModel_serializer(post, many=False)
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

# Main글쓰기
@api_view(['POST'])
def createMain(request):
    data = request.data
    user = UserModel.objects.filter(uid=data['uid']).first()
    main = MainModel.objects.create(
        parent_user = user,
        uid = data['uid'],
        title = data['title'],
        body = data['body'],
        imageurl = data['imageurl'],
    )
    serializer = MainModel_serializer(main, many=False)
    return Response(serializer.data)

# Main에 Comment 쓰기
@api_view(['POST'])
def createMainComment(request, pk, uid):
    user = UserModel.objects.filter(uid=uid)
    main = MainModel.objects.get(id=pk)
    data = request.data
    comment = MainCommentModel.objects.create(
        parent_user = user,
        parent_id = main,
        uid = uid,
        title = data['title'],
        body = data['body'],
        to = data['to']
    )
    serializer = MainCommentModel_serializer(comment, many=False)
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

@api_view(['DELETE'])
def deleteMain(request, pk):
    board = MainModel.objects.get(id=pk)
    board.delete()
    return Response('board was deleted')

@api_view(['PUT'])
def updateMainComment(request, main_pk, comment_pk):
    comments = MainCommentModel.objects.get(parent_id=main_pk).parent_id
    comment = comments.get(id=comment_pk)
    serializer = MainCommentModel_serializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("update comment success")
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteMainComment(request, main_pk, comment_pk):
    comments = MainCommentModel.objects.get(parent_id=main_pk).parent_id
    comment = comments.get(id=comment_pk)
    comment.delete()
    return Response('board was deleted')





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
