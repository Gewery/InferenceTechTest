from django.urls import path
from messaging.views import *

app_name = "messaging"

urlpatterns = [
    path('create/', MessageCreateView.as_view()),
    path('all/', MessagesListView.as_view()),
    path('all/<int:pk>/', MessagesToUserListView.as_view()),
    path('detail/<int:pk>/', MessageDetailView.as_view()),
]
