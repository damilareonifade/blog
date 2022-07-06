from http.client import HTTPResponse
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from django.urls import reverse_lazy,reverse
from .form import CreateForm,UserEditForm,UserProfileForm
from django.http import HttpResponse,HttpResponseRedirect
from .models import Profile
from blog.models import Post,Vote
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.db.models import F
from django.http import JsonResponse

# Create your views here.

@login_required
def profile(request):
    post = Post.object.filter(status='Published')
    return render(request,'account/profile.html',{'posts':post})

@login_required
def avatar(request):
    user = User.objects.get(username=request.user)
    avatar = Profile.objects.filter(user=user)
    context = {
         'avatar' : avatar
          }
    return context



@login_required
def delete_user(request):
    if request.method == "POST":
        user = User.objects.get(username = request.user)
        user.is_active = False
        user.save()
        return reverse('accounts:login')
    return render(request,'account/delete.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=request.user.profile)

        if form.is_valid() and profile_form.is_valid():
            form.save(instance=request.user)
            profile_form.save(instance = request.user.profile)
    else:
        form= UserEditForm()
        profile_form = UserProfileForm()
    return render(request,'account/update.html',{'user_form':form,'profile_form':profile_form})

def register(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate Your Account"
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject=subject, message= message)
            return HttpResponse("Registered Successfully and Activation Sent")
    else:
        form = CreateForm()
    
    return render(request,'registration/register.html',{'form':form})

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')
    return render()

@login_required
def favourite_add(request,id):
    user = get_object_or_404(Post,id=id)
    test =  user.favourite.filter(id = request.user.id).exists()
    if test:
        user.favourite.remove(request.user)
    else:
        user.favourite.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def favourite_list(request):
    new = Post.object.filter(favourite=request.user)
    return render(request,'account/favourites.html',{'new':new})

def thumbs(request):
    if request.method.GET('action') == 'thumbs':
        id = int(request.POST.get('post_id'))
        button = request.POST.get('button')
        update = Post.object.get(id=id)

        if update.thumbs.filter(request.user.id).exists():

            q = Vote.object.get(
                Q(postid=id) & Q(userid=request.user.id)
            )
            evote = q.vote
            if evote == True:
                if button == 'thumbsup':
                    update.thumbsup = F('thumbsup') - 1
                    update.remove(request.user.id)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()
                    return JsonResponse({'up':up,'down':down,'remove':'none'})
                
                if button == 'thumbsdown':
                    update.thumbup = F('thumbsup') - 1
                    update.thumbsdown = F('thumbsdown') + 1
                    update.save()
                    q.vote = False
                    q.save(update_fields['vote'])
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    return JsonResponse({'up':up,'down':down})
                pass

            if evote == False:
                if button == 'thumbsup':
                    update.thumbsdown = F('thumbsdown') - 1
                    update.thumbsup = F('thumbsup') + 1
                    update.save()
                    q.vote = True
                    q.save(update_fields['vote'])
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    return JsonResponse({'up':up,'down':down})
                
                if button == 'thumbsdown':
                    update.thumbsdown = F('thumbsdown') - 1
                    update.remove(request.user.id)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up':up,'down':down,'remove': 'none'})

        # New Selection
        else:
            if button == 'thumbsup':
                update.thumbsup = F('thumbsup') + 1
                update.thumbs.add(request.user)
                update.save()
                new = Vote(postid=id,userid=request.user.id,vote=True)
                new.save()
            else:
                update.thumbsdown= F('thumbsdown') + 1
                update.thumbs.add(request.user)
                update.save()
                new = Vote(postid=id,userid=request.user.id,vote=False)
                new.save()
            
            update.refresh_from_db()
            up= update.thumbsup
            down= update.thumbsdown
            
            return JsonResponse({'up':up,'down':down})

def likes(request):
    if request.POST.get('action') == 'post':
        id = int(request.POST.get('postid'))
        post = Post.object.filter(id=id)
        if post.like.filter(id=request.user.id).exists():
            post.like_count = F('like_count') - 1
            post.like.remove(request.user.id)
            post.save()
            post.refresh_from_db()
            result = post.like_count
            return JsonResponse({'result':result})
        else:
            post.like_count = F('like_count') + 1
            post.like.add(request.user.id)
            post.save()
            post.refresh_from_db()
            result = post.like_count
            return JsonResponse({'result':result}) 


