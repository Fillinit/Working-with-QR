from django.shortcuts import render, redirect, get_object_or_404
from PyPDF2 import PdfReader
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    template = "mainapp/index.html"
    return render(request, template)


def orders(request):
    template = "mainapp/orders.html"
    return render(request, template)


def packaging(request):
    template = "mainapp/packaging.html"
    return render(request, template)


def operations(request):
    template = "mainapp/operations.html"
    return render(request, template)


def marking_codes(request):
    template = "mainapp/marking_codes.html"
    return render(request, template)
