from django.urls import path

from . import views


urlpatterns = [
    path('brands/', views.BrandsList.as_view(), name='create-list-brands'),
    path('brands/<int:id>', views.BrandDetail.as_view(), name='detail-update-delete-brand'),
    path('rules/', views.RulesList.as_view(), name='create-list-rules'),
    path('rules/<int:id>', views.RuleDetail.as_view(), name='detail-update-delete-rule'),
]
