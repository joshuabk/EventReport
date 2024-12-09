from django.urls import path
from . import views
urlpatterns = [
    path('', views.addReport, name='addReport'),
    path('login/',  views.loginUser, name = 'login' ),
    path('logout/',  views.logoutUser, name = 'logout' ),
    path('showReports/', views.showReports, name='showReports'),
    path('editReport/<int:report_id>', views.editReport, name='editReport'),
    path('deleteReport/<report_id>',views.deleteReport, name='deleteReport'),
    path('showSingleReport/<report_id>',views.showSingleReport, name='showSingleReport'),
   
   
]