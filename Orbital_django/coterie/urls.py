from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^handle_create_coterie', views.handle_create_coterie, name="handle_create_coterie"),

    url(r'^handle_apply_coterie', views.handle_apply_coterie, name="handle_apply_coterie"),

    url(r'^handle_join_coterie', views.handle_join_coterie, name="handle_join_coterie"),

    url(r'^handle_quit_coterie', views.handle_quit_coterie, name="handle_quit_coterie"),

    url(r'^handle_delete_coterie', views.handle_delete_coterie, name="handle_delete_coterie"),

    # coterie document related action
    url(r'^handle_coteriefile_upload', views.handle_coteriefile_upload, name="handle_coteriefile_upload"),

    url(r'^handle_coteriefile_delete', views.handle_coteriefile_delete, name="handle_coteriefile_delete"),

    url(r'^display_coteriefile_viewer_page', views.display_coteriefile_viewer_page, name="display_coteriefile_viewer_page"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
