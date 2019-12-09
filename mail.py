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
                file.writelines(str(datetime.datetime.now().strftime("%d %b %Y - %H:%M")) + " Error de autenticacion: " + str(e))
                file.writelines('\nRecorda enviar mail de ' + str(subject) + ' a: ' + str(to))
        except smtplib.SMTPServerDisconnected as e:
            print("Servidor desconectado: " + str(e))
            with open('mail_logfile', 'a') as file:
                file.writelines(str(datetime.datetime.now().strftime("%d %b %Y - %H:%M")) + " Servidor desconectado: " + str(e))
                file.writelines('\nRecorda enviar mail de ' + str(subject) + ' a: ' + str(to))
        except smtplib.SMTPSenderRefused as e:
            print("Se requiere autenticacion: " + str(e))
            with open('mail_logfile', 'a') as file:
                file.writelines(str(datetime.datetime.now().strftime("%d %b %Y - %H:%M")) + " Se requiere autenticacion: " + str(e))
                file.writelines('\nRecorda enviar mail de ' + str(subject) + ' a: ' + str(to))
        except smtplib.SMTPException as e:
            print("Unexpected error: " + str(e))
            with open('mail_logfile', 'a') as file:
                file.writelines(str(datetime.datetime.now().strftime("%d %b %Y - %H:%M")) + " Unexpected error: " + str(e))
                file.writelines('\nRecorda enviar mail de ' + str(subject) + ' a: ' + str(to))



