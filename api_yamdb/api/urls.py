from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet, TitleViewSet, CategoryViewSet, GenreViewSet, SignupView

router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

auth_urls = [
    path('signup/', SignupView.as_view()),
]

v1_urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urls))
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
