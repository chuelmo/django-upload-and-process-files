from django.urls import re_path, path
from . import views

# namespace
app_name = "hello"

urlpatterns = [
    re_path(r'^upload/$', views.model_form_upload, name='model_form_upload'),
    re_path(r'^delete/$', views.model_delete, name='model_delete'),
    path('', views.file_list, name='file_list'),
    re_path(r'^download/(?P<id>.*)/$', views.file_response_download, name='file_download'),

]