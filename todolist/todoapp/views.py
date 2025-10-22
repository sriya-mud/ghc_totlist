from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_finance_data

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
        data["top_losers"] =  list(data["top_losers"])
    context = {
        'form': form,
        'tasks': tasks,
        'stock_data': stock_data,
        "range_10": range(10)
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




