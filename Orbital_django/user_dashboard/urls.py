from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.display_user_dashboard, name="user_dashboard"),

    url(r'^friends_page', views.display_friends_page, name="friends_page"),

    url(r'^group_page', views.display_group_page, name="group_page"),

    url(r'^friend_page', views.display_friend_page, name="friend_page"),

    url(r'^handle_log_out', views.handle_log_out, name="log_out"),

    url(r'^handle_file_upload', views.handle_file_upload, name="file_upload"),

    url(r'^handle_delete', views.handle_delete, name="delete_document"),

    url(r'^handle_uncollect', views.handle_uncollect, name="uncollect_document"),

    url(r'^change_portrait', views.change_portrait, name="change_portrait"),

    url(r'^handle_follow_user', views.handle_follow_user, name="handle_follow_user"),

    url(r'^handle_unfollow_user', views.handle_unfollow_user, name="handle_unfollow_user"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
