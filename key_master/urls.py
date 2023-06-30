from django.urls import path
from key_master import views


urlpatterns = [
    path('chaves/devolver/<int:chave_id>/',views.devolver_chave, name='devolver_chave'),
    path('',views.index,name='index'),
    path('sucess_devolver/',views.sucess_devolver,name='sucess_devolver'),
    path('listar/alugadas',views.listar_chaves_alugadas,name='listar_chaves_alugadas'),
    path('listar/disponiveis',views.listar_chaves_disponiveis,name='listar_chaves_disponiveis'),
    path('chaves/pegar/<int:chave_id>/',views.alugar_chave,name='alugar_chave'),
    path('sucess/',views.sucess,name='sucess'),
    path('aluguel/',views.AluguelListView.as_view(),name='listar_aluguel'),
    
    
    
]