#!flask/bin/python
# -*- coding: utf-8 -*-

# - por:
#	Neviim Jads - (neviimdev@gmail.com) 

# - Demostratico de como criar uma API com flask, codigo criado com base educacional.


import pygal
from pygal.style import *

from flask import Flask, jsonify
from flask import render_template
from flask import make_response
from flask import url_for
from flask import request
from flask import abort

from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app  = Flask(__name__, static_url_path = "", static_folder = "static")

# Uma lista de dicionarios json
dados = [
	{
		'id':1,
		'maquina'  :'nvmdev',
		'memoria'  :[1395, 8212, 5720, 7218, 2464, 1660, 2123, 6607, 2651, 6361, 1044, 3797],
		'processo' :[7473, 5099, 1700, 2651, 6361, 6044, 3797, 9450, 5933, 4203, 3229, 7810],
		'ping'     :[ 403,  701,  859, 1079,  544,  736,   34,  102, 2933, 4203, 5229, 5910],
		'done'     :False
	}
]

# Função para melhorar a interface de serviço web:
#
# 	Tudo o que estamos fazendo aqui é tomar uma tarefa do nosso banco de dados e 
# 	criar uma nova tarefa que tem todos os campos, exceto ID, que é substituído 
# 	por um outro campo chamado uri, gerado com url_for do Flask.
#
#		$ curl -u neviim:password -i http://localhost:5000/monitor/api/v1.0/dados
#
def make_public_dado(dado):
	new_dado = {}
	for field in dado:
		if field == 'id':
			new_dado['uri'] = url_for('get_dado', dado_id=dado['id'], _external=True)
		else:
			new_dado[field] = dado[field]
	return new_dado


''' Autenticação
'''
# Login
@auth.get_password
def get_password(username):
	if username == 'neviim':
		return 'password'
	return None


''' Todos defaut
'''
# GET todos, Monitor
@app.route('/monitor/api/v1.0/dados', methods=['GET'])
@auth.login_required
def get_dados():
	return jsonify({'dados': [make_public_dado(dado) for dado in dados]})

# GET por id, Monitor (abort)
@app.route('/monitor/api/v1.0/dados/<int:dado_id>', methods=['GET'])
@auth.login_required
def get_dado(dado_id):
	dado = [dado for dado in dados if dado['id'] == dado_id]
	if len(dado) == 0:
		abort(404)
	return jsonify({'dado': dado[0]})

# POST, Monitor (request)
@app.route('/monitor/api/v1.0/dados', methods=['POST'])
@auth.login_required
def create_dado():
	if not request.json or not 'maquina' in request.json:
		abort(400)
	dado = {
		'id': dados[-1]['id'] + 1,
		'maquina' : request.json['maquina'],
		'memoria' : request.json.get('memoria', 0),
		'processo': request.json.get('processo', 0),
		'ping'    : request.json.get('ping', 0),
		'done'    : False
	}
	dados.append(dado)
	return jsonify({'dado': dado}), 201

# PUT, Monitor (request)
# curl -u neviim:password -i http://localhost:5000/monitor/api/v1.0/dados
# curl -u neviim:password -i -H "Content-Type: application/json" -X PUT -d '{"hora":6,"ping":200}' http://localhost:5000/monitor/api/v1.0/dados/1
#
@app.route('/monitor/api/v1.0/dados/<int:dado_id>', methods=['PUT'])
#@auth.login_required
def update_dado(dado_id):
	dado = filter(lambda t: t['id'] == dado_id, dados)
	if len(dado) == 0:
		abort(404)    
	if not request.json:
		abort(400)  
	if 'hora'     in request.json and type(request.json['hora'])     != int  or 'hora' not in request.json:
		abort(400) 
	if 'ping'     in request.json and type(request.json['ping'])     != int:
		abort(400)
	if 'memoria'  in request.json and type(request.json['memoria'])  != int:
		abort(400)
	if 'processo' in request.json and type(request.json['processo']) != int:
		abort(400)
	if 'done'     in request.json and type(request.json['done']) is not bool:
		abort(400)  

	# registro da hora do envio
	hr = request.json.get('hora')

	# condicoes para inserir
	if 'memoria'  in request.json: 
		dado[0]['memoria'][hr]  = request.json.get('memoria' , dado[0]['memoria' ])
	if 'processo' in request.json:
		dado[0]['processo'][hr] = request.json.get('processo', dado[0]['processo'])
	if 'ping'     in request.json:
		dado[0]['ping'][hr]     = request.json.get('ping'    , dado[0]['ping'])
	if 'done'     in request.json:
		dado[0]['done']         = request.json.get('done'    , dado[0]['done'])
	#
	return jsonify({'dado': make_public_dado(dado[0])})

# DELETE, monitor
@app.route('/monitor/api/v1.0/dados/<int:dado_id>', methods=['DELETE'])
@auth.login_required
def delete_dado(dado):
	dado = [dado for dado in dados if dado['id'] == dado]
	if len(dado) == 0:
		abort(404)
	dados.remove(dado[0])
	return jsonify({'result': True})


''' Tratando erros
'''
# ERRO 400 - Request mal sucedido
@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify( { 'error': 'Os dados do request nao estao corretor, verifiqueos.' } ), 400)

# ERRO 403 - Retornar 403 em vez de 401
@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Acesso nao autorizado'}), 403)
	# para impedir que navegadores de exibir a caixa de diálogo de autenticação padrão

# ERRO 404 - (make_response)
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Nao encontrado!'}), 404)


''' Monta grafico com os dados teste
'''
@app.route('/monitor/teste')
def index_teste():
	radar_chart = pygal.Radar()
	radar_chart.fill = True
	radar_chart.style = NeonStyle
	radar_chart.title = 'Maquina: teste'
	radar_chart.x_labels = ['12', '11', '10', '09', '08', '07', '06', '05', '04', '03', '02', '01']

	radar_chart.add('memoria' , [1395, 8212, 5720, 7218, 2464, 1660, 2123, 6607, 2651, 6361, 1044, 3797])
	radar_chart.add('processo', [7473, 5099, 1700, 2651, 6361, 6044, 3797, 9450, 5933, 4203, 3229, 7810])
	radar_chart.add('rede'    , [3472, 2933, 4203, 5229, 3810, 4828, 9013, 4669, 3797, 9450, 2933, 4103])
	radar_chart.add('ping'    , [ 403,  701,  859, 1079,  544,  736,   34,  102, 2933, 4203, 5229, 5910])
	chart = radar_chart.render(is_unicode=True)
	return render_template('teste.html', chart=chart )

# GET por id, monta grafico (abort)
@app.route('/monitor/api/v1.0/graph/<int:dado_id>', methods=['GET'])
def get_mostra_graph(dado_id):
	dado = [dado for dado in dados if dado['id'] == dado_id]
	if len(dado) == 0:
		abort(404)

	# pygal grafico
	radar_chart = pygal.Radar()
	radar_chart.fill = True
	radar_chart.style = NeonStyle
	radar_chart.title = 'Maquina: ' +dado[0]['maquina']
	radar_chart.x_labels = ['12', '11', '10', '09', '08', '07', '06', '05', '04', '03', '02', '01']

	radar_chart.add('memoria' , dado[0]['memoria'])
	radar_chart.add('processo', dado[0]['processo'])
	radar_chart.add('ping'	  , dado[0]['ping'])
	chart = radar_chart.render(is_unicode=True)
	#
	return render_template('index.html', chart=chart )


''' Chamada principal
'''
# --- Inicio
if __name__ == '__main__':
	app.run( debug=True,
			 host="0.0.0.0",
			 port=int("5000")
	)


