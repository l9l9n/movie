from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import MovieListView, MovieDetailView, ReviewCreateView

urlpatterns = [
    path("movie/", MovieListView.as_view()),
    path("movie/<int:pk>/", MovieDetailView.as_view()),
    path("review/", ReviewCreateView.as_view()),

]



#     path("movie/", views.MovieViewSet.as_view({'get': 'list'})),
#     path("movie/<int:pk>/", views.MovieViewSet.as_view({'get': 'retrieve'})),
#     path("review/", views.ReviewCreateViewSet.as_view({'post': 'create'})),
#     path("rating/", views.AddStarRatingViewSet.as_view({'post': 'create'})),
#     path('actor/', views.ActorsViewSet.as_view({'get': 'list'})),
#     path('actor/<int:pk>/', views.ActorsViewSet.as_view({'get': 'retrieve'})),