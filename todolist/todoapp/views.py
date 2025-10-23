from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_finance_data
from itertools import zip_longest
import csv
import os
from django.conf import settings



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
    csv_path = os.path.join(settings.BASE_DIR, 'todoapp', 'static', 'data.csv')

    print("CSV Path:", csv_path)
    csv_exists = os.path.exists(csv_path)

    task_data = {
    "task1": {"labels": [], "values": []},
    "task2": {"labels": [], "values": []},
    "task3": {"points": []}
    }

    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                task = (row.get('task') or '').strip()
                if not task:
                    continue

                if task in ['task1', 'task2']:
                    category = (row.get('category') or '').strip()
                    value_str = (row.get('value') or '').strip()
                    if category and value_str:
                        try:
                            value = float(value_str)
                            task_data[task]["labels"].append(category)
                            task_data[task]["values"].append(value)
                        except ValueError:
                            continue

                elif task == 'task3':
                    x_str = (row.get('x') or '').strip()
                    y_str = (row.get('y') or '').strip()
                    if x_str and y_str:
                        try:
                            x, y = float(x_str), float(y_str)
                            task_data['task3']["points"].append({"x": x, "y": y})
                        except ValueError:
                            continue


    context = {
        'form': form,
        'tasks': tasks,
        'stock_data': stock_data,
        "range_10": range(10),
        'task_data': task_data,
        'csv_path': csv_path,
        'csv_exists': csv_exists
    }

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




