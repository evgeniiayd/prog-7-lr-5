from django.urls import path
from . import views

urlpatterns = [
    path('stats/<int:question_id>/', views.voting_stats, name='voting_stats'),
    path('export/<int:question_id>/<str:forma>/', views.export_votes, name='export_votes'),
    path('chart/<int:question_id>/', views.vote_chart, name='vote_chart'),
]
