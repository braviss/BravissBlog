from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from blog.models import Article
from view_breadcrumbs import (
    ListBreadcrumbMixin,
    DetailBreadcrumbMixin,
    CreateBreadcrumbMixin,
    DeleteBreadcrumbMixin,
    BaseBreadcrumbMixin,
)
from blog.forms import ArticleForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Employee
from blog.mixins import BalanceRequiredMixin
from decimal import Decimal
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required


class HomePageView(TemplateView):
    template_name = 'home.html'


class ArticleListView(LoginRequiredMixin,
                      ListBreadcrumbMixin,
                      ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    ordering = '-created_at'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(status='pu', type='a').order_by('-created_at')


class ArticleDetailView(LoginRequiredMixin,
                        DetailBreadcrumbMixin,
                        DetailView):
    model = Article
    breadcrumb_use_pk = False
    template_name = 'article_detail.html'
    count_hit = True

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.viewed()
        self.object = obj
        return obj


class ArticleCreateView(LoginRequiredMixin,
                        BalanceRequiredMixin,
                        CreateBreadcrumbMixin,
                        CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'
    success_url = reverse_lazy('blog:article_list')

    def form_valid(self, form):
        self.request.user.balance -= Decimal('10.0')
        self.request.user.save()

        form.instance.author = self.request.user
        messages.success(self.request,
                         'Awaiting moderator confirmation')
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, BaseBreadcrumbMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'
    crumbs = [("Article update", reverse_lazy('home'))]

    def form_valid(self, form):
        form.instance.status = 'pe'
        messages.success(self.request,
                         'Awaiting review by a moderator.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:article_detail',
                            kwargs={'slug': self.object.slug})


class ArticleDeleteView(LoginRequiredMixin,
                        DeleteBreadcrumbMixin,
                        DeleteView):
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('blog:article_list')


class UserArticleListView(ListBreadcrumbMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(Employee, username=self.kwargs['username'])
        return Article.objects.filter(author=user).order_by('-created_at')


class ArticleRaiseView(BaseBreadcrumbMixin, TemplateView):
    template_name = 'article_raise.html'
    crumbs = [("Article adv", reverse_lazy('home'))]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_slug = kwargs.get('slug')
        article = get_object_or_404(Article, slug=article_slug)
        context['article'] = article
        all_articles = Article.objects.filter(status='pu').order_by('-created_at')
        position = list(all_articles).index(article) + 1
        context['position'] = position
        total_articles = all_articles.count()
        context['total_articles'] = total_articles
        return context

@login_required
def update_publish_date(request, slug):
    if request.method == 'POST':
        article = get_object_or_404(Article, slug=slug)
        article.created_at = timezone.now()
        article.save()
        return redirect('blog:article_list')
    return redirect('blog:article_list')
