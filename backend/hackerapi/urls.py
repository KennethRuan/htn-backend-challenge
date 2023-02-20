from django.urls import path
from .views import HackerView, SkillView

urlpatterns = [
    path('users', HackerView.as_view()),
    path('users/<pk>', HackerView.as_view()),
    path('skills', SkillView.as_view()),
    path('skills/', SkillView.as_view())

]

