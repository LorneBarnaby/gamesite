from django.urls import path
from scoretracker import views

app_name = 'scoretracker'


urlpatterns = [
    path('',views.index,name='index'),
    path('game/<slug:game_slug>/',views.view_game,name='view_game'),
    path('game/<slug:game_slug>/add_score',views.add_scores,name="add_scores"),
    path('add_game/',views.add_game,name='add_game'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('profile/',views.user_profile,name='profile'),
    path('logout/',views.user_logout,name='logout'),
    path('my_stats/',views.view_stats,name='view_stats'),
    path('gen_graph/',views.gen_url,name='gen_graph'),
]