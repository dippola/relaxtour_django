import json

from rest_framework.decorators import api_view
from .models import UserModel, PostModel, PostCommentModel, PostModelView, LikeModel
from .serializers import UserModel_serializer, PostModel_serializer, PostCommentModel_serializer, PostModelView_serializer
from django.core.paginator import Paginator

from rest_framework.response import Response

from django.http  import JsonResponse, HttpResponse

from django.forms import model_to_dict

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

import mykeys

cred = credentials.Certificate('./relax-tour-de785-firebase-adminsdk-j86xu-68f3337ce7.json')
firebase_admin.initialize_app(cred,{
    'storageBucket' : mykeys.storageBucket
})





@api_view(['GET'])
def testDeleteStorage(reauest):
    # bucket = storage.bucket()
    # path = bucket.blob('userimages/test@gmail.com/2.png')
    # path.delete()
    bucket = storage.bucket()
    filenames = bucket.list_blobs(prefix='userimages/test@gmail.coma/')
    if filenames is not None:
        for name in filenames:
            path = bucket.blob(str(name.name))
            path.delete()
    return Response("Success")

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
    bucket = storage.bucket()
    filenames = bucket.list_blobs(prefix='userimages/' + str(user.id) + "/")
    if filenames is not None:
        for name in filenames:
            path = bucket.blob(str(name.name))
            path.delete()
    user.delete()
    return Response('user was deleted')


@api_view(['GET'])
def getPostsPageAll(request, page):
    posts = PostModel.objects.all()
    page = request.GET.get('page', page)
    paginator =Paginator(posts, 15)
    page_obj = paginator.page(page)
    postview = []
    for i in page_obj:
        if i.imageurl != "":
            imgcount = len(i.imageurl.split("●"))
        else:
            imgcount = 0
        like_count = LikeModel.objects.filter(parent_id=i.id).count()
        model = PostModelView(
            parent_id=i.id,
            parent_user=i.parent_user.id,
            nickname=i.parent_user.nickname,
            user_image=i.parent_user.imageurl,
            category=i.category,
            imageurlcount=imgcount,
            date=i.date,
            title=i.title,
            imageurl=i.imageurl,
            commentcount=PostCommentModel.objects.filter(parent_id=i.id).count(),
            view=i.view,
            like=like_count
        )
        postview.append(model)
    serializer = PostModelView_serializer(postview, many=True)
    return HttpResponse(json.dumps({'pages': paginator.num_pages, 'posts': serializer.data}))

@api_view(['GET'])
def getPostsPageWithCategory(request, category, page):
    posts = PostModel.objects.filter(category=category)
    page = request.GET.get('page', page)
    paginator =Paginator(posts, 15)
    page_obj = paginator.page(page)
    postview = []
    for i in page_obj:
        if i.imageurl != "":
            imgcount = len(i.imageurl.split("●"))
        else:
            imgcount = 0
        like_count = LikeModel.objects.filter(parent_id=i.id).count()
        model = PostModelView(
            parent_id=i.id,
            parent_user=i.parent_user.id,
            nickname=i.parent_user.nickname,
            user_image=i.parent_user.imageurl,
            category=i.category,
            imageurlcount=imgcount,
            date=i.date,
            title=i.title,
            imageurl=i.imageurl,
            commentcount=PostCommentModel.objects.filter(parent_id=i.id).count(),
            view=i.view,
            like=like_count
        )
        postview.append(model)
    serializer = PostModelView_serializer(postview, many=True)
    return HttpResponse(json.dumps({'pages': paginator.num_pages, 'posts': serializer.data}))

@api_view(['POST'])
def setLike(request, pk, id):
    like_model = LikeModel.objects.filter(parent_id=pk, user_ids=id).first()
    if like_model.exists():
        like_model.remove()
        return Response("delete")
    else:
        like_model(parent_id=1, user_ids=19)
        return Response("add")

@api_view(['PUT'])
def getPostDetail(request, pk):
    willAddHit = request.data['willAddHit']
    post = PostModel.objects.filter(id=pk).first()
    if willAddHit == True:
        post.view += 1
        mtd = {
            "view": post.view,
        }
        update_serializer = PostModel_serializer(post, data=mtd, partial=True)
        if update_serializer.is_valid():
            update_serializer.save()
    model = PostModel(
        id=post.id,
        parent_user=post.parent_user,
        nickname=post.parent_user.nickname,
        user_url=post.parent_user.imageurl,
        category=post.category,
        date=post.date,
        title=post.title,
        body=post.body,
        imageurl=post.imageurl,
        view=post.view,
        like=post.like,
        list=post.list,
        commentcount = PostCommentModel.objects.filter(parent_id=post.id).count()
    )
    post_serializer = PostModel_serializer(model)
    main_comment = PostCommentModel.objects.filter(parent_id=pk)
    page = request.GET.get('page', 1)
    paginator = Paginator(main_comment, 8)
    page_obj = paginator.page(page)
    comments_serializer = PostCommentModel_serializer(page_obj, many=True)
    return HttpResponse(json.dumps({'post': post_serializer.data, 'comments': comments_serializer.data}))

@api_view(['POST'])
def createPost(request, id):
    data = request.data
    user = UserModel.objects.get(id=id)
    main = PostModel.objects.create(
        parent_user = user,
        category = data['category'],
        title = data['title'],
        body = data['body'],
        imageurl = data['imageurl'],
        list=data['list']
    )
    serializer = PostModel_serializer(main, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updatePost(request, pk):
    data = request.data
    main = PostModel.objects.filter(id=pk).first()
    serializer = PostModel_serializer(main, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
def deletePost(request, pk):
    board = PostModel.objects.get(id=pk)
    bucket = storage.bucket()
    if board.imageurl != '':
        rd = board.imageurl.split("●")[1]
        filenames = bucket.list_blobs(prefix='community/main/' + rd + "/")
        if filenames is not None:
            for name in filenames:
                path = bucket.blob(str(name.name))
                path.delete()
    board.delete()
    return Response('board was deleted')

@api_view(['GET'])
def getPostAllComments(request, pk):
    comments = PostCommentModel.objects.filter(parent_id=pk)
    serializer = PostCommentModel_serializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPostComments(request, pk, page):
    main_comment = PostCommentModel.objects.filter(parent_id=pk)
    page = request.GET.get('page', page)
    paginator = Paginator(main_comment, 8)
    page_obj = paginator.page(page)
    serializer = PostCommentModel_serializer(page_obj, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPostCommentsMore(request, pk, lastid):
    main_comment = PostCommentModel.objects.filter(parent_id=pk)
    convert_request = PostCommentModel.objects.get(id=lastid)
    start_position = list(main_comment).index(convert_request)
    result_list = []
    count = 0
    for i, ii in enumerate(main_comment):
        count += 1
        if i  > start_position:
            if ii is not None:
                result_list.append(ii)
                if count == 8:
                    break
            else:
                break
    serializer = PostCommentModel_serializer(result_list, many=True)
    return Response(serializer.data)

# Main에 Comment 쓰기
@api_view(['POST'])
def createPostComment(request, pk, id):
    user = UserModel.objects.get(id=id)
    main = PostModel.objects.get(id=pk)
    to_id=0
    to_nickname=''
    data = request.data
    if data['to_id'] is not None:
        if data['to_id'] != 0:
            if UserModel.objects.get(id=data['to_id']) is not None:
                touser = UserModel.objects.get(id=data['to_id'])
                to_id = touser.id
                to_nickname = touser.nickname
    comment = PostCommentModel.objects.create(
        parent_user = user,
        parent_id = main,
        body = data['body'],
        nickname = user.nickname,
        user_url = user.imageurl,
        to_id = to_id,
        to_nickname=to_nickname
    )
    serializer = PostCommentModel_serializer(comment, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updatePostComment(request, id):
    comment = PostCommentModel.objects.filter(id=id).first()
    serializer = PostCommentModel_serializer(comment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
def deletePostComment(request, id):
    comment = PostCommentModel.objects.filter(id=id).first()
    comment.delete()
    return Response('comment was deleted')


# get all Main(url)
# @api_view(['GET'])
# def getMains(request):
#     posts = MainModel.objects.all()
#     serializer = MainModel_serializer(posts, many=True)
#     return Response(serializer.data)
#
# @api_view(['DELETE'])
# def deleteAllMain(request):
#     posts = MainModel.objects.all()
#     posts.delete()
#     return Response("deleted all main")



# Main 하나 가져오기(url)
# @api_view(['GET'])
# def getMain(request, pk):
#     post = MainModel.objects.get(id=pk)
#     serializer = MainModel_serializer(post, many=False)
#     return Response(serializer.data)

# Main글쓰기




@api_view(['GET'])
def getMainAllComments(request, pk):
    comments = PostCommentModel.objects.filter(parent_id=pk)
    serializer = PostCommentModel_serializer(comments, many=True)
    return Response(serializer.data)

# Main에 comments 가져오기(url)
















