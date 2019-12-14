from flask import render_template
from flask import flash
from flask import redirect, url_for, abort
from werkzeug.utils import secure_filename
import os.path
import os
from random import randint
from forms import *
from run import app
from consultas import *
from sqlalchemy.exc import SQLAlchemyError
from run import db, login_manager
from mail import enviarMail
from flask_login import login_required, login_user, logout_user, current_user, LoginManager


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Debe iniciar sesión para continuar.', 'warning')
    return redirect(url_for('ingresar'))


def has_permission(user, evento):
    aux = False
    if user.is_authenticated:
        if user.is_admin() or user.is_owner(evento):
            aux = True
    return aux


@app.route('/',  methods=["POST", "GET"])
@app.route('/<int:pag>', methods=["POST", "GET"])
def index(pag=1):

    filtro = Filtro()
    titulo = "Trap Eventos - Home"
    pag_tam = 9
    paginar = True
    eventos = db.session.query(Evento).filter(Evento.fecha >= db.func.current_timestamp(),
                                              Evento.aprobado == 1).order_by(Evento.fecha).paginate(pag, pag_tam,
                                                                                                    error_out=False)
    if filtro.is_submitted():
        lista_eventos = db.session.query(Evento)

        if filtro.fechainicial.data is not None:
            lista_eventos = lista_eventos.filter(Evento.fecha >= filtro.fechainicial.data)
        if filtro.fechafinal.data is not None:
            lista_eventos = lista_eventos.filter(Evento.fecha <= filtro.fechafinal.data)
        if filtro.categoria.data != 'empty':
            lista_eventos = lista_eventos.filter(Evento.tipo == filtro.categoria.data)
        if filtro.titulo.data != "":
            lista_eventos = lista_eventos.filter(Evento.nombre.ilike('%'+filtro.titulo.data+'%'))

        eventos = lista_eventos.filter(Evento.aprobado == 1).order_by(Evento.fecha)
        paginar = False

    return render_template('main.html', eventos=eventos, titulo=titulo, filtro=filtro, paginar=paginar)


@app.route('/mis-eventos')
@login_required
def miseventos():
    from consultas import listar_miseventos
    titulo = "Mis Eventos"
    lista_eventos = listar_miseventos(current_user.usuarioId)

    return render_template('mis_eventos.html', titulo=titulo, lista_eventos=lista_eventos)


@app.route('/ver-evento/<id>', methods=["POST", "GET"])
def vistaevento(id):
    evento = get_evento(id)

    if evento.aprobado == 1 or has_permission(current_user, evento):
        formulario = AgregarComentario()
        titulo = "Evento - " + evento.nombre
        lista_comentarios = listar_comentarios(id)

        if formulario.is_submitted():
            if formulario.validate_on_submit():
                flash('Comentario añadido!', 'success')
                formulario.mostrar_datos()

                comentario = Comentario(contenido=formulario.contenido.data, usuarioId=current_user.usuarioId,
                                        eventoId=id)
                try:
                    db.session.add(comentario)
                    db.session.commit()
                except SQLAlchemyError as e:
                    db.rollback()
                    enviarMail(os.getenv('ADMIN_MAIL'), 'SQLAlchemy error', 'error', e=e)

                return redirect(url_for('vistaevento', id=id))
            else:
                flash('Comentario no añadido. Reintente', 'danger')

        return render_template('ver_evento.html', id=id, evento=evento, titulo=titulo,
                               formulario=formulario, lista_comentarios=lista_comentarios)
    else:
        return redirect(url_for('index'))


@app.route('/crear-evento', methods=["POST", "GET"])
@login_required
def crearevento():
    formulario = CrearEvento()
    titulo = "Nuevo Evento"
    if formulario.validate_on_submit():
        f = formulario.imagen.data
        filename = secure_filename(formulario.nombreevento.data + str(randint(1, 100)))
        f.save(os.path.join('static/images/', filename))
        flash('Evento creado con exito! (Debera ser aprobado por un administrador antes de '
              'ser mostrado en la pagina)', 'success')
        formulario.mostrar_datos()
        print("Imagen: " + str(filename))

        evento = Evento(nombre=formulario.nombreevento.data, fecha=formulario.fechaevento.data,
                        hora=formulario.hora.data,
                        lugar=formulario.lugarevento.data, tipo=formulario.opciones.data, imagen=filename,
                        descripcion=formulario.descripcion.data, usuarioId=current_user.usuarioId)
        try:
            db.session.add(evento)
            db.session.commit()
        except SQLAlchemyError as e:
            db.rollback()
            enviarMail(os.getenv('ADMIN_MAIL'), 'SQLAlchemy error', 'error', e=e)

        return redirect(url_for('miseventos'))

    return render_template('crear_evento.html', titulo=titulo, formulario=formulario, destino="crearevento")


@app.route('/editar-evento/<int:id>', methods=["POST", "GET"])
@login_required
def actualizar(id):
    titulo = "Editar evento"
    evento = get_evento(id)
    if has_permission(current_user, evento):

        class Evento:
            nombreevento = evento.nombre
            fechaevento = evento.fecha
            hora = evento.hora
            lugarevento = evento.lugar
            imagen = evento.imagen
            descripcion = evento.descripcion
            opciones = evento.tipo

        formulario = CrearEvento(obj=Evento)

        CrearEvento.opcional(formulario.imagen)

        if formulario.validate_on_submit():
            flash('Evento actualizado con exito! (La actualizacion debera ser aprobada por un administrador antes'
                  ' de ser mostrada en la pagina)', 'success')
            formulario.mostrar_datos()

            evento.nombre = formulario.nombreevento.data
            evento.fecha = formulario.fechaevento.data
            evento.hora = formulario.hora.data
            evento.lugar = formulario.lugarevento.data
            evento.descripcion = formulario.descripcion.data
            evento.tipo = formulario.opciones.data
            evento.aprobado = 0

            db.session.commit()

            return redirect(url_for('miseventos'))

        return render_template('crear_evento.html', titulo=titulo, formulario=formulario, destino="actualizar", id=id,
                               evento=evento)
    else:
        return redirect(url_for('index'))


@app.route('/aprobar-eventos')
@login_required
def aprobareventos():
    lista_eventos = listar_eventos_pendientes()
    titulo = "Eventos pendientes"

    if current_user.is_admin():
        return render_template('aprobar_eventos.html', titulo=titulo, lista_eventos=lista_eventos)

    else:
        return redirect(url_for('index'))


@app.route('/aprobarById/<int:id>')
@login_required
def aprobarEventoById(id):

    if current_user.is_admin():

        evento = get_evento(id)
        evento.aprobado = 1
        db.session.commit()

        enviarMail(evento.usuario.email, 'Evento aprobado!', 'evento_aprobado', evento=evento)

        return redirect(url_for('aprobareventos'))
    else:
        flash('Usted no tiene permiso para realizar esta accion', 'warning')
        return redirect(url_for('index'))


@app.route('/eliminarById/<int:id>')
@login_required
def eliminarEventoById(id):
    evento = get_evento(id)
    if current_user.is_admin() or current_user.is_owner(evento):
        try:
            db.session.delete(evento)
            db.session.commit()
        except SQLAlchemyError as e:
            db.rollback()
            enviarMail(os.getenv('ADMIN_MAIL'), 'SQLAlchemy error', 'error', e=e)
        return redirect(url_for('aprobareventos'))
    else:
        flash('Usted no tiene permiso para realizar esta accion', 'warning')
        return redirect(url_for('index'))


@app.route('/eliminarComentarioById/<int:id>')
@login_required
def eliminarComentarioById(id):

    comentario = get_comentario(id)
    if current_user.is_admin() or current_user.is_owner(comentario) or current_user.is_owner(comentario.evento):
        try:
            db.session.delete(comentario)
            db.session.commit()
        except SQLAlchemyError as e:
            db.rollback()
            enviarMail(os.getenv('ADMIN_MAIL'), 'SQLAlchemy error', 'error', e=e)

        flash('Comentario eliminado!', 'success')
        return redirect(url_for('vistaevento', id=comentario.eventoId))
    else:
        flash('Usted no tiene permiso para realizar esta accion', 'warning')
        return redirect(url_for('index'))


@app.route('/ingresar', methods=["POST", "GET"])
def ingresar():
    titulo = "Ingresar"
    formulario = Registro()
    login = Login()
    if formulario.submit1.data is True and formulario.validate_on_submit():

        if validarExistente(formulario.email.data):
            flash('Cuenta creada con exito!', 'success')
            flash('Pronto recibiras un email de bienvenida!', 'success')
            formulario.mostrar_datos()

            usuario = Usuario(formulario.nombre.data, formulario.apellido.data, formulario.email.data,
                              formulario.contrasenia.data)
            try:
                db.session.add(usuario)
                db.session.commit()
                enviarMail(formulario.email.data, 'Bienvenido a Trap Eventos!', 'cuenta_creada', formulario=formulario)
                login_user(usuario, False)
            except SQLAlchemyError as e:
                db.rollback()
                enviarMail(os.getenv('ADMIN_MAIL'), 'SQLAlchemy error', 'error', e=e)

            return redirect(url_for('index'))
        else:
            flash('Existe una cuenta registrada con el email ingresado. Intenta recuperar tu contraseña', 'danger')

    if login.submit2.data is True and login.validate_on_submit():

        usuario = db.session.query(Usuario).filter(Usuario.email == login.emailLogin.data).first()
        # Si el usuario existe y se verifica la pass
        if usuario is not None and usuario.verificar_pass(login.contraseniaLogin.data):
            # Loguear usuario
            login_user(usuario, login.remember_me.data)
            return redirect(url_for('index'))
        else:
            # Mostrar error de autenticación
            flash('Fallo autenticacion, reintente.', 'danger')

    if not current_user.is_authenticated:
        return render_template('registro.html', titulo=titulo, formulario=formulario, login=login)
    else:
        return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('ingresar'))
