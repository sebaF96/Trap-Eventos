from flask import request
from run import csrf, app, db
from flask import jsonify
from consultas import listar_comentarios, get_comentario, get_evento, listar_eventos_pendientes
from mail import enviarMail
from sqlalchemy.exc import SQLAlchemyError


# Ver Evento por Id
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/evento/136
@app.route('/api/evento/<id>', methods=['GET'])
def apiGetEventoById(id):
    evento = get_evento(id)

    return jsonify(evento.to_json())

# Listar eventos
# curl -H "Accept:application/json" http://localhost:5000/api/evento/
@app.route('/')
@app.route('/api/evento/', methods=['GET'])
def apiListarEventos():
    lista_eventos = listar_eventos_pendientes()

    return jsonify({'eventos': [evento.to_json() for evento in lista_eventos]})


# Actualizar evento
# curl -i -X PUT -H "Content-Type:application/json" -H "Accept:application/json" http://localhost:5000/api/evento/136
# -d '{"nombre":"CEEEEEEB", "tipo":"edited"}'
@app.route('/api/evento/<id>', methods=['PUT'])
@csrf.exempt
def apiActualizarEvento(id):
    evento = get_evento(id)
    evento.nombre = request.json.get('nombre', evento.nombre)
    evento.fecha = request.json.get('fecha', evento.fecha)
    evento.tipo = request.json.get('tipo', evento.tipo)
    evento.lugar = request.json.get('lugar', evento.lugar)
    evento.descripcion = request.json.get('descripcion', evento.descripcion)
    evento.aprobado = 0
    try:
        db.session.add(evento)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()

    return jsonify(evento.to_json()), 201

# Aprobar evento
# curl -i -X PUT -H "Content-Type:application/json" -H
# "Accept:application/json" http://localhost:5000/api/evento/47/aprobar
@app.route('/api/evento/<id>/aprobar', methods=['PUT'])
@csrf.exempt
def apiAprobarEvento(id):

    evento = get_evento(id)
    evento.aprobado = 1
    db.session.add(evento)
    db.session.commit()

    enviarMail(evento.usuario.email, 'Evento aprobado!', 'evento_aprobado', evento=evento)

    return jsonify(evento.to_json()), 201

# Eliminar evento
# curl -i -X DELETE -H "Accept: application/json" http://localhost:5000/api/evento/134
@app.route('/api/evento/<id>', methods=['DELETE'])
@csrf.exempt
def eliminarEvento(id):
    evento = get_evento(id)
    db.session.delete(evento)
    db.session.commit()
    return '', 204


# Ver Comentario por Id
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/comentario/136
@app.route('/api/comentario/<id>', methods=['GET'])
def apiGetComentarioById(id):
    comentario = get_comentario(id)
    return jsonify(comentario.to_json())


# Listar comentarios por evento
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/comentarios/15
@app.route('/api/comentarios/<evento>', methods=['GET'])
def apiGetComentariosByEvento(evento):
    lista_comentarios = listar_comentarios(evento)

    return jsonify({'Comentarios': [comentario.to_json() for comentario in lista_comentarios]})

# Eliminar comentario
# curl -i -X DELETE -H "Accept: application/json" http://localhost:5000/api/comentario/134
@app.route('/api/comentario/<id>', methods=['DELETE'])
@csrf.exempt
def apiEliminarComentarioById(id):
    comentario = get_comentario(id)
    db.session.delete(comentario)
    db.session.commit()
    return '', 204

