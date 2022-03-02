from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Game, Score, Row, Column
from django.contrib.auth.models import User
from .forms import GameForm, UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import matplotlib.pyplot as plt
import io, base64

# Create your views here.
@login_required
def index(request):
    games = Game.objects.filter(users__username=request.user.username)
    context_dict= {} 
    context_dict["games"] = games
    response = render(request, 'scoretracker/index.html', context=context_dict)
    return response

@login_required
def view_game(request,game_slug):
    game = Game.objects.get(slug=game_slug)
    rows= Row.objects.all().filter(game=game)
    users = game.users.all().order_by('id')
    scores = Score.objects.filter(game=game)

    context_dict = {}
    context_dict["rows"] = rows
    context_dict["users"] = users
    context_dict["scores"] = scores
    context_dict["game"] = game

    response = render(request, 'scoretracker/game.html', context=context_dict)
    return response

@login_required
def add_scores(request,game_slug):
    if request.method == "POST":
        game = Game.objects.get(slug=game_slug)
        users = game.users.all()

        row = Row(game=game)
        row.save_no_cols()

        for user in users:
            print(request.POST.get(f'{user.username}_score'))
            col = Column(user=user,row=row,value=int(request.POST.get(f'{user.username}_score')))
            col.save()
        
        # row.save()

    return redirect(reverse('scoretracker:view_game', kwargs={'game_slug':game_slug}))


@login_required
def add_game(request):

    if request.method == "POST":
        posted_form = GameForm(request.POST)
        if posted_form.is_valid():
            print(posted_form.cleaned_data['users'])
            f = posted_form.save()
            f.save()
            return redirect(reverse('scoretracker:view_game', kwargs={'game_slug':f.slug}))
        else:
            return render(request, 'scoretracker/add_game.html',{'form':posted_form})
    else:
        form = GameForm()

        return render(request, 'scoretracker/add_game.html',{'form':form})

    # users = User.objects.all()


def register(request):

    if request.method == "POST":
        user_form = UserForm(request.POST) 
        
        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)

            return redirect(reverse('scoretracker:index'))
        else:
            print(user_form.errors)
    else: 
        user_form = UserForm()
    
    return render(request,template_name='scoretracker/auth/register.html',context={'user_form':user_form})


def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # login_form = LoginForm(request.POST)

        # if login_form.is_valid():
        #     print(login_form)
        #     print(login_form.data.get('password'))

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('scoretracker:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}")
            return HttpResponse("Invalid login details supplied.")
    else:
        login_form = LoginForm()
        return render(request, 'scoretracker/auth/login.html', context={'login_form':login_form})

@login_required
def user_profile(request):

    return render(request,'scoretracker/profile.html')


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    # print('logout out')
    return redirect(reverse('scoretracker:index'))
    # return HttpResponseRedirect('/scoretracker/login/')

@login_required
def view_stats(request):
    game = Game.objects.get(name='GHS')
    games = game.get_score_for_user(request.user)

    users = game.users.all()

    return render(request,'scoretracker/view_stats.html',context={'game':game,'users':users})


def gen_url(request):
    fig, ax = plt.subplots()
    print(request.GET)
    other = request.GET.get('otheruser')
    response = HttpResponse(content_type='image/png')
    
    scores = {}
    for row in Game.objects.get(name='GHS').rows:
        for col in row.columns:
            user_score = scores.get(col.user.username,[])
            user_score.append(col.value)
            scores[col.user.username] = user_score

    ax.plot(scores[request.user.username], scores[other],'.')
    flike = io.BytesIO()
    fig.savefig(response)
    # plt.savefig('/tmp/generated_image_blahblah.png')

    # with open('/tmp/generated_image_blahblah.png', 'rb') as file:
    #     return HttpResponse(content=file)
    return response

