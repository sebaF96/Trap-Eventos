from run import db, app, login_manager
from werkzeug.security import generate_password_hash, check_password_hash   # TOKENS
from flask_login import UserMixin, LoginManager
from flask import url_for


class Evento(db.Model):

    eventoId = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(60), nullable=False)

    fecha = db.Column(db.Date, nullable=False)

    hora = db.Column(db.Time, nullable=False)

    descripcion = db.Column(db.String(500), nullable=False)

    imagen = db.Column(db.String(70), nullable=False)

    tipo = db.Column(db.String(15), nullable=False)

    lugar = db.Column(db.String(60), nullable=False)

    usuario = db.relationship("Usuario", back_populates="eventos")

    comentarios = db.relationship("Comentario", back_populates="evento", cascade="all, delete-orphan")

    usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.usuarioId'), nullable=False)

    aprobado = db.Column(db.Boolean, nullable=False, default=False)

    def to_json(self):
        evento_json = {
            'eventoId': url_for('apiGetEventoById', id=self.eventoId, _external=True),
            'nombre': self.nombre,
            'fecha': self.fecha,
            'tipo': self.tipo,
            'lugar': self.lugar,
            'imagen': self.imagen,
            'descripcion': self.descripcion
        }

        return evento_json

    @staticmethod
    def from_json(evento_json):

        nombre = evento_json.get('nombre')
        fecha = evento_json.get('fecha')
        tipo = evento_json.get('tipo')
        lugar = evento_json.get('lugar')
        imagen = evento_json.get('imagen')
        descripcion = evento_json.get('descripcion')

        return Evento(nombre=nombre, tipo=tipo, lugar=lugar, imagen=imagen,
                      descripcion=descripcion, fecha=fecha)


class Usuario(UserMixin, db.Model):

    usuarioId = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(40), nullable=False)

    apellido = db.Column(db.String(30), nullable=False)

    email = db.Column(db.String(60), nullable=False)

    password_hash = db.Column(db.String(128), nullable=False)

    admin = db.Column(db.Boolean, nullable=False, default=False)

    eventos = db.relationship("Evento", back_populates="usuario", cascade="all, delete-orphan")

    comentarios = db.relationship("Comentario", back_populates="usuario", cascade="all, delete-orphan")

    #  No permitir leer la pass de un usuario
    @property
    def password(self):
        raise AttributeError('La password no puede leerse')
    #  Al setear la pass generar un hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_id(self):
        return self.usuarioId
    #  Al verififcar pass comparar hash del valor ingresado con el de la db

    def verificar_pass(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return str(self.nombre) + ' ' + str(self.apellido)

    def is_admin(self):         # Comprueba si el usuario es administrador
        aux = False
        if self.admin == 1:
            aux = True
        return aux

    def is_owner(self, event_or_coment):  # Comprueba si el usuario es dueño, puede usarse con comentarios o eventos.
        aux = False
        if self.usuarioId == event_or_coment.usuarioId:
            aux = True
        return aux


class Comentario(db.Model):

    comentarioId = db.Column(db.Integer, primary_key=True)

    contenido = db.Column(db.String(350), nullable=False)

    fechahora = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    usuario = db.relationship("Usuario", back_populates="comentarios")

    usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.usuarioId'), nullable=False)

    evento = db.relationship("Evento", back_populates="comentarios")

    eventoId = db.Column(db.Integer, db.ForeignKey('evento.eventoId'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

