from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# Configuração da URL base da API
API_BASE_URL = "http://backend:8000"

@app.route('/')
def index():
    response = requests.get(f"{API_BASE_URL}/api/v1/tarefas/")
    try:
        tarefas = response.json()
    except:
        tarefas = []
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_tarefa():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        prazo = request.form['prazo']
        diario = request.form.get('diario') == 'on'
        payload = {
            'titulo': titulo,
            'descricao': descricao,
            'concluida': False,
            'prazo': prazo,
            'diario': diario
        }
        response = requests.post(f"{API_BASE_URL}/api/v1/tarefas/", json=payload)
        if response.status_code == 201:
            return redirect(url_for('index'))
        return "Erro ao adicionar tarefa", 500
    return render_template('adicionar.html')

@app.route('/atualizar/<int:tarefa_id>', methods=['GET', 'POST'])
def atualizar_tarefa(tarefa_id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        concluida = request.form.get('concluida') == 'on'
        prazo = request.form['prazo']
        diario = request.form.get('diario') == 'on'
        payload = {
            'titulo': titulo,
            'descricao': descricao,
            'concluida': concluida,
            'prazo': prazo,
            'diario': diario
        }
        response = requests.patch(f"{API_BASE_URL}/api/v1/tarefas/{tarefa_id}", json=payload)
        if response.status_code == 200:
            return redirect(url_for('index'))
        return "Erro ao atualizar tarefa", 500
    response = requests.get(f"{API_BASE_URL}/api/v1/tarefas/{tarefa_id}")
    if response.status_code == 404:
        return "Tarefa não encontrada", 404
    tarefa = response.json()
    return render_template('atualizar.html', tarefa=tarefa)

@app.route('/excluir/<int:tarefa_id>', methods=['POST'])
def excluir_tarefa(tarefa_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/tarefas/{tarefa_id}")
    if response.status_code == 200:
        return redirect(url_for('index'))
    return "Erro ao excluir tarefa", 500

#Rota para resetar o database
@app.route('/reset-database', methods=['GET'])
def resetar_database():
    response = requests.delete(f"{API_BASE_URL}/api/v1/tarefas/")
    
    if response.status_code == 200  :
        return render_template('confirmacao.html')
    else:
        return "Erro ao resetar o database", 500
 
if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')