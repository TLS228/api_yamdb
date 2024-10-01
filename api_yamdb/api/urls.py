from django.urls import include, path

from .views import SignupView


auth_urls = [
    path('signup/', SignupView.as_view()),
    #path('token/')
]

urlpatterns = [
    path('v1/auth/', include(auth_urls))
]
