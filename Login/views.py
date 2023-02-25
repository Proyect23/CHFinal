from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CreateForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#@PassQ!Sam345
def home(requests):
    return render(requests, 'home.html')

@login_required
def task(requests):
    task = Task.objects.filter(user= requests.user, datecomplete__isnull = True)
    print(task)
    return render(requests, 'task.html',
                  {"tasks": task}
                  )

@login_required
def taskComplete(requests):
    task = Task.objects.filter(user= requests.user, datecomplete__isnull = False).order_by('-datecomplete')
    print(task)
    return render(requests, 'task.html',
                  {"tasks": task}
                  )

def Terminos_condicones(requests):
    return render(requests, "policy&terms.html")


@login_required
def newtask(requests):
    if requests.method == "GET":
        return render(requests, "newtask.html", {
            "form": CreateForm
        })
        
    elif requests.method == "POST":        
        try:
            print(requests.POST)
            form = CreateForm(requests.POST)
            NewForm = form.save(commit=False)
            NewForm.user = requests.user
            NewForm.save()

            return render(requests, "task.html")
        
        except Exception as e:
            return render(requests, "task.html",{
                "error": "Revisa los datos ingresados"
                })


    
@login_required
def Taskdetails(requests, task_id):
    if requests.method == "GET":
        task = get_object_or_404(Task, pk = task_id, user = requests.user)
        form = CreateForm(instance=task)
        return render(requests, "taskdetails.html",
            {
            'task': task,
            'form': form
            }
            )
    else:
        try:
            task = get_object_or_404(Task, pk = task_id, user = requests.user)
            form = CreateForm(requests.POST, instance= task)
            form.save()
            return redirect("task")
        
        except ValueError:
            return render(requests, "taskdetails.html",
                {
                    "task":task,
                    "form": form,
                    "error": "Por favor revise los datos ingresados"
                }
            )    

@login_required
def TaskUpdate(requests, task_id):
    task = get_object_or_404(
        Task, 
        pk = task_id, 
        user = requests.user)        
    if requests.method == "POST":    
        task.datecomplete = timezone.now()
        task.save()
        return redirect("task")

@login_required
def TaskDelete(requests, task_id):
    task = get_object_or_404(
        Task, 
        pk = task_id, 
        user = requests.user)
    if requests.method == "POST":
        task.delete()
        return redirect("task")



#Funciones de Usuarios
def UserLogin(requests):
    
    if requests.method == "GET":
        return render(requests, "singin.html")
        
    elif requests.method == "POST":        
        form_recive = requests.POST
        print(form_recive)
        if "password1" in form_recive:
            
            checkbox = form_recive.get("use_stages")
            if not checkbox:
                return render(requests, "singin.html",{
                        "error": "Por favor Acepte los Terminos y Condicones para continuar"
                    })
                
                
            if form_recive["password1"] == form_recive["password2"]:
                try:
                    print(f"Se ha creado un nuevo user {requests.POST}")
                    user = User.objects.create_user(
                        username = requests.POST["email"], 
                        password= requests.POST["password1"]
                        )
                    user.save()
                    
                    login(requests, user)
                    return redirect("task")

                except:
                    return render(requests, "singin.html",{
                        "error": "El usuario ya existe"
                    })
            else:
                return render(requests, "singin.html",{
                        "error": "Las contraseñas no coinciden"
                    })
            
#password es para los forms de login
        elif "password" in form_recive:
            print(form_recive)
            user = authenticate(
                requests, 
                username = form_recive["email"], 
                password = form_recive["password"]
                )
            if user:
                login(requests, user)
                return redirect("task")
                
            else:
                return render(requests, "singin.html",{
                        "error": "El mail o la constraseña no son correctas"
                    })

@login_required
def CloseSession(requests):
    logout(requests)
    return redirect("home")



def error_404(requests, exception):
    return redirect(requests, "404.html")