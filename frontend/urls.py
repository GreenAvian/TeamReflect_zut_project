from django.urls import path
from frontend import views

urlpatterns = [
    path("", views.home, name="home"),
    path("your-name/", views.get_name, name = 'get_name'),
    path("thanks/", views.result_page, name = 'result_page'),
]
