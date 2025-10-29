from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_finance_data
from itertools import zip_longest
import os
from django.conf import settings
import pandas as pd

def stock_data_analysis_1():
    csv_path = os.path.join(settings.BASE_DIR, 'todoapp', 'static', 'C:/Users/sriya.m/Downloads/combined_nifty.csv')
    print("CSV Path (Analysis 1):", csv_path)

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(df.head(40))

        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
        ma_column = '7-Day MA' if '7-Day MA' in df.columns else 'MA7'
        if ma_column not in df.columns:
            df[ma_column] = None
        
        df = df.dropna(subset=['Date', 'Close',ma_column])

        return {
            "labels": df['Date'].dt.strftime('%Y-%m-%d').tolist(),
            "close_values": df['Close'].tolist(),
            "ma_values": df[ma_column].tolist()
        }

    return {"labels": [], "close_values": [], "ma_values": []}


def stock_data_analysis_2():
    csv_path = os.path.join(settings.BASE_DIR, 'todoapp', 'static', 'C:/Users/sriya.m/Downloads/MSFT_processed.csv')
    print("CSV Path (Analysis 2):", csv_path)

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(df.head(40))
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
        df = df.dropna(subset=['Date', 'Diff'])
        return {
            "labels": df['Date'].dt.strftime('%Y-%m-%d').tolist(),
            "values": df['Diff'].tolist()
        }

    return {"labels": [], "values": []}


def stock_data_analysis_3():
    #  Use direct CSV path (no os.path.join with drive letter)
    csv_path = r'C:/Users/sriya.m/Downloads/graph_used_columns.csv'
    print("CSV Path (Analysis 3):", csv_path)

    if not os.path.exists(csv_path):
        print("File not found:", csv_path)
        return {"labels": [], "close_vs_return": {"labels": [], "close": [], "close_return": []}}

    df = pd.read_csv(csv_path)
    print(df.head(30))

    # Clean column names
    df.columns = df.columns.str.strip()

    #  Convert date column
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Date'])

    # Handle Close and Close_Return(%) columns safely
    if 'Close' not in df.columns or 'Close_Return(%)' not in df.columns:
        print("Required columns missing in CSV")
        return {"labels": [], "close_vs_return": {"labels": [], "close": [], "close_return": []}}

    close_vs_return = {
        "labels": df['Date'].dt.strftime('%Y-%m-%d').tolist(),
        "close": df['Close'].fillna(0).round(2).tolist(),
        "close_return": df['Close_Return(%)'].fillna(0).round(2).tolist()
    }

    return {
        "labels": close_vs_return["labels"],
        "close_vs_return": close_vs_return
    }



def index(request):
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    stock_data =  get_finance_data()

    for data in stock_data.values():
        data["top_gainers"] = list(data["top_gainers"])
        data["top_losers"] =  sorted(data["top_losers"], key=lambda x: x[1])
        data["gainers_losers"] = list(zip_longest(data["top_gainers"], data["top_losers"]))
    

    # Read CSV for Data Analysis Tab
   

    #print("CSV Path:", csv_path)
    #csv_exists = os.path.exists(csv_path)

    #task_data = {
    #"task1": {"labels": [], "values": []},
    #"task2": {"labels": [], "values": []},
    #"task3": {"points": []}
    #}

    #if os.path.exists(csv_path):
        #task_stock_data = pd.read_csv(csv_path)
        # print("CSV Data Loaded Successfully")
    
    #Function 1,2,3 calls
    analysis1_data = stock_data_analysis_1()
    analysis2_data = stock_data_analysis_2()
    analysis3_data = stock_data_analysis_3()

    context = {
        'form': form,
        'tasks': tasks,
        'stock_data': stock_data,
        "range_10": range(10),
        #"task_data": task_stock_data,
        #"csv_exists": csv_exists,
        "analysis1_data": analysis1_data,
        "analysis2_data": analysis2_data,
        "analysis3_data": analysis3_data,
    }
    # print("Context Data:", context)

    return render(request, 'todoapp/index.html',context)


def update_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todoapp/update.html', {'form': form, 'task': task})


def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('index')
    return render(request, 'todoapp/delete.html', {'task': task})

class FinanceAPIView(APIView):
    def get(self, request):
        data = get_finance_data()
        return Response([data])




