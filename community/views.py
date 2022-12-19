import datetime
import json

from rest_framework.decorators import api_view
from .models import UserModel, PostModel, PostCommentModel, LikeModel
from .serializers import UserModel_serializer, PostModel_serializer, PostCommentModel_serializer, LikeModel_serializer
from django.core.paginator import Paginator

from rest_framework.response import Response

from django.http import JsonResponse, HttpResponse

from django.forms import model_to_dict

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import messaging

import mykeys

cred = credentials.Certificate('./relax-tour-de785-firebase-adminsdk-j86xu-68f3337ce7.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': mykeys.storageBucket
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
        uid=data['uid'],
        email=data['email'],
        imageurl=data['imageurl'],
        nickname=data['nickname'],
        provider=data['provider'],
        token=data['token'],
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
def getUserCommunity(request, id):
    posts = PostModel.objects.filter(parent_user=id).count()
    comments = PostCommentModel.objects.filter(parent_user=id).count()
    likes = LikeModel.objects.filter(user_ids=id).count()
    return Response(str(posts) + "/" + str(comments) + "/" + str(likes))


@api_view(['GET'])
def getUserCommunityPost(request, id, page):
    posts = PostModel.objects.filter(parent_user=id)
    page = request.GET.get('page', page)
    paginator = Paginator(posts, 15)
    page_obj = paginator.page(page)
    postview = []
    for i in page_obj:
        if i.imageurl != "":
            imgcount = len(i.imageurl.split("●"))
        else:
            imgcount = 0
        model = {
            'parent_id': i.id,
            'parent_user': i.parent_user.id,
            'nickname': i.parent_user.nickname,
            'user_image': i.parent_user.imageurl,
            'category': i.category,
            'imageurlcount': imgcount,
            'date': str(i.date),
            'title': i.title,
            'imageurl': i.imageurl,
            'commentcount': PostCommentModel.objects.filter(parent_id=i.id).count(),
            'view': i.view,
            'like': LikeModel.objects.filter(parent_id=i.id).count()
        }
        postview.append(model)
    return HttpResponse(json.dumps({'pages': paginator.num_pages, 'posts': postview}))


@api_view(['GET'])
def getUserCommunityCategory(request, id, category, page):
    posts = PostModel.objects.filter(parent_user=id, category=category)
    page = request.GET.get('page', page)
    paginator = Paginator(posts, 15)
    page_obj = paginator.page(page)
    postview = []
    for i in page_obj:
        if i.imageurl != "":
            imgcount = len(i.imageurl.split("●"))
        else:
            imgcount = 0
        model = {
            'parent_id': i.id,
            'parent_user': i.parent_user.id,
            'nickname': i.parent_user.nickname,
            'user_image': i.parent_user.imageurl,
            'category': i.category,
            'imageurlcount': imgcount,
            'date': str(i.date),
            'title': i.title,
            'imageurl': i.imageurl,
            'commentcount': PostCommentModel.objects.filter(parent_id=i.id).count(),
            'view': i.view,
            'like': LikeModel.objects.filter(parent_id=i.id).count()
        }
        postview.append(model)
    return HttpResponse(json.dumps({'pages': paginator.num_pages, 'posts': postview}))


@api_view(['GET'])
def getUsersCommentsAll(request, id, page):
    print(">>>1: " + str(request.user_agent.is_mobile))
    print(">>>2: " + str(request.user_agent.is_tablet))
    print(">>>3: " + str(request.user_agent.is_touch_capable))
    print(">>>4: " + str(request.user_agent.is_pc))
    print(">>>5: " + str(request.user_agent.is_bot))
    print(">>>6: " + str(request.user_agent.browser))
    print(">>>7: " + str(request.user_agent.os))
    print(">>>7: " + str(request.user_agent.device))
    comments = PostCommentModel.objects.filter(parent_user=id).order_by('-date')
    page = request.GET.get('page', page)
    paginator = Paginator(comments, 15)
    page_obj = paginator.page(page)
    result = []
    for i in page_obj:
        fori = {
            'parent_id': i.parent_id_id,
            'towho': i.to_nickname,
            'body': i.body,
            'date': str(i.date)
        }
        result.append(fori)
    return HttpResponse(json.dumps({'pages':paginator.num_pages, 'result': result}))

@api_view(['GET'])
def getUsersLikeAll(request, id, page):
    likes = LikeModel.objects.filter(user_ids=id)
    page = request.GET.get('page', page)
    paginator = Paginator(likes, 15)
    page_obj = paginator.page(page)
    result = []
    for i in page_obj:
        post = PostModel.objects.get(id=i.parent_id_id)
        if post.imageurl != "":
            imgcount = len(post.imageurl.split("●"))
        else:
            imgcount = 0
        model = {
            'parent_id': post.id,
            'parent_user': post.parent_user.id,
            'nickname': post.parent_user.nickname,
            'user_image': post.parent_user.imageurl,
            'category': post.category,
            'imageurlcount': imgcount,
            'date': str(post.date),
            'title': post.title,
            'imageurl': post.imageurl,
            'commentcount': PostCommentModel.objects.filter(parent_id=post.id).count(),
            'view': post.view,
            'like': LikeModel.objects.filter(parent_id=post.id).count()
        }
        result.append(model)
    return HttpResponse(json.dumps({'pages': paginator.num_pages, 'posts': result}))





@api_view(['GET'])
def getPostsPageAll(request, page):
    posts = PostModel.objects.all()
    page = request.GET.get('page', page)
    paginator = Paginator(posts, 10)
    page_obj = paginator.page(page)
    postview = []
    for i in page_obj:
        if i.imageurl != "":
            imgcount = len(i.imageurl.split("●"))
        else:
            imgcount = 0
        model = {
            'parent_id': i.id,
            'parent_user': i.parent_user.id,
            'nickname': i.parent_user.nickname,
            'user_image': i.parent_user.imageurl,
            'category': i.category,
            'imageurlcount': imgcount,
            'date': str(i.date),
            'title': i.title,
            'imageurl': i.imageurl,
            'commentcount': PostCommentModel.objects.filter(parent_id=i.id).count(),
            'view': i.view,
            'like': LikeModel.objects.filter(parent_id=i.id).count()
        }
        postview.append(model)
    return HttpResponse(json.dumps({'pages': paginator.num_pages, 'posts': postview}))


@api_view(['GET'])
def getPostsPageWithCategory(request, category, page):
    posts = PostModel.objects.filter(category=category)
    page = request.GET.get('page', page)
    paginator = Paginator(posts, 10)
    page_obj = paginator.page(page)
    postview = []
    for i in page_obj:
        if i.imageurl != "":
            imgcount = len(i.imageurl.split("●"))
        else:
            imgcount = 0
        model = {
            'parent_id': i.id,
            'parent_user': i.parent_user.id,
            'nickname': i.parent_user.nickname,
            'user_image': i.parent_user.imageurl,
            'category': i.category,
            'imageurlcount': imgcount,
            'date': str(i.date),
            'title': i.title,
            'imageurl': i.imageurl,
            'commentcount': PostCommentModel.objects.filter(parent_id=i.id).count(),
            'view': i.view,
            'like': LikeModel.objects.filter(parent_id=i.id).count()
        }
        postview.append(model)
    return HttpResponse(json.dumps({'pages': paginator.num_pages, 'posts': postview}))


@api_view(['PUT'])
def setLike(request, pk, id):
    like_model = LikeModel.objects.filter(parent_id=pk, user_ids=id).first()
    if like_model is None:
        post_model = PostModel.objects.get(id=pk)
        user_model = UserModel.objects.get(id=id)
        model = LikeModel(
            parent_id=post_model,
            user_ids=user_model
        )
        model.save()
        return Response("add")
    else:
        like_model.delete()
        return Response("remove")


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
    like_user_list = LikeModel.objects.filter(parent_id=post.id)
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
        like=like_user_list.count(),
        list=post.list,
        commentcount=PostCommentModel.objects.filter(parent_id=post.id).count()
    )
    post_serializer = PostModel_serializer(model)
    main_comment = PostCommentModel.objects.filter(parent_id=pk)
    page = request.GET.get('page', 1)
    paginator = Paginator(main_comment, 6)
    page_obj = paginator.page(page)
    comments_serializer = PostCommentModel_serializer(page_obj, many=True)
    like_user_list_serializer = LikeModel_serializer(like_user_list, many=True)
    return HttpResponse(json.dumps({'post': post_serializer.data, 'comments': comments_serializer.data,
                                    'likeuserlist': like_user_list_serializer.data}))


@api_view(['POST'])
def createPost(request, id):
    data = request.data
    user = UserModel.objects.get(id=id)
    main = PostModel.objects.create(
        parent_user=user,
        category=data['category'],
        title=data['title'],
        body=data['body'],
        imageurl=data['imageurl'],
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
    paginator = Paginator(main_comment, 6)
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
        if i > start_position:
            if ii is not None:
                result_list.append(ii)
                if count == 6:
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
    to_id = 0
    to_nickname = ''
    data = request.data
    is_have_to = False
    if data['to_id'] is not None:
        if data['to_id'] != 0:
            if UserModel.objects.get(id=data['to_id']) is not None:
                touser = UserModel.objects.get(id=data['to_id'])
                to_id = touser.id
                to_nickname = touser.nickname
                is_have_to = True
    comment = PostCommentModel.objects.create(
        parent_user=user,
        parent_id=main,
        body=data['body'],
        nickname=user.nickname,
        user_url=user.imageurl,
        to_id=to_id,
        to_nickname=to_nickname
    )
    serializer = PostCommentModel_serializer(comment, many=False)
    if main.parent_user.id != user.id:
        if main.parent_user.notification:
            sendNotification(token=main.parent_user.token, title="There is a comment on your comment.", body=data['body'], postid=pk, user_url=user.imageurl, nickname=user.nickname)
    if is_have_to:
        if UserModel.objects.get(id=to_id).notification:
            to_token = UserModel.objects.get(id=to_id).token
            sendNotification(token=to_token, title="The comment has been registered in your post.", body=data['body'], postid=pk, user_url=user.imageurl, nickname=user.nickname)
    return Response(serializer.data)

def sendNotification(token, title, body, postid, user_url, nickname):
    message = messaging.Message(
        notification = messaging.Notification(
            title="comment●" + str(postid) + "●" + user_url + "●" + nickname + "●" + title,
            body=body,
        ),
        android = messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority = 'normal',
            notification = messaging.AndroidNotification(
                icon='',
                color='#000000'
            )
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(badge=42),
            ),
        ),
        token=token,
    )
    response = messaging.send(message)


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
