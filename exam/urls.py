from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('exam/<int:exam_id>/', views.exam_page, name='exam'),
    path('logout/', views.logout_view, name='logout'),
    path('instructions/<int:exam_id>/', views.instructions, name='instructions'),

]
