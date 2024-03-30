from django.contrib import admin
from blog.models import Article, Category
from django.utils import timezone


@admin.action(description="Mark selected stories as published")
def make_published(modeladmin, request, queryset):
    queryset.update(status="pu")


@admin.action(description="Raise article")
def raise_article(modeladmin, request, queryset):
    queryset.update(created_at=timezone.now())


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "slug", "author"]
    list_filter = ('status', 'created_at')
    ordering = ["-created_at"]
    exclude = ["last_modify_time"]
    actions = [make_published, raise_article]
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title',
              'slug',
              'body',
              'category',
              'image',
              'status',
              'type',
              'author',
              'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug",]
