from django.urls import path
from . import views
from django.views.generic.base import TemplateView
from .views import SignUpView, DeleteUserView


urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("feedbacks/form/", views.get_feedback, name = 'get_feedback'),
    path("feedbacks/", views.result_feedbacks, name = 'result_feedbacks'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('delete_user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    path('users/', views.user_list, name='user_list'),
    path('confirm_delete_user/<int:user_id>/', views.ConfirmDeleteUserView.as_view(), name='confirm_delete_user'),  # URL for user deletion confirmation
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile_field'),
    path('feedbacks/<int:id_feedback>/', views.feedback_view, name='feedback_view'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    

]
