from django.urls import path
from . import views
from django.views.generic.base import TemplateView
from .views import SignUpView
from .views import DeleteUserView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("your-name/", views.get_name, name = 'get_name'),
    path("thanks/", views.result_page, name = 'result_page'),
    path("your-feedback/", views.get_feedback, name = 'get_feedback'),
    path("feedbacks/", views.result_feedbacks, name = 'result_feedbacks'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('delete_user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    path('users/', views.user_list, name='user_list'),
    path('confirm_delete_user/<int:user_id>/', views.ConfirmDeleteUserView.as_view(), name='confirm_delete_user'),  # URL for user deletion confirmation
]
