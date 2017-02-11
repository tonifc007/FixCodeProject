# -*- coding: utf 8 -*-
from __future__ import absolute_import
from celery import shared_task
from django.core.mail import send_mail, EmailMessage

@shared_task
def email_acao_seguir(stremissor, emailreceptor, nomereceptor):
	try:
		send_mail(
		    'Você ganhou um novo seguidor',
		    'Olá: '+nomereceptor+', você ganhou um novo seguidor: '+stremissor+'',
		    'fixcodeproject@gmail.com',
		    [emailreceptor],
		    fail_silently=False,
		)
	except Exception as e:
		print("Erro ao enviar email")
	return "Email eviado"

@shared_task
def email_boas_vindas(nomeuser, emailuser):
	try:
		msg = EmailMessage(
		    'Bem-vindo(a) ao FixCode',
		    '<h2>Olá, '+nomeuser+'<h2>'
		    +'<h3>Seja bem vindo a plataforma FixCode. :)</h3>'
		    +'<p>Esta plataforma foi desenvolvida pensada nos desenvolvedores de softwares. O intuito inicial é a interação entre os vários desenvolvedores e programadores que existem mundo a fora e para isso a comunidade leva consigo a ideia do auxilio aos programadores.</p>'
		    +'<ul><li><a href="#">Acesse agora</a></li><li><a href="#">Conheça a plataforma</a></li></ul>',
		    'fixcodeproject@gmail.com',
		    [emailuser]
		)
		msg.content_subtype = "html"
		msg.send()
	except Exception as e:
		print("Erro ao enviar email")
	return "Email de boas-vindas enviado"

@shared_task
def email_alteracao(first,last,nomeuser,emailuser):
	try:
		msg = EmailMessage(
		    'Conta com alteração',
		    '<h2>Olá, '+first+'<h2>'
		    +'<h3>Sua conta foi alterada:</h3>'
		    +'<p><i>(Sua nova senha não será exibida por questões de segurança)</i></p>'
		    +'<ul><li>Primeiro nome: <b>'+first+'<b>;</li>'
		    +'<li>Ultimo nome: <b>'+last+'<b>;</li>'
		    +'<li>Username: <b>'+nomeuser+'<b>;</li>'
		    +'<li>Email: <b>'+emailuser+'<b>.</li></ul>'
		    +"<br><br><p>Para alterar parâmetros da sua conta vá em <a href='#'>FixCode</a>:"
		    +'<br><i>Editar perfil > Configurações avançadas</i></p>',
		    'fixcodeproject@gmail.com',
		    [emailuser]
		)
		msg.content_subtype = "html"
		msg.send()
	except Exception as e:
		print(e)
		print("Erro ao enviar email")
	return "Email de altração enviado"
