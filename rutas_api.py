from flask import redirect, url_for, request
from datetime import datetime
from run import app,db
from modelos import *
from flask import jsonify

# Listar eventos
@app.route('/')
@app.route('/api/eventos/', methods=['GET'])
def apiListarEventos():
    lista_eventos = db.session.query(Evento).all()
    # Recorrer la lista de personas convirtiendo cada una a JSON
    return jsonify({'eventos': [evento.to_json() for evento in lista_eventos]})


# Ver Evento por Id
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:8000/api/persona/2
@app.route('/api/evento/<id>', methods=['GET'])
def apiGetEventoById(id):
    evento = db.session.query(Evento).get_or_404(id)
    # Convertir la persona creada en JSON
    return jsonify(evento.to_json())
