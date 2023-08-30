from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Instancia

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('signin')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['senha']
        )

        if user.is_authenticated:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuário ou senha incorretos'
            })

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['confirmarSenha'] == request.POST['senha']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                               first_name=request.POST['nome'],
                                               last_name=request.POST['sobrenome'],
                                               email=request.POST['email'],
                                               password=request.POST['senha'])
                user.save()
                login(request, user)
                return redirect('signin')
            except:
                return render(request, 'signup.html', {
                            'form' : UserCreationForm,
                            'error' : 'Usuário Já Existe'
                            })
            
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'As senhas são diferentes'
        })

def signout(request):
    logout(request)
    return redirect('signin')

def predictor(request):
    if request.method == 'GET':
        return render(request, 'predict.html')
    elif request.method == 'POST':
        instancia = Instancia()
        instancia.nome_instancia = request.POST['nome_instancia']
        instancia.temperatura = request.POST['temperatura']
        instancia.umidade_ar = request.POST['umidade_ar']
        instancia.umidade_solo = request.POST['umidade_solo']
        instancia.tipo_solo = request.POST['tipo_solo']
        instancia.tipo_cultura = request.POST['tipo_cultura']
        instancia.nitrogenio = request.POST['nitrogenio']
        instancia.potassio = request.POST['potassio']
        instancia.fosforo = request.POST['fosforo']
        instancia.id_usuario = request.user

        instancia.save()
        return redirect('result')


def result(request):
    return render(request, 'result.html')