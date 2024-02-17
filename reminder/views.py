from django.shortcuts import render,redirect
from django.views.generic import View
from reminder.forms import UserForm,LoginForm,TodoForm,Todos
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

def owner_permission_required(fn):
    def wrappper(request,*args, **kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.user != request.user:
            return redirect("signin")
        else:
            return fn(request,*args, **kwargs)
    return wrappper


decs=[signin_required,owner_permission_required]        



class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=UserForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            print("account craeted")
            return redirect("register")
        else:
            print("failed")
            return render(request,"register.html",{"form":form})

class SigninView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            usr_name=form.cleaned_data.get("username")
            pswd=form.cleaned_data.get("password")
            user_objest=authenticate(request,username=usr_name,password=pswd)
            if user_objest:
                login(request,user_objest)
                print("logged in")
                return redirect("index")
        
        print("invalid")
        return render(request,"login.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class IndexView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        qs=Todos.objects.filter(user=request.user).order_by("status")
        return render(request,"index.html",{"form":form,"data":qs})
    
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        else:
            return render(request,"index.html",{"form":form})
        
@method_decorator(decs,name="dispatch")
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todos.objects.filter(id=id).delete()
        return redirect("index")
    
@method_decorator(decs,name="dispatch")    
class TodoChangeView(View):
    def get(self,request,*args,**kwargs):
       id=kwargs.get("pk")
       todo_object=Todos.objects.get(id=id)
       if todo_object.status==True:
           todo_object.status=False
           todo_object.save()
       else:
           todo_object.status=True
           todo_object.save()
        
       return redirect("index")
    
@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")


        
    
    





