from django.conf.urls import url
from . import views

urlpatterns = [
    url('conference/', views.ConferenceDetails.as_view()),
    url('talks/',views.TalkDetails.as_view()),
    url('edit-people/',views.AddRemovePublic.as_view()),
    url('edit-talk/',views.EditTalk.as_view())
    
]