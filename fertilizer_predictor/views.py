from datetime import date
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
import pandas as pd
from .models import Instancia, Resultado, Descricao, InstanciaCrop, ResultadoCrop
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

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_chart_compare(column, title):
    data = pd.read_csv(r"C:\Users\Usuário\Facul\Estágio\Estagio II\fertilizer-app\notebook_fertilizer_precidtor\testes\Fertilizer Prediction.csv")

    fig = go.Figure()


    fig.add_trace(go.Box(x=data['Fertilizer Name'], y=data[column], boxmean=True, boxpoints='all'))

    # Personalize rótulos e título
    fig.update_layout(
        xaxis_title='Fertilizer Name',
        yaxis_title=column,
        title=title
    )
    chart = fig.to_html()

    return chart

def create_boxplot(x_column, y_column, title):
    data = pd.read_csv(r"C:\Users\Usuário\Facul\Estágio\Estagio II\fertilizer-app\notebook_fertilizer_precidtor\testes\Fertilizer Prediction.csv")
    fig = px.box(data, x=x_column, y=y_column)

    # Personalize os rótulos e o título
    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column,
        title=title
    )
    chart = fig.to_html()

    return chart

def result(request, id_resultado):
    resultado = Resultado.objects.get(id_resultado=id_resultado)
    instance = resultado.id_instancia
    chart_nitro = create_chart_compare('Nitrogen', 'Influência do Nitrogênio')
    chart_potassium = create_chart_compare('Potassium', 'Influência do Potássio')
    chart_phosphorous = create_chart_compare('Phosphorous', 'Influência do Fósforo')
 
    return render(request, 'fertilizante/result.html', {"resultado": resultado, "chart_nitro": chart_nitro, 'chart_potassium':chart_potassium, 'chart_phosphorous':chart_phosphorous,"instance": instance})

def predict_fertilizer(instancia, user):
    model = pd.read_pickle(r"C:\Users\Usuário\Facul\Estágio\Estagio II\fertilizer-app\ai_agro_predictor\fertilizer_predictor\classifier\classifier_fert.pkl")

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

    resultado = Resultado.objects.create(tipo_fertilizante=tipo_fertilizante, data=date.today(), id_instancia=instancia, id_descricao=descricao, id_usuario=user)
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
            resultado = predict_fertilizer(instancia, request.user)
            return result(request, resultado.id_resultado)
    else:
        form = ParametrosForm()
        lista_instancia = Instancia.objects.filter(id_usuario=request.user)

        p = Paginator(lista_instancia, 7)
        page = request.GET.get('page')
        instancias = p.get_page(page)

        return render(request, 'fertilizante/create-instance.html', {'form': form, 'lista_instancia': lista_instancia, 'instancias': instancias})

    
def history(request, tipo):
    if request.user.is_authenticated:
        if tipo == 'fertilizante':
            instancias = Instancia.objects.filter(id_usuario=request.user)
            resultados = Resultado.objects.filter()
            lista = Resultado.objects.filter(id_usuario=request.user)
        elif tipo == 'cultura':
            instancias = InstanciaCrop.objects.filter(id_usuario=request.user)
            resultados = ResultadoCrop.objects.filter()
            lista = ResultadoCrop.objects.filter(id_usuario=request.user)

        p = Paginator(lista, 7)
        page = request.GET.get('page')
        pages = p.get_page(page)

        return render(request, 'history.html', {'lista': lista, 'pages': pages, 'resultados': resultados, 'instancias': instancias})

def edit_instancia(request, id_instancia):
    instancia = Instancia.objects.get(id_usuario=request.user, id_instancia=id_instancia)
    if request.method == 'POST':
        form = ParametrosForm(request.POST or None, instance=instancia)
        if form.is_valid():
            instancia.nome_instancia = form.cleaned_data['nome_instancia']
            instancia.temperatura = form.cleaned_data['temperatura']
            instancia.umidade_ar = form.cleaned_data['umidade_ar']
            instancia.umidade_solo = form.cleaned_data['umidade_solo']
            instancia.tipo_solo = form.cleaned_data['tipo_solo']
            instancia.tipo_cultura = form.cleaned_data['tipo_cultura']
            instancia.nitrogenio = form.cleaned_data['nitrogenio']
            instancia.fosforo = form.cleaned_data['fosforo']
            instancia.potassio = form.cleaned_data['potassio']
            instancia.data = date.today()
            instancia.save()
            resultado = predict_fertilizer(instancia, request.user)
            return result(request, resultado.id_resultado)
    else:
        form = ParametrosForm(instance=instancia)
        lista_instancia = Instancia.objects.filter(id_usuario=request.user)

        p = Paginator(lista_instancia, 7)
        page = request.GET.get('page')
        instancias = p.get_page(page)

    return render(request, 'fertilizante/update-instance.html', {'form': form, 'instancia': instancia, 'lista_instancia': lista_instancia, 'instancias': instancias})


def crate_chart_crop(column, title):
    data = pd.read_csv(r"C:\Users\Usuário\Facul\Estágio\Estagio II\fertilizer-app\notebook_fertilizer_precidtor\testes\Crop_recommendation.csv")

    fig = go.Figure()


    fig.add_trace(go.Box(x=data['label'], y=data[column], boxmean=True, boxpoints='all'))

    # Personalize rótulos e título
    fig.update_layout(
        xaxis_title='Cultura',
        yaxis_title=column,
        title=title
    )
    chart = fig.to_html()

    return chart

def resultCrop(request, id_resultado):
    resultado = ResultadoCrop.objects.get(id_resultado=id_resultado)

    instance = resultado.id_instancia
    chart_nitro = crate_chart_crop('N', 'Influência do Nitrogênio')
    chart_potassium = crate_chart_crop('P', 'Influência do Potássio')
    chart_phosphorous = crate_chart_crop('K', 'Influência do Fósforo')

    return render(request, 'crop/result-crop.html', {"resultado": resultado, "chart_nitro": chart_nitro, 'chart_potassium':chart_potassium, 'chart_phosphorous':chart_phosphorous,"instance": instance})


def predict_crop(instancia, user):
    model = pd.read_pickle(r"C:\Users\Usuário\Facul\Estágio\Estagio II\fertilizer-app\ai_agro_predictor\fertilizer_predictor\classifier\classifier_crop.pkl")

    temperatura = instancia.temperatura
    umidade = instancia.umidade
    nitrogenio = instancia.nitrogenio
    potassio = instancia.potassio
    fosforo = instancia.fosforo
    ph = instancia.ph
    chuva = instancia.chuva
    [['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
    result = model.predict([[nitrogenio, potassio, fosforo, temperatura, umidade, ph, chuva]])

    if result[0] == 0:
        cultura = 'apple'
    elif result[0] ==1:
        cultura = 'banana'
    elif result[0] == 2:
        cultura = 'blackgram'
    elif result[0] == 3:
        cultura = 'chickpea'
    elif result[0] == 4:
        cultura = 'coconut'
    elif result[0] == 5:
        cultura = 'coffee'
    elif result[0] == 6:
        cultura = 'cotton'
    elif result[0] == 7:
        cultura = 'grapes'
    elif result[0] == 8:
        cultura = 'jute'
    elif result[0] == 9:
        cultura = 'kidneybeans'
    elif result[0] == 10:
        cultura = 'lentil'
    elif result[0] == 11:
        cultura = 'maize'
    elif result[0] == 12:
        cultura = 'mango'
    elif result[0] == 13:
        cultura = 'mothbeans'
    elif result[0] == 14:
        cultura = 'mungbean'
    elif result[0] == 15:
        cultura = 'muskmelon'
    elif result[0] == 16:
        cultura = 'orange'
    elif result[0] == 17:
        cultura = 'papaya'
    elif result[0] == 18:
        cultura = 'pigeonpeas'
    elif result[0] == 19:
        cultura = 'pomegranate'
    elif result[0] == 20:
        cultura = 'rice'
    elif result[0] == 21:
        cultura = 'watermelon'
    

    resultado = ResultadoCrop.objects.create(id_instancia=instancia, cultura=cultura, id_usuario=user)
    resultado.save()

    return resultado



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
            resultado = predict_crop(instancia, request.user)
            return resultCrop(request, resultado.id_resultado, result)
    else:
        form = ParametrosFormCrop()
        lista_instancia = InstanciaCrop.objects.filter(id_usuario=request.user)

        p = Paginator(lista_instancia, 7)
        page = request.GET.get('page')
        instancias = p.get_page(page)

        return render(request, 'crop/create-instance-crop.html', {'form': form, 'lista_instancia': lista_instancia, 'instancias': instancias})

def edit_instancia_crop(request, id_instancia):
    instancia = InstanciaCrop.objects.get(id_usuario=request.user, id_instancia=id_instancia)
    if request.method == 'POST':
        form = ParametrosFormCrop(request.POST or None, instance=instancia)
        if form.is_valid():
            instancia.nome_instancia = form.cleaned_data['nome_instancia']
            instancia.temperatura = form.cleaned_data['temperatura']
            instancia.umidade = form.cleaned_data['umidade']
            instancia.chuva = form.cleaned_data['chuva']
            instancia.ph = form.cleaned_data['ph']
            instancia.nitrogenio = form.cleaned_data['nitrogenio']
            instancia.fosforo = form.cleaned_data['fosforo']
            instancia.potassio = form.cleaned_data['potassio']
            instancia.data = date.today()
            instancia.save()
            resultado = predict_crop(instancia, request.user)
            return resultCrop(request, resultado.id_resultado)
    else:
        form = ParametrosFormCrop(instance=instancia)
        lista_instancia = InstanciaCrop.objects.filter(id_usuario=request.user)

        p = Paginator(lista_instancia, 7)
        page = request.GET.get('page')
        instancias = p.get_page(page)

    return render(request, 'crop/update-instance-crop.html', {'form': form, 'instancia': instancia, 'lista_instancia': lista_instancia, 'instancias': instancias})
