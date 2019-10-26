from flask import redirect, url_for, request
from datetime import datetime
from run import app,db
from modelos import *
from flask import jsonify

# Listar eventos
# curl -H "Accept:application/json" http://localhost:5000/api/evento/
@app.route('/')
@app.route('/api/evento/', methods=['GET'])
def apiListarEventos():
    lista_eventos = db.session.query(Evento).all()
    # Recorrer la lista de personas convirtiendo cada una a JSON
    return jsonify({'eventos': [evento.to_json() for evento in lista_eventos]})


# curl -i -X PUT -H "Content-Type:application/json" -H "Accept:application/json" http://localhost:5000/api/evento/136
# -d '{"nombre":"CEEEEEEB", "tipo":"edited"}'
# Actualizar evento
@app.route('/api/evento/<id>', methods=['PUT'])
def apiActualizarEvento(id):
    evento = db.session.query(Evento).get_or_404(id)
    evento.nombre = request.json.get('nombre', evento.nombre)
    evento.fecha = request.json.get('fecha', evento.fecha)
    evento.tipo = request.json.get('tipo', evento.tipo)
    evento.lugar = request.json.get('lugar', evento.lugar)
    evento.descripcion = request.json.get('descripcion', evento.descripcion)
    db.session.add(evento)
    db.session.commit()
    # Convertir la persona actualizada en JSON
    # Pasar código de status
    return jsonify(evento.to_json()), 201

# curl -i -X PUT -H "Content-Type:application/json" -H
# "Accept:application/json" http://localhost:5000/api/evento/136/aprobar
@app.route('/api/evento/<id>/aprobar', methods=['PUT'])
def apiAprobarEvento(id):
    evento = db.session.query(Evento).get_or_404(id)
    evento.aprobado = 1
    db.session.add(evento)
    db.session.commit()

    return jsonify(evento.to_json()), 201


# curl -i -X DELETE -H "Accept: application/json" http://localhost:8000/api/persona/2
@app.route('/api/evento/<id>', methods=['DELETE'])
def eliminarEvento(id):
    evento = db.session.query(Evento).get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    # Pasar código de status
    return '', 204


# Ver Evento por Id
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/evento/136
@app.route('/api/evento/<id>', methods=['GET'])
def apiGetEventoById(id):
    evento = db.session.query(Evento).get_or_404(id)
    # Convertir la persona creada en JSON
    return jsonify(evento.to_json())
