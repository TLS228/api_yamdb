from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet

router_v1 = routers.DefaultRouter()
# router.register('groups', GroupViewSet)
# router.register(
#     r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
# )
# router.register('posts', PostViewSet)
# router.register('follow', FollowViewSet, basename='follow')

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

auth_urls = [
    # path('signup/'),
    # path('token/')
]

v1_urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urls))
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
