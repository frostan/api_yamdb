from django.contrib import admin
from reviews.models import Title, Genre, Comment, Review, Category
# Register your models here.
admin.site.register(Title,)
admin.site.register(Genre,)
admin.site.register(Comment,)
admin.site.register(Review,)
admin.site.register(Category,)
