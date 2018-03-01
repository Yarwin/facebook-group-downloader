from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.HomeListView.as_view(),
         name='index'),
    path('get-group/', views.get_group, name='get-group'),
    path('group/<str:group>/', views.GroupListView.as_view(), name='group-list-view'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
