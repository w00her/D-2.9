from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        postRate = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRate.get('postRating')

        commentRate = self.authorUser.comment_set.aggregate(
            commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRate.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    ARTICLE = 'ART'
    NEWS = 'NWS'
    CATEGORY_CHOICES = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    )

    categoryType = models.CharField(
        max_length=3, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview_temp(self):
        return self.text[:123] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField(max_length=255)
    rating = models.IntegerField(default=0)
    dateCreation = models.DateTimeField(auto_now_add=True)
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
