from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import usuario
from django.contrib.auth import login
from django.contrib import messages
from datetime import date
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate


def add_usuario(request):
    if request.method == 'POST':
        name = request.POST.get("nome")
        mail = request.POST.get("email")
        pwd = request.POST.get("senha")
        gender = request.POST.get("genero")
        phone = request.POST.get("telefone")
        birth_date = request.POST.get("data_nascimento")

        if usuario.objects.filter(email=mail).exists():
            messages.error(request, "E-mail já cadastrado, insira um e-mail válido.")
            return redirect('registro')
        
       
        users = usuario(
            nome=name, 
            email=mail, 
            genero=gender, 
            telefone=phone,
            data_nascimento=date.fromisoformat(birth_date)
        )
        
        users.set_password(pwd)  #depois preciso explicar o que eu fiz na classe
        users.save()

        messages.success(request, "Usuário registrado com sucesso!")
        return redirect("/") 
    return render(request, 'registro.html')

def realizar_login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        user = authenticate(request, email=email, password=senha)

        if user is not None:
            user.last_login = timezone.now()  # O login simplesmente não funciona sem isso
            user.save(update_fields=['last_login'])
            login(request, user)
            return redirect("/")  
        else:
            messages.error(request, "E-Mail ou Senha inválidos, tente novamente!")
            return redirect('realizar_login')  

    return render(request, 'login.html')

def home(request):
 return render(request, 'home/home.html', {'user': request.user})