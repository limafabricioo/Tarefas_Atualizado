from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de tarefas
tarefas = []

# Rotas
@app.route('/api/tarefas', methods=['GET'])
def get_tarefas():
    return jsonify(tarefas)

@app.route('/api/adicionar_tarefa', methods=['POST'])
def adicionar_tarefa():
    nova_tarefa = request.json
    tarefas.append(nova_tarefa)
    return jsonify({'message': 'Tarefa adicionada com sucesso!'})

@app.route('/api/alterar_status/<nome>', methods=['PUT'])
def alterar_status(nome):
    for tarefa in tarefas:
        if tarefa['nome'] == nome:
            tarefa['status'] = request.json['status']
            return jsonify({'message': 'Status da tarefa alterado com sucesso!'})
    return jsonify({'error': 'Tarefa não encontrada!'}), 404

@app.route('/api/excluir_tarefa/<nome>', methods=['DELETE'])
def excluir_tarefa(nome):
    for tarefa in tarefas:
        if tarefa['nome'] == nome:
            tarefas.remove(tarefa)
            return jsonify({'message': 'Tarefa excluída com sucesso!'})
    return jsonify({'error': 'Tarefa não encontrada!'}), 404

# Inicialização do servidor
if __name__ == '__main__':
    app.run(debug=True)

