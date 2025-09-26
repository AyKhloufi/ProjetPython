from django.views.generic.base import View
from django.shortcuts import render

class HomeView(View):
    def get(self, request):
        return render(request, 'App/home.html')
    
class AboutView(View):
    def get(self, request):
        return render(request, 'App/about.html')