from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy, path

from alarms import views



urlpatterns = [

#########################################################################    
################  PLANB 

    path('index/',views.index,name="index"),
    
    
    ###  USERS module

    path('usuarios/',views.users_list,name="usuarios"),
    path('usuario/add/',views.useradd,name="useradd"),    
    path('usuario/<uuid:pk>/',views.usuario_detail, name="usuario"),
    path('usuario/<uuid:pk>/delete/',views.usuario_delete, name="usuariodelete"),
    
  ###  ALARMS ALERTS module
    path('alarmas/user/<uuid:pk>', views.alertas, name="usuarioalertas"),

    
    path('alarmas/', views.alertas, name="alertas"),
    
    # ajax monitoreo de alarmas
    path('alarmas/latest/', views.latest, name='latest'),
    path('alarmas/has_new_data/', views.has_new_data, name='has_new_data'),
    path('api/alarms/', views.AlarmaEventAPIView.as_view(), name='apialarm'),



  ###  BARRIOS VIVIENDA  module

    path('barrios/',views.barrios_list, name="barrios"),
    path('barrio/add/',views.barrioadd,name="barrioadd"),    

    path('barrio/<uuid:pk>/delete/',views.barrio_delete, name="barriodelete"),
    path('barrio/<uuid:pk>/',views.barrio_detail, name="barrio"),
    path('barrio/<uuid:pk>/change/',views.barrio_edit, name="barrioedit"),
    path('usuarios/<uuid:pk>/',views.users_list,name="usuariosbarrio"),

    path('vivienda/<uuid:pk>/delete/',views.vivienda_delete, name="viviendadelete"),
    path('vivienda/<uuid:pk>/',views.vivienda_detail, name="vivienda"),
    path('vivienda/<uuid:pk>/change/',views.vivienda_edit, name="viviendaedit"),
    path('vivienda/add/',views.viviendaadd,name="viviendaadd"),    
    

################   end PLANB += index


#########################################################################3    
    

    #CMS_End-----------------
    path('',views.index,name="index"),
    path('index/',views.index,name="index"),
    
    
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('dashboard:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]