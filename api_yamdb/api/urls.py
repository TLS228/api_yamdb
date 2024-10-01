from django.urls import include, path


auth_urls = [
    path('signup/'),
    path('token/')
]

urlpatterns += [
    path('v1/auth/', include(auth_urls))
]
