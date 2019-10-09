from run import db
from modelos import Evento, Usuario, Comentario


def mostrar_eventos():
    lista_eventos = db.session.query(Evento).filter(Evento.fecha >= db.func.current_timestamp(),
                                                    Evento.aprobado == 1).all()

    return lista_eventos


def listar_eventos_pendientes():
    return db.session.query(Evento).filter(Evento.aprobado == 0).order_by(Evento.fecha).all()


def get_evento(id):

    evento = db.session.query(Evento).filter(Evento.eventoId == id).one()

    return evento


def get_comentario(id):

    return db.session.query(Comentario).filter(Comentario.comentarioId == id).one()


def listar_miseventos(id):

    lista_eventos = db.session.query(Evento).filter(Evento.usuarioId == id).all()

    return lista_eventos


def listar_comentarios(id):

    return db.session.query(Comentario).filter(Comentario.eventoId == id).order_by(Comentario.fechahora).all()
