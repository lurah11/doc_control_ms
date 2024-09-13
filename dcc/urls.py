from django.urls import path
from . import views


app_name="dcc"

urlpatterns = [
    path('',views.HomeView.as_view(), name='home-view'),
    path('document',views.DocumentListView.as_view(),name='document-list-view'),
    path('document/<int:pk>',views.DocumentDetailView.as_view(),name='document-detail-view'),
    path('document/create',views.DocumentCreateView.as_view(),name='document-create-view')
]