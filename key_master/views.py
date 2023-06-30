from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.list import ListView
from .models import Aluguel,Funcionario,Chave
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

# Create your views here.


def index(request):
    return render(request, 'index.html')

def sucess_devolver(request):
    return render(request, 'sucess_devolver.html')


def sucess(request):
    return render(request, 'sucess.html')

@login_required
def listar_chaves_disponiveis(request):
    chaves_disponoveis = Chave.objects.filter(disponivel=True)
    return render(request, 'listar_chaves_disponiveis.html', {'chaves': chaves_disponoveis})




@login_required
def listar_chaves_alugadas(request):
    usuario = request.user.funcionario
    chaves_alugadas = Chave.objects.filter(alugueis__usuario=usuario, alugueis__data_devolucao__isnull=True, alugueis__chave__disponivel=False)
    
    
    return render(request, 'listar_chaves_alugadas.html', {'chaves': chaves_alugadas})



@login_required
def alugar_chave(request, chave_id):
    chave = Chave.objects.get(id=chave_id)
    if chave.disponivel:
        usuario = request.user.funcionario
        aluguel_chave = Aluguel.objects.create(chave=chave, usuario=usuario)
        chave.disponivel = False
        chave.save()
        aluguel_chave.save()
        return redirect('sucess')
    else:
        messages.error(request, 'Essa chave não está disponível.')
        return redirect('listar_chaves_disponiveis')
    
    
 
@login_required 
def devolver_chave(request, chave_id):
    usuario = request.user.funcionario
    aluguel_chave = Aluguel.objects.filter(chave_id=chave_id, usuario=usuario, data_devolucao__isnull=True).first()
    
    if aluguel_chave:
        aluguel_chave.data_devolucao = timezone.now()
        aluguel_chave.save()
        
        chave = aluguel_chave.chave
        chave.disponivel = True
        chave.save()
        
        return redirect('sucess_devolver')
    else:
        messages.error(request, 'Não foi possível encontrar o registro do aluguel desta chave.')
        return redirect('listar_chaves_alugadas')   
# @login_required
# def devolver_chave(request, chave_id):
#     chave = Chave.objects.get(id=chave_id)
#     aluguel = chave.alugueis.all()[0]

#     if chave.disponivel == False:
#         chave.disponivel = True
#         chave.save()

#         aluguel.data_devolucao = timezone.now()
#         aluguel.save()

#     return redirect('sucess')


class AluguelListView(ListView):
    model = Aluguel
    template_name = 'listar_alugueis.html'
    context_object_name = 'alugueis'