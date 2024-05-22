from django.urls import path, include
from rest_framework import routers

from .views import BoothViewSet, CommentViewSet

app_name = 'booth'

booth_router = routers.SimpleRouter(trailing_slash=False)
booth_router.register('booth', BoothViewSet, basename='booth')

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(booth_router.urls)),
    path('booth/<int:id>/', include(comment_router.urls)),
    path('', include(comment_router.urls)),
]