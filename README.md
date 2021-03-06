vmlerta
=======

Pacotes:
--------

	$ cd vmlerta

	$ virtualenv venv
 	$ source venv/bin/activate 
 	
	(venv)➜ vmlerta   venv/bin/pip install --upgrade pip

 	(venv)➜ vmlerta   venv/bin/pip install pygal
    (venv)➜ vmlerta   venv/bin/pip install flask
	(venv)➜ vmlerta   venv/bin/pip install flask-httpauth


    # Para sair do virtualenv

	(venv)$ deactivate 



Forma de uso:
-------------

lista todos os registros, usando (@auth.login_required)

```bash
$ curl -u neviim:password -i http://localhost:5000/monitor/api/v1.0/dados
```

Lista registro id=2

```bash
$ curl -u neviim:password -i http://localhost:5000/monitor/api/v1.0/dados/2
```

Insere um registro

```bash
$ curl -u neviim:password -i -H "Content-Type: application/json" -X POST -d '{ "maquina":"vmremoto", "memoria":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "processo":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "ping":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] }' http://localhost:5000/monitor/api/v1.0/dados

$ curl -u neviim:password -i -H "Content-Type: application/json" -X POST -d '\
									{ "maquina" :"vmremoto", \
									  "memoria" :[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
									  "processo":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
									  "ping"    :[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  \
									}' \
									http://localhost:5000/monitor/api/v1.0/dados
```

Atualiza um registro especifico (id=3)

```bash
$ curl -u neviim:password -i -H "Content-Type: application/json" -X PUT -d '{"done":true, "processo":255}' http://localhost:5000/monitor/api/v1.0/dados/3
$ curl -u neviim:password -i -H "Content-Type: application/json" -X PUT -d '{"done":true, "memoria":3500}' http://localhost:5000/monitor/api/v1.0/dados/3
``` 

Deleta o registro id=3

```bash
$ curl -u neviim:password -i -X DELETE http://localhost:5000/monitor/api/v1.0/dados/3
```

Acesso com LOGIN

```bash
$ curl -u neviim:password -i http://localhost:5000/monitor/api/v1.0/dados
```