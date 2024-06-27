from django.urls import path, include
from core import views
from .views import LikeView, AddQueryView


urlpatterns = [
    path('',views.index,name="index"),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('logout',views.logout,name='logout'),
    path('blog',views.blog,name='blog'),
    path('post/<slug>/',views.posts,name='posts'),
    path('save',views.save,name='save'),
    path('pquery',views.pquery,name="pquery"),
    path('addquery',AddQueryView.as_view(),name="addquery"),
    path('psave',views.psave,name="psave"),
    path('pcomment/<int:pk>',views.pcomment,name="pcomment"),
    path('pcomment/csave',views.csave,name="csave"),
    path('knowscore',views.knowscore,name='knowscore'),
    path('score_result',views.score_result,name='score_result'),
    path('Diet', views.diet,name="Diet"),
    path('dietres',views.dietres,name='dietres'),
    path('doctors', views.doctors,name="doctors"),
    path('dprofile/<slug>/',views.dprofile, name='dprofile'),
    path('meeting',views.videocall, name='meeting'),
    path('gencode',views.gencode, name='gencode'),
    path('subscription/<int:plan_id>/',views.subscription, name='subscription'),
    path('plan',views.plan, name='plan'),
    path('premium',views.premium, name='premium'),
    path('payment_process',views.payment_process, name='payment_process'),
    path('create_subscription/', views.create_subscription, name='create_subscription'),
    path('home',views.home,name='home'),
    path('genroom',views.genroom, name='genroom'),
    path('<str:room>/',views.room,name='room'),
    path('send',views.send,name='send'),
    path('getMessages/<str:room>/',views.getMessages,name='getMessages'),

]