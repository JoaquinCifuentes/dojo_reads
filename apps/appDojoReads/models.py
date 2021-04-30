from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UsuariosManager(models.Manager):
    def basic_validator(self, postData):
        error={}
        error["nombre"] = self.validar_longitud("nombre", postData["nombre"], 2)
        error["alias"] = self.validar_longitud("alias", postData["alias"], 5)
        error["password"] = self.validar_longitud("password", postData["password"], 2)
        
        if len(self.filter(email=postData["email"])) > 0:
            error["email"]="el email ya existe, por favor intenta logearte"
        if not EMAIL_REGEX.match(postData["email"]):
            error["email"]="el mail no tiene un formato valido"
        if postData["password"] != postData["confirm"]:
            error["confirm"]= "las contraseñas deben ser iguales"
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
        error["titulo"] = self.validar_longitud("titulo", datos["titulo"], 2)
        error["resena"] = self.validar_longitud("resena", datos["resena"], 10)
        
        if len(Book.objects.filter(titulo=datos["titulo"])) > 0:
            error["titulo"]="el libro ya existe en nuestra base de datos,siga participando"
        return error
    
    def review_validatron(self, datos):
        error={}
        #if len(datos["resena"])<10:
        #    error["resena"]="la reseña debe tener 10 caracteres como minimo"
        return error

    def validar_longitud(self, campo, cadena, largoMinimo):
        error ={}
        if len(cadena)< largoMinimo:
            return (f"{campo} no puede ser menor que {largoMinimo} caracteres.")
        

    


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
