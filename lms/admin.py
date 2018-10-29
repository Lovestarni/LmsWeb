from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from .models import *

class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'isbn', 'catelog', 'title', 'author', 'price', 'publisher', 'pubdate','number']
    list_editable = ['title', 'author', 'price', 'number']
    list_per_page = 10
    list_filter = ['pubdate']
    search_fields = ['title','author','publisher','summary']

class BorrowAdmin(admin.ModelAdmin):
    list_display = ['id', 'userId', 'bookId', 'boDate', 'reDate', 'returnFlag']
    list_editable = ['reDate','returnFlag']
    list_filter = ['boDate', 'returnFlag']

class CommonUserInline(admin.TabularInline):
    model = CommonUser
    can_delete = False
    verbose_name = '用户'
    verbose_name_plural = verbose_name

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id','userId','bookId']

class UserAdmin(BaseUserAdmin):
    inlines = (CommonUserInline, )

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id','userId','bookId','subDate','number']
    list_filter = ['subDate', 'successFlag']

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Borrow, BorrowAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.site_header = '图书借阅系统管理'