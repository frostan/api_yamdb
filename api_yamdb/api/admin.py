from django.contrib import admin
from reviews.models import Titles, Genres, Comment, Review, Categories
# Register your models here.
admin.site.register(Titles,)
admin.site.register(Genres,)
admin.site.register(Comment,)
admin.site.register(Review,)
admin.site.register(Categories,)