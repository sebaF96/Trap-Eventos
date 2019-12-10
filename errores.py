from flask import render_template, request, jsonify
from run import app
import datetime


def write_log(e):
    with open('logfile', 'a') as file:
        file.write(str(datetime.datetime.now().strftime("%d %b %Y - %H:%M")) + ' - ' + str(e))


# Manejar error de página no encontrada
@app.errorhandler(404)
def page_not_found(e):
    print(e)
    # Si la solicitud acepta json y no HTML
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    # Sino responder con template HTML
    return render_template('errores/404.html'), 404


# Manejar error de página no encontrada
@app.errorhandler(405)
def method_not_allowed(e):
    print(e)
    write_log(e)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'not found'})
        response.status_code = 405
        return response
    # Sino responder con template HTML
    return render_template('errores/404.html'), 405


# Manejar error de error interno
@app.errorhandler(500)
def internal_server_error(e):
    print(e)
    write_log(e)
    # Si la solicitud acepta json y no HTML
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    # Sino responder con template HTML
    return render_template('errores/500.html'), 500


@app.errorhandler(400)
def badrequest(e):
    print(e)
    write_log(e)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'Bad request'})
        response.status_code = 400
        return response
    # Sino responder con template HTML
    return render_template('errores/500.html'), 400


@app.errorhandler(502)
def badgateway(e):
    print(e)
    write_log(e)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'Bad Gateway'})
        response.status_code = 400
        return response
    # Sino responder con template HTML
    return render_template('errores/500.html'), 502


@app.errorhandler(Exception)
def generalException(e):
    print(e)
    write_log(e)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'Unexpected error ' + str(e)})
        return response
    # Sino responder con template HTML
    return render_template('errores/500.html'), 500
