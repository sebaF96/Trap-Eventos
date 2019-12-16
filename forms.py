from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, \
    SubmitField, BooleanField
from wtforms.fields.html5 import EmailField, DateField
from wtforms import validators
from wtforms_components import TimeField, DateRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from datetime import date
import re
from run import db
from modelos import Usuario


class CrearEvento(FlaskForm):

    def nombre_evento(self, field):
        if re.findall("[?/_{$*°}^]", field.data):
            raise validators.ValidationError("Solo los siguientes caracteres especiales estan admitidos (! - # @ . ,)")
        if re.findall("fuck", field.data) or re.findall("nigga", field.data):
            raise validators.ValidationError("El nombre del evento no puede contener malas palabras.")

    def mostrar_datos(self):
        print("Evento: " + str(self.nombreevento.data))
        print("Fecha: " + str(self.fechaevento.data))
        print("Hora: " + str(self.hora.data))
        print("Clasificacion: " + str(self.opciones.data))
        print("Descripcion: " + str(self.descripcion.data))

    def opcional(field):
        field.validators.insert(0, validators.Optional())

    def rangofecha(self, field):
        if field.data < date.today():
            raise validators.ValidationError("Por favor, ingrese una fecha valida")
        # Esta funcion no deja ingresar una fecha en el pasado

    clasificacion = [
        ('Conferencia', 'Conferencia'),
        ('Curso', 'Curso'),
        ('Deporte', 'Deporte'),
        ('Estudio', 'Estudio'),
        ('E-Sport', 'E-Sport'),
        ('Festival', 'Festival'),
        ('Fiesta', 'Fiesta'),
        ('Musical', 'Musical'),
        ('Obra', 'Obra'),
        ('Pasar el rato', 'Pasar el rato'),
        ('Otro', 'Otro')
    ]

    nombreevento = StringField('Nombre del evento',
                               [
                                   validators.DataRequired(message="Completar nombre"),
                                   validators.length(min=5, max=60,
                                                     message='El nombre del evento debe tener entre 5 y 60 caracteres'),
                                   nombre_evento
                               ])

    fechaevento = DateField('Fecha del Evento',
                            [
                                validators.DataRequired(message="Ingrese la fecha de su evento"),
                                rangofecha
                            ])

    hora = TimeField('Hora de inicio',
                     [
                         validators.DataRequired(message="Ingrese la hora de inicio de su evento.")
                     ])

    lugarevento = StringField('Lugar del evento',
                              [
                                  validators.DataRequired(message="Debe especificar el lugar del evento"),
                                  validators.length(min=5, max=60,
                                                    message='El lugar del evento debe tener entre 5 y 60 caracteres')
                              ])

    imagen = FileField(validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'El archivo debe ser una imagen jpg o png')
    ])

    descripcion = TextAreaField('Introduzca una descripcion del evento',
                                [
                                    validators.DataRequired(message="Por favor ingrese una descripcion"),
                                    validators.length(min=40, max=500,
                                                      message='La descripcion del evento debe tener entre 40 y 500 caracteres')
                                ])

    opciones = SelectField('Tipo de evento', [
    ], choices=clasificacion)

    submit = SubmitField("Crear evento!")
    actualizar = SubmitField("Actualizar")


class AgregarComentario(FlaskForm):
    contenido = TextAreaField('Escriba su comentario',
                              [
                                  validators.DataRequired(message="No puede comentar en blanco."),
                                  validators.length(min=4, max=350, message="Su comentario debe tener entre "
                                                                            "4 y 350 caracteres")
                              ])
    submit = SubmitField("Comentar")

    def mostrar_datos(self):
        print("Comentario: " + str(self.contenido.data))


class Registro(FlaskForm):

    def validar_letrasonly(self, field):
        if re.findall("\d", field.data):
            raise validators.ValidationError("Este campo solo puede contener letras")
        if re.findall("[!#$_%&+?:/¿¡*~{}|°]", field.data):
            raise validators.ValidationError("Este campo solo puede contener letras")

    def mostrar_datos(self):
        print("Nombre: " + str(self.nombre.data))
        print("Apellido: " + str(self.apellido.data))
        print("Email: " + str(self.email.data))

    nombre = StringField('Nombre de pila',
                         [
                             validators.DataRequired(message="Completar nombre"),
                             validators.length(max=60,
                                               message='Su nombre debe tener menos de 60 caracteres'),
                             validar_letrasonly

                         ])

    apellido = StringField('Apellido',
                           [
                               validators.DataRequired(message="Completar apellido"),
                               validar_letrasonly,
                               validators.length(max=60,
                                                 message='Su apellido debe tener menos de 60 caracteres')
                           ])

    email = EmailField('Correo Electronico',
                       [
                           validators.DataRequired(message="Completar apellido"),
                           validators.Email(message="Formato incorrecto"),
                           validators.length(max=60,
                                             message='Su email no puede contener mas de 60 caracteres')
                       ])

    contrasenia = PasswordField('Contraseña', [
        validators.DataRequired(message="Ingrese la contraseña"),
        validators.length(min=8, max=35, message="La contraseña debe contener entre 8 y 35 caracteres"),
        validators.EqualTo('repetir', message='Las contraseñas no coinciden')
    ])

    repetir = PasswordField('Repetir contraseña')

    submit1 = SubmitField("Crear cuenta!")


class Login(FlaskForm):

    emailLogin = StringField('Correo electronico', [
                           validators.DataRequired()])

    contraseniaLogin = PasswordField('Contraseña',
                                     [
                                         validators.DataRequired()])

    remember_me = BooleanField('Recordarme')

    submit2 = SubmitField("Entrar")

    def mostrar_datos(self):
        print("Usuario: " + str(self.usuarioLogin.data))
        print("Contraseña: " + str(self.contraseniaLogin.data))


class Filtro(FlaskForm):

    categoria = [
        ('empty', 'Todas'),
        ('Conferencia', 'Conferencia'),
        ('Curso', 'Curso'),
        ('Deporte', 'Deporte'),
        ('Estudio', 'Estudio'),
        ('E-Sport', 'E-Sport'),
        ('Festival', 'Festival'),
        ('Fiesta', 'Fiesta'),
        ('Musical', 'Musical'),
        ('Obra', 'Obra'),
        ('Pasar el rato', 'Pasar el rato'),
        ('Otro', 'Otro')
    ]

    fechainicial = DateField('Desde')

    fechafinal = DateField('Hasta')

    titulo = StringField('Nombre del evento', render_kw={"placeholder": "Titulo completo o palabra clave"})

    categoria = SelectField('Categoria', [], choices=categoria)

    filtrar = SubmitField("Filtrar")


def validarExistente(email):
    aux = False

    if db.session.query(Usuario).filter(Usuario.email.ilike(email)).count() == 0:
        aux = True
    return aux
