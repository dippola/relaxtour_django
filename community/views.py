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

import appkeys

cred = credentials.Certificate('./relax-tour-de785-firebase-adminsdk-j86xu-68f3337ce7.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': appkeys.storageBucket
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
def getUser(request, id):
    if request.headers['key'] == appkeys.appkey:
        user = UserModel.objects.filter(id=id)
        serializer = UserModel_serializer(user, many=True)
        return Response(serializer.data)
    else:
        return Response("failed")


# user생성
@api_view(['POST'])
def createUser(request):
    if request.headers['key'] == appkeys.appkey:
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
    else:
        return Response("failed")


@api_view(['PUT'])
def updateUser(request, uid):
    if request.headers['key'] == appkeys.appkey:
        data = request.data
        user = UserModel.objects.filter(uid=uid).first()
        serializer = UserModel_serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    else:
        return Response("failed")


@api_view(['PUT'])
def updateUserNotification(request, id):
    if request.data['key'] == appkeys.appkey:
        data = request.data
        user = UserModel.objects.filter(id=id).first()
        serializer = UserModel_serializer(user, data=data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    else:
        return Response("Failed")


@api_view(['GET'])
def searchEmail(request, email):
    if request.headers['key'] == appkeys.appkey:
        user = UserModel.objects.filter(email=email)
        serializer = UserModel_serializer(user, many=True)
        return Response(serializer.data)
    else:
        return Response("Failed")


@api_view(['GET'])
def searchNickname(request, nickname):
    if request.headers['key'] == appkeys.appkey:
        user = UserModel.objects.filter(nickname=nickname)
        serializer = UserModel_serializer(user, many=True)
        return Response(serializer.data)
    else:
        return Response("Failed")


@api_view(['DELETE'])
def deleteUser(request, uid):
    if request.headers['key'] == appkeys.appkey:
        user = UserModel.objects.filter(uid=uid).first()
        bucket = storage.bucket()
        filenames = bucket.list_blobs(prefix='userimages/' + str(user.id) + "/")
        if filenames is not None:
            for name in filenames:
                path = bucket.blob(str(name.name))
                path.delete()
        user.delete()
        return Response('user was deleted')
    else:
        return Response('Failed')


@api_view(['GET'])
def getUserCommunity(request, id):
    if request.headers['key'] == appkeys.appkey:
        posts = PostModel.objects.filter(parent_user=id).count()
        comments = PostCommentModel.objects.filter(parent_user=id).count()
        likes = LikeModel.objects.filter(user_ids=id).count()
        return Response(str(posts) + "/" + str(comments) + "/" + str(likes))
    else:
        return Response("Failed")


@api_view(['GET'])
def getUserCommunityPost(request, id, page):
    if request.headers['key'] == appkeys.appkey:
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
    else:
        return HttpResponse("Failed")


@api_view(['GET'])
def getUserCommunityCategory(request, id, category, page):
    if request.headers['key'] == appkeys.appkey:
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
    else:
        return HttpResponse("Failed")


@api_view(['GET'])
def getUsersCommentsAll(request, id, page):
    if request.headers['key'] == appkeys.appkey:
        comments = PostCommentModel.objects.filter(parent_user=id).order_by('-date')
        page = request.GET.get('page', page)
        paginator = Paginator(comments, 15)
        page_obj = paginator.page(page)
        result = []
        for i in page_obj:
            to_nickname = None
            if i.to_id is not None:
                if i.to_id != 21:
                    to_nickname = UserModel.objects.get(id=i.to_id.id).nickname
                else:
                    to_nickname = 'unknown'
            fori = {
                'parent_id': i.parent_id_id,
                'towho': to_nickname,
                'body': i.body,
                'date': str(i.date)
            }
            result.append(fori)
        return HttpResponse(json.dumps({'pages':paginator.num_pages, 'result': result}))
    else:
        return HttpResponse("Failed")

@api_view(['GET'])
def getUsersLikeAll(request, id, page):
    if request.headers['key'] == appkeys.appkey:
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
    else:
        return HttpResponse("Failed")




@api_view(['GET'])
def getPostsPageAll(request, page):
    if request.headers['key'] == appkeys.appkey:
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
    else:
        return HttpResponse("Failed")


@api_view(['GET'])
def getPostsPageWithCategory(request, category, page):
    if request.headers['key'] == appkeys.appkey:
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
    else:
        return HttpResponse("Failed")


@api_view(['PUT'])
def setLike(request, pk, id):
    if request.headers['key'] == appkeys.appkey:
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
    else:
        return Response("Failed")


@api_view(['PUT'])
def getPostDetail(request, pk):
    if request.headers['key'] == appkeys.appkey:
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
        model = {
            'id': post.id,
            'parent_user': post.parent_user.id,
            'nickname': post.parent_user.nickname,
            'user_url': post.parent_user.imageurl,
            'category': post.category,
            'date': str(post.date),
            'title': post.title,
            'body': post.body,
            'imageurl': post.imageurl,
            'view': post.view,
            'like': like_user_list.count(),
            'list':post.list,
            'commentcount': PostCommentModel.objects.filter(parent_id=post.id).count()
        }
        main_comment = PostCommentModel.objects.filter(parent_id=pk)
        page = request.GET.get('page', 1)
        paginator = Paginator(main_comment, 6)
        page_obj = paginator.page(page)
        modellist = []
        for i in page_obj:
            to_id = None
            to_nickname = None
            if i.to_id is not None:
                if i.to_id != 21:
                    to_id = i.to_id.id
                    to_nickname = UserModel.objects.get(id=i.to_id.id).nickname
                else:
                    to_id = 21
                    to_nickname = 'unknown'
            commentmodel = {
                'id': i.id,
                'date': str(i.date),
                'parent_id': i.parent_id.id,
                'parent_user': i.parent_user.id,
                'body': i.body,
                'nickname': i.parent_user.nickname,
                'user_url': i.parent_user.imageurl,
                'to_id': to_id,
                'to_nickname': to_nickname
            }
            modellist.append(commentmodel)
        like_user_list_serializer = LikeModel_serializer(like_user_list, many=True)
        return HttpResponse(json.dumps({'post': model, 'comments': modellist, 'commentsPages': paginator.num_pages,
                                        'likeuserlist': like_user_list_serializer.data}))
    else:
        return HttpResponse("Failed")


@api_view(['POST'])
def createPost(request, id):
    if request.headers['key'] == appkeys.appkey:
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
    else:
        return Response("Failed")

@api_view(['PUT'])
def updatePost(request, pk):
    if request.headers['key'] == appkeys.appkey:
        data = request.data
        main = PostModel.objects.get(id=pk)
        model = {
            "title": data['title'],
            "body": data['body'],
            "imageurl": data['imageurl'],
            "list": data['list']
        }
        serializer = PostModel_serializer(main, data=model, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(">>>1")
            return Response("Success")
        print(">>>2")
        return Response("Failed: " + str(serializer.errors))
    else:
        print(">>>3")
        return Response("Failed")


@api_view(['DELETE'])
def deletePost(request, pk):
    if request.headers['key'] == appkeys.appkey:
        board = PostModel.objects.get(id=pk)
        bucket = storage.bucket()
        if board.imageurl != '':
            rd = board.imageurl.split("●")[0]
            filenames = bucket.list_blobs(prefix='community/main/' + rd + "/")
            if filenames is not None:
                for name in filenames:
                    path = bucket.blob(str(name.name))
                    path.delete()
        board.delete()
        return Response('board was deleted')
    else:
        return Response("Failed")


@api_view(['GET'])
def getPostAllComments(request, pk):
    if request.headers['key'] == appkeys.appkey:
        comments = PostCommentModel.objects.filter(parent_id=pk)
        commentlist = []
        for i in comments:
            to_id = None
            to_nickname = None
            if i.to_id is not None:
                if i.to_id != 21:
                    to_id = i.to_id.id
                    to_nickname = UserModel.objects.get(id=i.to_id.id).nickname
                else:
                    to_id = 21
                    to_nickname = 'unknown'
            model = {
                'id': i.id,
                'date': str(i.date),
                'parent_id': i.parent_id.id,
                'parent_user': i.parent_user.id,
                'body': i.body,
                'nickname': i.parent_user.nickname,
                'user_url': i.parent_user.imageurl,
                'to_id': to_id,
                'to_nickname': to_nickname
            }
            commentlist.append(model)
        return HttpResponse(json.dumps({'comments': commentlist}))
    else:
        return Response("Failed")


@api_view(['GET'])
def getPostComments(request, pk, page):
    if request.headers['key'] == appkeys.appkey:
        main_comment = PostCommentModel.objects.filter(parent_id=pk)
        page = request.GET.get('page', page)
        paginator = Paginator(main_comment, 6)
        page_obj = paginator.page(page)
        modellist = []
        for i in page_obj:
            to_id = None
            to_nickname = None
            if i.to_id is not None:
                if i.to_id != 21:
                    to_id = i.to_id.id
                    to_nickname = UserModel.objects.get(id=i.to_id.id).nickname
                else:
                    to_id = 21
                    to_nickname = 'unknown'
            model = {
                'id': i.id,
                'date': str(i.date),
                'parent_id': i.parent_id.id,
                'parent_user': i.parent_user.id,
                'body': i.body,
                'nickname': i.parent_user.nickname,
                'user_url': i.parent_user.imageurl,
                'to_id': to_id,
                'to_nickname': to_nickname
            }
            modellist.append(model)
        return HttpResponse(json.dumps({'comments': modellist}))
    else:
        return HttpResponse("Failed")


@api_view(['GET'])
def getPostCommentsMore(request, pk, page):
    if request.headers['key'] == appkeys.appkey:
        comments = PostCommentModel.objects.filter(parent_id=pk)
        page = request.GET.get('page', page)
        paginator = Paginator(comments, 6)
        print(">>>1: " + str(type(int(paginator.num_pages))))
        print(">>>2: " + str(type(int(page))))
        if int(page) <= int(paginator.num_pages):
            page_obj = paginator.page(page)
            modellist = []
            for i in page_obj:
                to_id = None
                to_nickname = None
                if i.to_id is not None:
                    if i.to_id != 21:
                        to_id = i.to_id.id
                        to_nickname = UserModel.objects.get(id=i.to_id.id).nickname
                    else:
                        to_id = 21
                        to_nickname = 'unknown'
                model = {
                    'id': i.id,
                    'date': str(i.date),
                    'parent_id': i.parent_id.id,
                    'parent_user': i.parent_user.id,
                    'body': i.body,
                    'nickname': i.parent_user.nickname,
                    'user_url': i.parent_user.imageurl,
                    'to_id': to_id,
                    'to_nickname': to_nickname
                }
                modellist.append(model)
            return HttpResponse(json.dumps({'comments': modellist, 'pages': paginator.num_pages}))
        else:
            return Response("Failed")
    else:
        return Response("Failed")


# Main에 Comment 쓰기
@api_view(['POST'])
def createPostComment(request, pk, id):
    if request.headers['key'] == appkeys.appkey:
        user = UserModel.objects.get(id=id)
        main = PostModel.objects.get(id=pk)
        to_id = 0
        data = request.data
        is_have_to = False
        comment = PostCommentModel
        if data['to_id'] is not None:
            if data['to_id'] != 0:
                if UserModel.objects.get(id=data['to_id']) is not None:
                    to_id = UserModel.objects.get(id=data['to_id']).id
                    is_have_to = True
                    comment = PostCommentModel.objects.create(
                        parent_user=user,
                        parent_id=main,
                        body=data['body'],
                        to_id=UserModel.objects.get(id=data['to_id']),
                    )
                else:
                    comment = PostCommentModel.objects.create(
                        parent_user=user,
                        parent_id=main,
                        body=data['body']
                    )
            else:
                comment = PostCommentModel.objects.create(
                    parent_user=user,
                    parent_id=main,
                    body=data['body']
                )
        else:
            comment = PostCommentModel.objects.create(
                parent_user=user,
                parent_id=main,
                body=data['body']
            )
        serializer = PostCommentModel_serializer(comment, many=False)
        if main.parent_user.id != user.id:
            if main.parent_user.notification:
                sendNotification(token=main.parent_user.token, title="The comment has been registered in your post.", body=data['body'], postid=pk, user_url=user.imageurl, nickname=user.nickname)
        if is_have_to:
            print(">>>1")
            if UserModel.objects.get(id=to_id).notification:
                print(">>>2")
                to_token = UserModel.objects.get(id=to_id).token
                sendNotification(token=to_token, title="There is a comment on your comment.", body=data['body'], postid=pk, user_url=user.imageurl, nickname=user.nickname)
        return Response(serializer.data)
    else:
        return Response("Failed")

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
            data = {
                "title": "comment●" + str(postid) + "●" + user_url + "●" + nickname + "●" + title,
                "body": body
            },
            token=token,
        )
        try:
            print(">>>3")
            response = messaging.send(message)
            Response("Firebase Cloud Messaging Successed")
        except Exception as e:
            Response("Firebase Cloud Messaging Failed: " + str(e))


@api_view(['PUT'])
def updatePostComment(request, pk, id):
    if request.headers['key'] == appkeys.appkey:
        # commentmodel = PostCommentModel.objects.create(
        #     body=request.data['body']
        # )
        data = request.data
        comment = PostCommentModel.objects.filter(id=id).first()
        serializer = PostCommentModel_serializer(comment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Comment has been edited")
        return Response("not valid")
    else:
        return Response("Failed")

@api_view(['DELETE'])
def deletePostComment(request, pk, id):
    if request.headers['key'] == appkeys.appkey:
        comment = PostCommentModel.objects.get(id=id)
        comment.delete()
        return Response('comment was deleted')
    else:
        return Response("Failed")

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

@api_view(['DELETE'])
def adminDeletePost(request, pk):
    if request.headers['key'] == appkeys.appkey:
        # board = PostModel.objects.get(id=pk)
        # bucket = storage.bucket()
        # if board.imageurl != '':
        #     rd = board.imageurl.split("●")[0]
        #     filenames = bucket.list_blobs(prefix='community/main/' + rd + "/")
        #     if filenames is not None:
        #         for name in filenames:
        #             path = bucket.blob(str(name.name))
        #             path.delete()
        # board.delete()
        # token = ""
        # title = ""
        # body = ""

        post = PostModel.objects.get(id=pk)
        token = post.parent_user.token
        title = "Relax Tour a policy violation"
        body = "The post has been deleted due to a violation of the community usage policy.\n(Reason: " + request.headers['why'] + ")"
        user_url = "https://firebasestorage.googleapis.com/v0/b/relax-tour-de785.appspot.com/o/admin%2Fadminimage.jpeg?alt=media&token=0963e1cd-9ae8-4df2-8ac6-25ebdf42e742"
        # post.delete()
        adminNotification(token=token, title=title, body=body, postid=pk, user_url=user_url, nickname="Relax Tour")
        return Response('board was deleted')
    else:
        return Response("Failed")

@api_view(['DELETE'])
def adminDeleteComment(request, pk):
    if request.headers['key'] == appkeys.appkey:
        comment = PostCommentModel.objects.get(id=pk)
        token = comment.parent_user.token
        title = "Relax Tour a policy violation"
        body = "The comment has been deleted due to a violation of the community usage policy.\n(Reason: " + \
               request.headers['why'] + ")"
        user_url = "https://firebasestorage.googleapis.com/v0/b/relax-tour-de785.appspot.com/o/admin%2Fadminimage.jpeg?alt=media&token=0963e1cd-9ae8-4df2-8ac6-25ebdf42e742"
        # comment.delete()
        adminNotification(token=token, title=title, body=body, postid=pk, user_url=user_url, nickname="Relax Tour")
        return Response('board was deleted')
    else:
        return Response('Failed')

def adminNotification(token, title, body, postid, user_url, nickname):
    message = messaging.Message(
        notification=messaging.Notification(
            title="admin●" + str(postid) + "●" + user_url + "●" + nickname + "●" + title,
            body=body,
        ),
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='normal',
            notification=messaging.AndroidNotification(
                icon='',
                color='#000000'
            )
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(badge=42),
            ),
        ),
        data={
            "title": "admin●" + str(postid) + "●" + user_url + "●" + nickname + "●" + title,
            "body": body
        },
        token=token,
    )
    try:
        print(">>>3")
        response = messaging.send(message)
        Response("Firebase Cloud Messaging Successed")
    except Exception as e:
        Response("Firebase Cloud Messaging Failed: " + str(e))

@api_view(['GET'])
def adminGetCommentUser(request, pk):
    if request.headers['key'] == appkeys.appkey:
        comment_user = PostCommentModel.objects.get(id=pk).parent_user.id
        return Response(comment_user)
    else:
        return Response(0)

@api_view(['PUT'])
def adminUserUpdate(request, id):
    if request.headers['key'] == appkeys.appkey:
        data = request.data
        user = UserModel.objects.filter(id=id).first()
        serializer = UserModel_serializer(user, data=data, partial=True)
        token = user.token
        title = "Relax Tour a policy violation"
        body = "Account profile has been deleted and changed due to a community policy violation.\n(Reason: " + \
               request.headers['why'] + ")"
        user_url = "https://firebasestorage.googleapis.com/v0/b/relax-tour-de785.appspot.com/o/admin%2Fadminimage.jpeg?alt=media&token=0963e1cd-9ae8-4df2-8ac6-25ebdf42e742"
        adminNotificationProfileUpdate(token=token, title=title, body=body, user_url=user_url, nickname="Relax Tour")
        if serializer.is_valid():
            serializer.save()
            return Response("success")
        else:
            return Response("not valid")
    else:
        return Response("Failed")

def adminNotificationProfileUpdate(token, title, body, user_url, nickname):
    message = messaging.Message(
        notification=messaging.Notification(
            title="admin_profile●" + user_url + "●" + nickname + "●" + title,
            body=body,
        ),
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='normal',
            notification=messaging.AndroidNotification(
                icon='',
                color='#000000'
            )
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(badge=42),
            ),
        ),
        data={
            "title": "admin_profile●" + user_url + "●" + nickname + "●" + title,
            "body": body,
        },
        token=token,
    )
    try:
        print(">>>3")
        response = messaging.send(message)
        Response("Firebase Cloud Messaging Successed")
    except Exception as e:
        Response("Firebase Cloud Messaging Failed: " + str(e))