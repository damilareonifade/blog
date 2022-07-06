from operator import contains
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from .models import Post,Category
from .form import NewCommentForm,PostSearchForm
from django.core import serializers
from django.views.generic import ListView
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from django.http import JsonResponse

def category(request):
    category_list = Category.objects.all()
    context = {"category_list":category_list}
    return context

def index_page(request):
    post = Post.object.filter(status='Published')
    return render(request, 'blog/home.html',{'posts':post})

def post_single(request, post):

    post = get_object_or_404(Post, slug=post, status='Published')

    fav = bool

    if post.favourite.filter(id=request.user.id).exists():
        fav = True

    allcomments = post.comments.filter(status=True)
    
    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post.slug)
    else:
        comment_form = NewCommentForm()
    return render(request, 'blog/single.html', {'post': post,  'comment_form': comment_form, 'allcomments': allcomments, 'fav': fav})



class CategoryListView(ListView):
    template_name = "category.html"
    context_object_name = 'catlist'

    def get_queryset(self):
        content= {
        'cat':self.kwargs['category'],
        'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published')
        }
        return content

def post_search(request):
    form = PostSearchForm()
    q= ''
    c= ''
    query = Q()
    results = []

    if request.POST.get('action') == 'post':
        search_string = str(request.POST.get('ss'))

        if search_string is not None:
            search_string = Post.object.filter(title__contains = search_string)[:3]

            data = serializers.serialize('json',list(search_string),fields=('id','title','slug'))

            return JsonResponse({'search_string':data})


    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']
            if c is not None:
                query &= Q(category=c)
            
            if q is not None:
                query &= Q(category=c)
            results = Post.object.filter(query)
    return render(request,'blog/search.html',{'form':form,'q':q,'results':results})