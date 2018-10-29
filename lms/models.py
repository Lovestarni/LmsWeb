from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Catalog(models.Model):
    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

    name = models.CharField('类别名', max_length=20)
    description = models.TextField('描述', blank=True)

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = verbose_name
        ordering = ('pubdate',)

    # 图书类
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    title = models.CharField('书名', max_length=200)
    subtitile = models.CharField('副标题', max_length=200, blank=True)
    pages = models.IntegerField('页数', blank=True)
    author = models.CharField('作者', max_length=60, blank=True)
    translator = models.CharField('译者', max_length=60, blank=True)
    price = models.CharField('定价', max_length=60, blank=True)
    publisher = models.CharField('出版社', max_length=200, blank=True)
    pubdate = models.CharField('出版日期', max_length=60, blank=True)
    cover_img = models.ImageField('封面', upload_to='category', blank=True)
    summary = models.TextField('内容简介', max_length=2000, blank=True)
    author_intro = models.TextField('作者简介', max_length=2000, blank=True)
    number = models.IntegerField('库存数量', default=0)
    catelog = models.ForeignKey(Catalog, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.title)


class CommonUser(models.Model):
    # user class
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickyName = models.CharField('昵称', blank=True, max_length=50)
    cate = models.BooleanField('类别', default=False)
    # False stands for students, True represent Teacher
    faculty = models.CharField('系别', max_length=20, blank=True, default='undefine')
    bookBorrow = models.IntegerField('已借图书数目', default=0)
    bookSub = models.IntegerField('已预约图书数目', default=0)

    def __str__(self):
        return str(self.nickyName)


class Borrow(models.Model):
    class Meta:
        verbose_name = '借阅'
        verbose_name_plural = verbose_name

    userId = models.IntegerField('用户编号')
    bookId = models.IntegerField('图书编号')
    boDate = models.DateTimeField('借书时间', auto_now_add=True)
    reDate = models.DateTimeField('还书时间', null=True)
    returnFlag = models.BooleanField('归还标志', default=False)

    def __str__(self):
        return str(str(self.userId) + str(self.bookId))


class Comments(models.Model):
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    userId = models.IntegerField('用户编号')
    bookId = models.IntegerField('图书编号')
    content = models.TextField('评论内容')

    def __str__(self):
        return str(str(self.userId) + str(self.bookId))


class Subscription(models.Model):
    class Meta:
        verbose_name = '预定'
        verbose_name_plural = verbose_name

    userId = models.IntegerField('用户编号')
    bookId = models.IntegerField('图书编号')
    subDate = models.DateTimeField('预定日期', auto_now_add=True)
    number = models.IntegerField('数量', default=1)
    successFlag = models.BooleanField('完成预约标志', default=False)

    def __str__(self):
        return str(str(self.userId) + str(self.bookId))
