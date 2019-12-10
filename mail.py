from run import mail, app
from flask_mail import Mail, Message
from flask import render_template, flash
from threading import Thread
import smtplib
import datetime
from errores import write_logmail


def enviarMail(to, subject, template, **kwargs):
    msg = Message(subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template('mail/' + template + '.txt', **kwargs)
    msg.html = render_template('mail/' + template + '.html', **kwargs)
    thr = Thread(target=mail_sender, args=[app, msg, to, subject])
    # Iniciar hilo
    thr.start()


def mail_sender(app, msg, to, subject):

    with app.app_context():
        try:
            mail.send(msg)
        except smtplib.SMTPAuthenticationError as e:
            print("Error de autenticacion: " + str(e))
            write_logmail(e, "Error de autenticacion: ", subject, to)

        except smtplib.SMTPServerDisconnected as e:
            print("Servidor desconectado: " + str(e))
            write_logmail(e, "Servidor descontctado: ", subject, to)

        except smtplib.SMTPSenderRefused as e:
            print("Se requiere autenticacion: " + str(e))
            write_logmail(e, "Se requiere autenticacion: ", subject, to)

        except smtplib.SMTPException as e:
            print("Unexpected error: " + str(e))
            write_logmail(e, "Unexpected error: ", subject, to)



