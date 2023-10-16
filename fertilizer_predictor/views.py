from datetime import date
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
import pandas as pd
from .models import Instancia, Resultado, Descricao, InstanciaCrop
from django.core.paginator import Paginator

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
    return render(request, 'fertilizante/result.html', {"resultado": resultado})

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

from .forms import ParametrosForm, ParametrosFormCrop

def create_instancia(request):
    if request.method == 'POST':
        form = ParametrosForm(request.POST)
        if form.is_valid():
            instancia = Instancia(
                nome_instancia=form.cleaned_data['nome_instancia'],
                temperatura=form.cleaned_data['temperatura'],
                umidade_ar=form.cleaned_data['umidade_ar'],
                umidade_solo=form.cleaned_data['umidade_solo'],
                tipo_solo=form.cleaned_data['tipo_solo'],
                tipo_cultura=form.cleaned_data['tipo_cultura'],
                nitrogenio=form.cleaned_data['nitrogenio'],
                fosforo=form.cleaned_data['fosforo'],
                potassio=form.cleaned_data['potassio'],
                id_usuario=request.user,
                data=date.today()
            )
            instancia.save()
            resultado = predict_fertilizer(instancia)
            return result(request, resultado.id_resultado)
    else:
        form = ParametrosForm()
        lista_instancia = Instancia.objects.filter(id_usuario=request.user)

        p = Paginator(lista_instancia, 7)
        page = request.GET.get('page')
        instancias = p.get_page(page)

        return render(request, 'fertilizante/create-instance.html', {'form': form, 'lista_instancia': lista_instancia, 'instancias': instancias})

    
def history(request):
    if request.user.is_authenticated:
        lista_instancia = Instancia.objects.filter(id_usuario=request.user)
        for i in lista_instancia:
            resultados = Resultado.objects.filter(id_instancia=i)

        p = Paginator(lista_instancia, 7)
        page = request.GET.get('page')
        instancias = p.get_page(page)

        return render(request, 'history.html', {'lista_instancia': lista_instancia, 'instancias': instancias})
    
def edit_instancia(request, id_instancia):
    instancia = Instancia.objects.get(id_usuario=request.user, id_instancia=id_instancia)
    if request.method == 'POST':
        form = ParametrosForm(request.POST or None, instance=instancia)
        if form.is_valid():
            instancia = Instancia(
                nome_instancia=form.cleaned_data['nome_instancia'],
                temperatura=form.cleaned_data['temperatura'],
                umidade_ar=form.cleaned_data['umidade_ar'],
                umidade_solo=form.cleaned_data['umidade_solo'],
                tipo_solo=form.cleaned_data['tipo_solo'],
                tipo_cultura=form.cleaned_data['tipo_cultura'],
                nitrogenio=form.cleaned_data['nitrogenio'],
                fosforo=form.cleaned_data['fosforo'],
                potassio=form.cleaned_data['potassio'],
                id_usuario=request.user,
                data=date.today()
            )
            instancia.save()
            resultado = predict_fertilizer(instancia)
            return result(request, resultado.id_resultado)
    else:
        form = ParametrosForm(instance=instancia)
        lista_instancia = Instancia.objects.filter(id_usuario=request.user)

        p = Paginator(lista_instancia, 7)
        page = request.GET.get('page')
        instancias = p.get_page(page)

    return render(request, 'fertilizante/update-instance.html', {'form': form, 'instancia': instancia, 'lista_instancia': lista_instancia, 'instancias': instancias})


def create_instancia_crop(request):
    if request.method == 'POST':
        form = ParametrosFormCrop(request.POST)
        if form.is_valid():
            instancia = InstanciaCrop(
                nome_instancia=form.cleaned_data['nome_instancia'],
                temperatura=form.cleaned_data['temperatura'],
                umidade=form.cleaned_data['umidade'],
                nitrogenio=form.cleaned_data['nitrogenio'],
                fosforo=form.cleaned_data['fosforo'],
                potassio=form.cleaned_data['potassio'],
                ph=form.cleaned_data['ph'],
                chuva=form.cleaned_data['chuva'],
                id_usuario=request.user,
                data=date.today()
            )
            instancia.save()
    else:
        form = ParametrosFormCrop()
        lista_instancia = InstanciaCrop.objects.filter(id_usuario=request.user)

        p = Paginator(lista_instancia, 7)
        page = request.GET.get('page')
        instancias = p.get_page(page)

        return render(request, 'crop/create-instance-crop.html', {'form': form, 'lista_instancia': lista_instancia, 'instancias': instancias})

def history_crop(request):
    if request.user.is_authenticated:
        lista_instancia = InstanciaCrop.objects.filter(id_usuario=request.user)

        p = Paginator(lista_instancia, 7)
        page = request.GET.get('page')
        instancias = p.get_page(page)

        return render(request, 'history.html', {'lista_instancia': lista_instancia, 'instancias': instancias})

def edit_instancia_crop(request, id_instancia):
    instancia = InstanciaCrop.objects.get(id_usuario=request.user, id_instancia=id_instancia)
    if request.method == 'POST':
        form = ParametrosFormCrop(request.POST or None, instance=instancia)
        if form.is_valid():
            instancia = InstanciaCrop(
                nome_instancia=form.cleaned_data['nome_instancia'],
                temperatura=form.cleaned_data['temperatura'],
                umidade=form.cleaned_data['umidade'],
                nitrogenio=form.cleaned_data['nitrogenio'],
                fosforo=form.cleaned_data['fosforo'],
                potassio=form.cleaned_data['potassio'],
                ph=form.cleaned_data['ph'],
                chuva=form.cleaned_data['chuva'],
                id_usuario=request.user,
                data=date.today()
            )
            instancia.save()
    else:
        form = ParametrosFormCrop(instance=instancia)
        lista_instancia = InstanciaCrop.objects.filter(id_usuario=request.user)

        p = Paginator(lista_instancia, 7)
        page = request.GET.get('page')
        instancias = p.get_page(page)

    return render(request, 'crop/update-instance-crop.html', {'form': form, 'instancia': instancia, 'lista_instancia': lista_instancia, 'instancias': instancias})
