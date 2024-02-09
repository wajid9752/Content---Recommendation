from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login ,  logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .recommendation import recommendation_script

@login_required(login_url="login")
def home(request):
    cat_form = CategoryForm()
    tag_form = TagForm()
    contents = Content.objects.all()
    return render(request, "home.html" , locals())




@login_required(login_url="login")
def profile(request):
    return render(request, "profile.html")



@login_required(login_url="login")
def update_profile(request):
    obj = CustomUser.objects.get(email = request.user.email )
    
    if request.POST:
        form = UserUpdateForm(request.POST ,instance = obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully")
            return redirect("profile")
        else:
            return render(request, "update-profile.html" , {'form':form})
    
    form = UserUpdateForm(instance = obj)
    return render(request, "update-profile.html" , {'form':form})


def user_login(request):    
    if request.POST:
        email = request.POST.get('email')
        raw_password = request.POST.get('password')

        user = authenticate(email=email, password=raw_password)
        if user is not None:
            login(request, user) 
            messages.success(request, "You are logged successfully.")
            return redirect("home")
        else:
            messages.error(request , "Credentials are not matched")
            return redirect("login")
        
    return render(request , "login.html")


def user_registration(request):
    if request.POST:
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticate user after registration and redirect to home
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            
            if user is not None:
                login(request, user) 
            else:    
                messages.error(request , "Something Went Wrong! Contact Admin")
                return redirect("register")
            
            messages.success(request, "You are registered successfully.")
            return redirect("home")
            
        else:
            return render(request , "register.html" , {'form':form} )    
        
    context={'form': RegisterUserForm() }
    return render(request , "register.html" , context)


def user_logout(request):
    logout(request)
    messages.success(request , "You are Logout Successfully!")
    return redirect("login")



## content 

@login_required(login_url="login")        
def my_content_list(request):
    contents = Content.objects.filter(user=request.user)
    return render(request , "my-contents.html" , locals())        


@login_required(login_url="login")
def content_detail(request, content_id):
    content = Content.objects.get(pk=content_id)
    recommended_contents = []
    
    # Retrieve recommended contents using recommendation_view
    get_output = recommendation_script(request.user)
    if get_output:
        for category in get_output:
            objs = Content.objects.filter(category=category)[:2]
            recommended_contents.extend(objs)
    
    # If no recommended contents, fetch some other contents
    if not recommended_contents:
        recommended_contents = Content.objects.exclude(pk=content_id)[:5]

    # Increment views count if the viewer is not the owner of the content
    if request.user != content.user:
        content.views += 1
        content.save()

    # Determine if the content is an image or a video
    is_video = content.file.url.lower().endswith(('.mp4', '.avi', '.mov'))
    is_img = content.file.url.lower().endswith(('.jpg', '.jpeg', '.png'))

    context = {
        'content': content,
        'is_img': is_img,
        'is_video': is_video,
        'recommended_contents': recommended_contents,
    }
    return render(request, 'content-detail.html', context)


@login_required(login_url="login")
def add_content(request):
    if request.method == 'POST':
        form = AddContentForm(request.POST, request.FILES)
        if form.is_valid():
            copy_form = form.save(commit=False)
            copy_form.user = request.user
            copy_form.save()
            return redirect('my-content-list')  # Redirect to a view displaying a list of contents
    else:
        form = AddContentForm()
    return render(request, 'form.html', {'form': form})

@login_required(login_url="login")
def update_content(request, content_id):
    content = get_object_or_404(Content, pk=content_id)
    if request.method == 'POST':
        form = AddContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            return redirect('my-content-list')  # Redirect to a view displaying a list of contents
    else:
        form = AddContentForm(instance=content)
    return render(request, 'form.html', {'form': form})

@login_required(login_url="login")
def delete_content(request, content_id):
    content = get_object_or_404(Content, pk=content_id)
    content.delete()
    return redirect('my-content-list')  # Redirect to a view displaying a list of contents
    
@login_required(login_url="login")
def recommendation_view(request):
    recommended_contents = []
    get_output = recommendation_script(request.user)
    if get_output:
        for category in get_output:
            objs = Content.objects.filter(category=category)[:2]
            recommended_contents.extend(objs)
    
    # If no recommended contents, fetch some other contents
    if not recommended_contents:
        recommended_contents = Content.objects.all()[:10]
    
    return render(request , "recommend.html" ,{ 'recommended_contents': recommended_contents} )
    

## acessing form js 
def filter_category(request):
    contents = []
    tag_id = request.GET.get('tag_id')
    category_id = request.GET.get('category_id')

  
    if category_id:
        contents = Content.objects.filter(category__id = category_id)

    if tag_id:
        contents = Content.objects.filter(tags__id = tag_id)
    
    return render(request , "partials/cards.html" , context={'contents':contents})



def dislike_likes_view(request):
    get_query = request.GET.get("query")
    get_content_id = request.GET.get("content")

    obj = Content.objects.get(id=get_content_id)
    
    if Content_Attributes.objects.filter(content_id = obj , user = request.user).exists():
        return JsonResponse({'status': f"You Alredy did your action"})
    
    
    if get_query == "like":
        Content_Attributes.objects.create(content_id = obj , user = request.user , is_like=True )
        obj.likes += 1
        obj.save() 
        status = "success"

    elif get_query == "dislike":
        Content_Attributes.objects.create(content_id = obj , user = request.user , is_like=False )
        obj.dislikes += 1
        obj.save() 
        status = "success"

    else:
        status = "failed"

    return JsonResponse({
        'status': status, 
        'like': obj.likes, 
        'dislike': obj.dislikes 
    })