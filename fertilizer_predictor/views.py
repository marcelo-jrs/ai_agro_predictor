from datetime import date
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
import pandas as pd
import pickle
from .models import Instancia, Resultado, Descricao

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

def result(request, id_resultado):
    resultado = Resultado.objects.get(id_resultado=id_resultado)
    return render(request, 'result.html', {"resultado": resultado})

def predict_fertilizer(instancia):
    model = pd.read_pickle(r"C:\Users\Usuário\Facul\Estágio\Estagio II\fertilizer-app\notebook_fertilizer_precidtor\classifier.pkl")

    temperatura = instancia.temperatura;
    umidade_ar = instancia.umidade_ar;
    umidade_solo = instancia.umidade_solo;
    tipo_solo = instancia.tipo_solo;
    tipo_cultura = instancia.tipo_cultura;
    nitrogenio = instancia.nitrogenio;
    potassio = instancia.potassio;
    fosforo = instancia.fosforo;

    result = model.predict([[temperatura, umidade_ar, umidade_solo, tipo_solo, tipo_cultura, nitrogenio, potassio, fosforo]])

    if result[0] == 0:
        tipo_fertilizante = "10-26-26"
        id_descricao = 0
    elif result[0] ==1:
        tipo_fertilizante = "14-35-14"
        id_descricao = 1
    elif result[0] == 2:
        tipo_fertilizante = "17-17-17"
        id_descricao = 2
    elif result[0] == 3:
        tipo_fertilizante = "20-20"
        id_descricao = 3
    elif result[0] == 4:
        tipo_fertilizante = "28-28"
        id_descricao = 4
    elif result[0] == 5:
        tipo_fertilizante = "DAP"
        id_descricao = 5
    else:
        tipo_fertilizante = "Urea"
        id_descricao = 6

    descricao = Descricao.objects.get(id_fertilizante=id_descricao)

    resultado = Resultado.objects.create(tipo_fertilizante=tipo_fertilizante, data=date.today(), id_instancia=instancia, id_descricao=descricao)
    resultado.save()

    return resultado


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

        resultado = predict_fertilizer(instancia)

        return result(request, resultado.id_resultado)
