import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
# Create your views here.
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import UserCustomRegister, UserCustomChange
from django.contrib.auth.models import User


def index(request):
    if request.method == 'GET':
        content = {'bookList': Book.objects.all(), 'currentUser': request.user,
                   'cateList': Catalog.objects.all()}
    return render(request, 'lms/index.html', content)


def about(request):
    # need id to define special book
    return render(request, 'lms/about.html')


def loging(request):
    # 登录模块
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'lms/login.html', {'error': '用户名不存在或密码错误'})
        else:
            login(request, user)
            return redirect('lms:lms_index')
    else:
        return render(request, 'lms/login.html')


def logouting(request):
    logout(request)
    return redirect('lms:lms_index')


def register(request):
    if request.method == 'POST':
        registerForm = UserCustomRegister(request.POST)
        if registerForm.is_valid():
            registerForm.save()
            newUser = authenticate(username=registerForm.cleaned_data['username'],
                                   password=registerForm.cleaned_data['password1'])
            newUser.email = registerForm.cleaned_data['email']
            CommonUser(user=newUser, nickyName=registerForm.cleaned_data['nickyName'],
                       cate=registerForm.cleaned_data['cate'],
                       faculty=registerForm.cleaned_data['faculty']).save()
            login(request, newUser)
            return redirect('lms:lms_index')
    else:

        registerForm = UserCustomRegister()
    content = {'registerForm': registerForm}
    return render(request, 'lms/register.html', content)


# def bookBrowse(request):
#     return render(request, 'lms/bookBrowse.html')


@login_required(login_url='lms:login')
def userCentre(request):
    # need id to define special user
    if request.method == 'POST':
        changeForm = UserCustomChange(request.POST, instance=request.user)
        if changeForm.is_valid():
            changeForm.save()
            request.user.commonuser.nickyName = changeForm.cleaned_data['nickyName']
            request.user.commonuser.save()
            # 关联的表要另外存储
            # newUser.email = registerForm.cleaned_data['email']
            # CommonUser(user=newUser, nickyName=registerForm.cleaned_data['nickyName'],
            #            cate=registerForm.cleaned_data['cate'],
            #            faculty=registerForm.cleaned_data['faculty']).save()
    else:
        pass
    changeForm = UserCustomChange()
    content = {'currentUser': request.user, 'changeForm': changeForm}
    return render(request, 'lms/userCentre.html', content)


@login_required(login_url='lms:login')
def subHistory(request):
    # need id to define special user
    if request.method == 'GET':
        bookListTarget = Subscription.objects.filter(userId=request.user.id)
        booklist = []
        for subInfo in bookListTarget:
            subTime = datetime.datetime.now().day - subInfo.subDate.day
            booklist.append((Book.objects.get(pk=subInfo.bookId), subInfo, subTime))
        content = {'bookList': booklist, 'currentUser': request.user}
    return render(request, 'lms/subHistory.html', content)


@login_required(login_url='lms:login')
def borrowHistory(request):
    # need id to define special user
    if request.method == 'GET':
        bookListTarget = Borrow.objects.filter(userId=request.user.id)
        booklist = []
        for borrowInfo in bookListTarget:
            borrowTime = datetime.datetime.now().day - borrowInfo.boDate.day
            booklist.append((Book.objects.get(pk=borrowInfo.bookId), borrowInfo, borrowTime))
        content = {'bookList': booklist, 'currentUser': request.user}
    return render(request, 'lms/borrowHistory.html', content)


# def comments(request):
#     # need id to define special book
#     return render(request, 'lms/comments.html')


@login_required(login_url='lms:login')
def subAndBo(request, bookId):
    # process subscrip
    if request.method == 'POST':
        if request.POST['subAndBoButton'] == '0':
            # 借书
            thisUser = User.objects.get(pk=request.user.id)
            if (thisUser.commonuser.cate is False and thisUser.commonuser.bookBorrow < 6) or (
                    thisUser.commonuser.cate is True and thisUser.commonuser.bookBorrow < 10):
                newBorrow = Borrow(userId=request.user.id, bookId=bookId)
                newBorrow.save()
                thisUser.commonuser.bookBorrow = thisUser.commonuser.bookBorrow + 1
                thisUser.commonuser.save()
                thisBook = Book.objects.get(pk=bookId)
                thisBook.number = thisBook.number - 1
                thisBook.save()
                content = {'bookList': Book.objects.all(), 'currentUser': request.user, 'successInfo': '借书成功'}
                return render(request, 'lms/index.html', content)
            else:
                content = {'bookList': Book.objects.all(), 'currentUser': request.user, 'failedInfo': '借书失败，超出借书最大数目'}
                return render(request, 'lms/index.html', content)

        elif request.POST['subAndBoButton'] == '1':
            thisUser = User.objects.get(pk=request.user.id)
            if thisUser.commonuser.bookSub < 3:
                newSub = Subscription(bookId=bookId, userId=request.user.id)
                newSub.save()
                thisUser.commonuser.bookSub = thisUser.commonuser.bookSub + 1
                thisUser.commonuser.save()
                content = {'bookList': Book.objects.all(), 'currentUser': request.user, 'successInfo': '预约成功'}
                return render(request, 'lms/index.html', content)
            else:
                content = {'bookList': Book.objects.all(), 'currentUser': request.user, 'failedInfo': '预约失败，超出可预约最大数目'}
                return render(request, 'lms/index.html', content)
    return redirect('lms:lms_index')


@login_required(login_url='lms:login')
def returnBook(request, bookId):
    # need id to define special user
    if request.method == 'POST':
        thisUser = User.objects.get(pk=request.user.id)
        thisUser.commonuser.bookBorrow = thisUser.commonuser.bookBorrow - 1
        thisUser.commonuser.save()
        thisBook = Book.objects.get(pk=bookId)
        thisBook.number = thisBook.number + 1
        thisBook.save()
        thisBorrow = Borrow.objects.get(pk = request.POST['borrowId'])
        thisBorrow.reDate = datetime.datetime.now()
        thisBorrow.returnFlag = True
        thisBorrow.save()
        return redirect('lms:borrowHistory')


def bookDetail(request, bookId):
    if request.method == 'GET':
        thisBook = Book.objects.get(id=bookId)
        commentList = Comments.objects.filter(bookId=bookId)
        commentInfoList = []
        # commentInfoList集合了用户和借阅信息
        for comment in commentList:
            commentInfoList.append((comment, User.objects.get(pk=comment.userId)))
        content = {'book': thisBook, 'commentList': commentInfoList}
        return render(request, 'lms/detail.html', content)


@login_required(login_url='lms:login')
def comment(request, bookId):
    if request.method == 'POST':
        if request.POST['comment'] != '':
            newComment = Comments(userId=request.user.id, bookId=bookId)
            newComment.content = request.POST['comment']
            newComment.save()
            return redirect('lms:bookDetail', bookId=bookId)
        else:
            return redirect('lms:bookDetail', bookId=bookId)
    else:
        return redirect('lms:bookDetail', bookId=bookId)


def cateQuery(request, cateId):
    if request.method == 'GET':
        content = {'bookList': Book.objects.filter(catelog_id=cateId),
                   'cateList': Catalog.objects.all(), 'currentUser': request.user}
        return render(request, 'lms/index.html', content)


def bookSearch(request):
    if request.method == 'POST':
        searchType = request.POST['searchType']
        keyword = request.POST['keyword']
        if searchType == 'title':
            bookList = Book.objects.filter(title__contains=keyword)
        elif searchType == 'author':
            bookList = Book.objects.filter(author__contains=keyword)
        elif searchType == 'summary':
            bookList = Book.objects.filter(summary__contains=keyword)
        else:
            bookList = Book.objects.filter(Q(title__contains=keyword) |
                                           Q(author__contains=keyword) |
                                           Q(summary__contains=keyword))

        content = {'bookList': bookList, 'cateList': Catalog.objects.all(), 'currentUser': request.user}
        return render(request, 'lms/index.html', content)
