from run import mail, app
from flask_mail import Mail, Message
from flask import render_template, flash
from threading import Thread
import smtplib
import datetime


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
            with open('mail_logfile', 'a') as file:
                file.writelines(str(datetime.datetime.now()) + " Error de autenticacion: " + str(e))
                file.writelines('Recorda enviar mail de ' + str(subject) + ' a: ' + str(to))
        except smtplib.SMTPServerDisconnected as e:
            print("Servidor desconectado: " + str(e))
            with open('mail_logfile', 'a') as file:
                file.writelines(str(datetime.datetime.now()) + " Servidor desconectado: " + str(e) + '\n')
                file.writelines('Recorda enviar mail de ' + str(subject) + ' a: ' + str(to))
        except smtplib.SMTPSenderRefused as e:
            print("Se requiere autenticacion: " + str(e))
            with open('mail_logfile', 'a') as file:
                file.writelines(str(datetime.datetime.now()) + " Se requiere autenticacion: " + str(e) + '\n')
                file.writelines('Recorda enviar mail de ' + str(subject) + ' a: ' + str(to))
        except smtplib.SMTPException as e:
            print("Unexpected error: " + str(e))
            with open('mail_logfile', 'a') as file:
                file.writelines(str(datetime.datetime.now()) + " Unexpected error: " + str(e) + '\n')
                file.writelines('Recorda enviar mail de ' + str(subject) + ' a: ' + str(to))



