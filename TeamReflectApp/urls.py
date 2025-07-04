from django.urls import path
from . import views
from django.views.generic.base import TemplateView
from .views import SignUpView, DeleteUserView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("feedback/form/", views.feedback_form, name = 'feedback_form'),
    path("feedback/form/partfill", lambda request: views.feedback_form(request, is_prefilled=True),  name = 'feedback_form_partfill'),
    path("feedback/list/", views.feedback_list, name = 'feedback_list'),
    path("feedback/results/", views.feedback_list, name='result_feedbacks'),
    path("feedback/add/", views.feedback_form, name="get_feedback"),
    path('feedback/<int:id_feedback>/', views.feedback_view, name='feedback_view'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('delete_user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    path('users/', views.user_list, name='user_list'),
    path('confirm_delete_user/<int:user_id>/', views.ConfirmDeleteUserView.as_view(), name='confirm_delete_user'),  # URL for user deletion confirmation
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile_field'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('post/', views.leader_post_form, name='leader_post_form'), #Rename these
    path('post/write_post', views.leader_post, name='leader_post'),
    path('post/write_comment', views.comment_post, name='comment_post'),
    path('post/<int:post_id>', views.post_view, name='post_view'),
    path('post/list/', views.post_list, name='post_list'),
    path('post/vote/<int:item_id>/', views.vote_poll_item, name='vote_poll_item'),
    path('leader-post/<int:post_id>/', views.leader_post_detail, name='leader_post_detail'),
    path('generate-report/<int:post_id>/', views.generate_leader_report, name='generate_report'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

