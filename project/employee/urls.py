from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('add/', views.AddView.as_view(), name='add'),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('update/<int:pk>/', views.UpdateView.as_view(), name='update')
]