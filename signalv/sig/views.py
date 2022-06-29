from django.shortcuts import render, reverse


def home(request):
    return render(request, 'sig/home.html')
