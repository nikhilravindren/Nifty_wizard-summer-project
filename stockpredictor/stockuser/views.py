from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.http import JsonResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import stocks, fundamental,predictors,messages
from datetime import datetime, timedelta
from django.db.models import Q
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import joblib
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your views here.

def user_user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            if user.is_superuser == False and user.is_staff == False:
                login(request, user)
                return redirect('home')
            elif user.is_superuser == False and user.is_staff == True:
                login(request, user)
                return redirect('home')
            else:
                msg = "You are not autherized for the access!"
                return render(request, 'login.html', {'msg': msg})
        else:
            msg = "Wrong credentials"
            return render(request, 'login.html', {"msg": msg})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')


def create_ac(request):
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            msg = 'this username already exists!....'
            return render(request,'register.html',{'msg':msg})
        else:
            password = request.POST['password']
            cpassword = request.POST['cpassword']
            if password == cpassword:
                hashed_password = make_password(password)
                email = request.POST['email']
                User.objects.create(username=username,password=hashed_password,email=email)
                user = user = get_object_or_404(User, username=username)
            else:
                msg = "password and confirm password doesn't match!.. "
                return render(request,'register.html',{'msg':msg})
            return redirect('login')
    return render(request,'register.html')

def home(request):
    return render(request, 'index.html')

def stock(request):
    all_datas = stocks.objects.all().order_by('id')
    paginator = Paginator(all_datas, 10)  # Show 10 datas per page

    page = request.GET.get('page')
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    return render(request, 'stocks.html', {"datas": datas})

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'service.html')

def why(request):
    return render(request, 'why.html')

def data_fetch(symbol):
    end_date = pd.Timestamp.now()  
    start_date = end_date - pd.DateOffset(months=2)  
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    last_30_trading_days = stock_data['Close'].round(2).tail(30).tolist()
    date = list(stock_data.tail(30).index)
    return last_30_trading_days, date


def predict(symbol,data):
    stock = get_object_or_404(stocks, symbol=symbol)
    predictor = get_object_or_404(predictors, stock=stock)

    loaded_model = joblib.load(predictor.model)
    loaded_scaler = joblib.load(predictor.scalar) 
    new_data = np.array(data).reshape(-1, 1)

    new_data_scaled = loaded_scaler.transform(new_data)
    new_data_scaled = np.reshape(new_data_scaled, (1, new_data_scaled.shape[0], 1))
    predicted_price = loaded_model.predict(new_data_scaled)
    predictions = loaded_scaler.inverse_transform(predicted_price)
    formatted_number = format(float(predictions[0][0]), ".2f")
    return formatted_number

def predicting_1(request, symbol):
    price, date = data_fetch(symbol)
    del price[:10]
    prediction = predict(symbol, price)
    request.session['prediction'] = float(prediction)+(float(prediction)*0.005)
    return redirect('stock_details', symbol=symbol)

# def predicting_7(request, symbol):
#     price, date = data_fetch(symbol)
#     del price[:10]
#     prediction = predict(symbol, price)
#     for i in range(4):
#         price.pop(0)
#         price.append(float(prediction)+(float(prediction)*0.005))
#         prediction = predict(symbol, price)
#     request.session['prediction'] = prediction
#     return redirect('stock_details', symbol=symbol)

    
# def predicting_30(request, symbol):
#     price, date = data_fetch(symbol)
#     del price[:10]
#     prediction = predict(symbol, price)
#     for i in range(21):
#         price.pop(0)
#         price.append(float(prediction)+(float(prediction)*0.005))
#         prediction = predict(symbol, price)

#     request.session['prediction'] = prediction
#     return redirect('stock_details', symbol=symbol)      

def stock_detail(request, symbol):
    price, date = data_fetch(symbol)
    prediction = request.session.get('prediction')
    if prediction:
        del request.session['prediction']
    
    date_str = [d.strftime('%Y-%m-%d') for d in date]
    value = 2
    if prediction:
        if float(price[-1]) < float(prediction):
            value = 1
        else:
            value = 0
    context = {
        'symbol': symbol,
        'price': price[-1],
        'prices': price,
        'dates': date_str,
        'value':value,
    }

    stock = get_object_or_404(stocks, symbol=symbol)
    fun = get_object_or_404(fundamental,stock=stock)
    return render(request, 'stock_details.html', {'context': context, 'fundamental': fun, 'stock': stock,'prediction': prediction})

def search_stock(request):
    if request.method == 'POST':
        want = request.POST.get('search', '').capitalize()
        if want:
            all_datas = stocks.objects.filter(Q(name__icontains=want)).order_by('id')
            paginator = Paginator(all_datas, 10)

            page = request.GET.get('page')
            try:
                datas = paginator.page(page)
            except PageNotAnInteger:
                datas = paginator.page(1)
            except EmptyPage:
                datas = paginator.page(paginator.num_pages)
            msg = 'no match user found!..'
            return render(request, 'search.html', {'datas': datas, 'msg': msg})
        else:
            msg = 'no match user found!..'
            return render(request, 'search.html', {'msg': msg})
    else:
        return redirect('home')


def concern(request):
    if request.method == 'POST':
        ask = request.POST['ask']
        messages.objects.create(user=request.user,msg=ask)
        return redirect('home')
    return redirect('home')

