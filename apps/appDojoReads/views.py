from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


def inicio(request):
    return render(request, "index.html")

def registro(request):
   
    if request.method == "GET":
        return redirect("/")
    elif request.method =="POST": 
        error = Usuario.objects.basic_validator(request.POST)
      
        if len(error) > 3 or error["nombre"] != None or error["alias"] != None or error["password"] != None:
           
            for key, value in error.items():
                messages.error(request, value, key)
            user= Usuario(
                nombre = request.POST["nombre"],
                alias =  request.POST["alias"],
                email =  request.POST["email"],
            )
            context = {
                "user": user
            }
           
            return render(request, 'index.html', context)
        else:
            
            contrasena= bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
            user = Usuario.objects.create(
                nombre = request.POST["nombre"],
                alias =  request.POST["alias"],
                email =  request.POST["email"],
                password =  contrasena
            )
            request.session['alias']=request.POST["alias"]
            request.session['id']=user.id
            context={
                "user":user
            }   
        return redirect("/books")

def login(request):
    if request.method == "GET":
        return redirect("/")
     
    elif request.method =="POST":        
        error = Usuario.objects.login_validator(request.POST)
        if len(error) > 0:
            for key, value in error.items():
                messages.error(request, value, key)
               
            return redirect('/')
        else:
           
            user=Usuario.objects.get(email=request.POST['correoIngreso'])
            contrasenaARevisar=request.POST['contrasena']
            contrasena=user.password
            if bcrypt.checkpw(contrasenaARevisar.encode(), contrasena.encode()):
                request.session['alias'] = user.alias
                request.session['id']=user.id
                return redirect ('/books')
            
            return redirect("/")

def books(request):
    if "id" in request.session:
        context ={
            "libros":Libros.objects.all(),
            "usuarios":Usuario.objects.all(),
            "resenas": Resena.objects.all().order_by("-updated_at"),
        }       
        return render(request,'books.html', context)
    return redirect("/")
def add(request):

    if request.method=="GET":
        context={
            "autores":Autor.objects.all()
        }
        return render(request, "add.html", context)
    elif request.method =="POST":
        
        #error = Usuario.objects.books_validator(request.POST)
#
        #if len(error) > 0:
        #    for key, value in error.items():
        #        messages.error(request, value, key)
        #    return render(request, "books.html")
#
        #else:
        user = Usuario.objects.get(id=request.session["id"])
        print(request.POST["nuevoAutor"])
        print(request.POST["rating"])
        esteAutor = Autor.objects.create(
            nombreAutor = request.POST["nuevoAutor"]
        )
        esteLibro=Libros.objects.create(
            titulo = request.POST["titulo"],
            agragadoPor = user,
            escritoPor = esteAutor,
        )
        estaResena = Resena.objects.create(
            resena = request.POST["resena"],
            rating = request.POST["rating"],
            comentario = esteLibro, 
            comentadoPor = user
        )
        
        request.session["titulo"]=esteLibro.titulo
        request.session["libroId"]=esteLibro.id
        return redirect(f"/detalle/{esteLibro.id}")

def detalle(request, libroId):
    error = Usuario.objects.review_validatron(request.POST)
    esteLibro=Libros.objects.get(id=libroId)
    context={
        "esteLibro": esteLibro,
        "resenas": Resena.objects.filter(comentario__id=libroId)
       
    }
    if len(error) > 0:
        for key, value in error.items():
            messages.error(request, value, key)
        return render(request, 'detalle.html')
    else:
       
        
        return render(request, "detalle.html", context)
def addReview(request, libroId):
    esteLibro=Libros.objects.get(id=libroId)
    Resena.objects.create(
        resena = request.POST["resena"],
        rating = request.POST["rating"],
        comentario = esteLibro, 
        comentadoPor = Usuario.objects.get(id=request.session["id"])
        )
    return redirect("/books")


def usuario(request, id):
    esteUsuario = Usuario.objects.get(id=id)
    resenasDeUsuario = Resena.objects.filter(comentadoPor=esteUsuario)
    context ={
        "esteUsuario": esteUsuario,
        "resenasTotales":esteUsuario.comentarista.count(),
        "resenasDeUsuario":Resena.objects.filter(comentadoPor=esteUsuario)
    }
    print(resenasDeUsuario)

    return render(request, "usuario.html", context)

def delete(request):
    if "id" in request.session:

               
        return render(request, "detalle.html")
    return redirect("/")
def salir(request):
    if "alias" in request.session:
        del request.session["alias"]
    if 'id' in request.session:
        del request.session['id']
    return redirect("/")













    


# Create your views here.
