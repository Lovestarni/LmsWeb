from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    path('', views.index, name='lms_index'),
    # path('bookBrowse', views.bookBrowse, name='bookBrowse'),
    path('browseHistory', views.borrowHistory, name='borrowHistory'),
    path('subHistory', views.subHistory, name='subHistory'),
    path('userCentre', views.userCentre, name='userCentre'),
    # path('comments', views.comments, name='comments'),
    path('about', views.about, name='about'),
    path('subAndBo/<int:bookId>', views.subAndBo, name='subAndBo'),
    path('returnBook/<int:bookId>', views.returnBook, name='returnBook'),
    path('login/', views.loging, name='login'),
    path('logout/', views.logouting, name='logout'),
    path('register/', views.register, name='register'),
    path('detail/<int:bookId>', views.bookDetail, name='bookDetail'),
    path('comment/<int:bookId>', views.comment, name='comment'),
    path('cate/<int:cateId>', views.cateQuery, name='cateQuery'),
    path('bookSearch/', views.bookSearch, name='bookSearch'),
]
