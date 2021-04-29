from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UsuariosManager(models.Manager):
    def basic_validator(self, postData):
        error={}
        if postData["nombre"].isalpha():
            if len(postData["nombre"])<2:
                error["nombre"]= "el nombre debe tener un largo minimo de 2 caracteres"
        else:
            error["nombre"]= "el nombre debe tener solo letras"
        if len(postData["alias"])<2:
            error["alias"]= "el apellido debe tener un largo minimo de 2 caracteres"
        if len(self.filter(email=postData["email"])) > 0:
            error["email"]="el email ya existe, por favor intenta logearte"
        if not EMAIL_REGEX.match(postData["email"]):
            error["email"]="el mail no tiene un formato valido"
        if len(postData["password"])<1:
            error["password"]= "la contraseña debe tener almenos 4 caracteres"    
        if postData["password"] != postData["confirm"]:
            error["password"]= "las contraseñas deben ser iguales"
        return error

    def login_validator(self, datos):
        error={}
        if len(self.filter(email=datos["correoIngreso"])) == 0:
            error["correoIngreso"]="el email no esta registrado, te invitamos a crear tu usuario"
            return error
        if len(datos["correoIngreso"])==0:
            error["correoIngreso"]="debes ingresar un email"
        
        user=Usuario.objects.get(email=datos['correoIngreso'])
        contrasenaARevisar=datos['contrasena']
        contrasena=user.password
        if bcrypt.checkpw(contrasenaARevisar.encode(), contrasena.encode()) == False:
            error["contrasena"]= "malo tu password"
        return error

    def books_validator(self, datos):
        error={}
        if len(datos["titulo"])<1:
            error["titulo"]="es requisito incorporar un titulo"
        if len(Book.objects.filter(titulo=datos["titulo"])) > 0:
            error["titulo"]="el libro ya existe,no wei"
        if len(datos["resena"])<5:
            error["resena"]= "por favor ingresar mas de 5 caracteres"
        return error
    
    def review_validatron(self, datos):
        error={}
        #if len(datos["resena"])<10:
        #    error["resena"]="la reseña debe tener 10 caracteres como minimo"
        return error


class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=UsuariosManager()

    #comentario
    #libroAgregado

class Autor(models.Model):
    nombreAutor = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    #libroEscrito

class Libros(models.Model):
    titulo = models.CharField(max_length=100)
    agragadoPor = models.ForeignKey(Usuario, related_name="libroAgregado", on_delete=models.CASCADE,  blank=True, null=True, default=None)
    escritoPor = models.ForeignKey(Autor, related_name="libroEscrito", on_delete=models.CASCADE,  blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    #comentario

class Resena(models.Model):
    resena = models.TextField()
    rating = models.FloatField()
    comentadoPor = models.ForeignKey(Usuario, related_name="comentarista", on_delete=models.CASCADE,  blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    comentario = models.ForeignKey(Libros, related_name="comentario", on_delete=models.CASCADE,  blank=True, null=True, default=None)
    
# Create your models here.
