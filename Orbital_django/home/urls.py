from django.conf.urls import url, include
from . import views

urlpatterns = [
    # urls that go to the home page
    url(r'^$', views.display_home_page, name = "home"),

    # urls that go to the sign_up_page
    url(r'^sign_up', views.display_sign_up_page, name = "sign_up"),

    # urls for the forms submitting
    url(r'^handle_sign_up', views.handle_sign_up, name = "handle_sign_up"),

    # urls for log_in
    url(r'^handle_log_in', views.handle_log_in, name = "handle_log_in"),

    url(r'^handle_nus_log_in', views.handle_nus_log_in, name = "handle_nus_log_in"),

    url(r'^handle_search', views.handle_search, name = "handle_search"),
]
