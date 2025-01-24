from django.urls import path
from . import views
from .views import ConversationViewSet,MessageViewSet
from rest_framework.routers import DefaultRouter




# urlpatterns = [
#     path('conversations/', views.ConversationList.as_view()),
#     path('conversations/<int:pk>/', views.ConversationDetail.as_view()),
#     path('conversations/<int:pk>/messages/', views.MessageList.as_view()),
#     path('conversations/<int:pk>/messages/<int:msg_pk>/', views.MessageDetail.as_view()),
# ]


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'conversations/(?P<conversation_id>[^/.]+)/messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]

["routers.DefaultRouter()"]
