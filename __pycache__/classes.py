import sqlite3
from datetime import date

class Task:
    def __init__(self, nome, descricao, data, status="Pendente"):
        self.nome = nome
        self.descricao = descricao
        self.data = data
        self.status = status

    def mudar_status(self, novo_status):
        self.status = novo_status

    def salvar_no_bd(self):
        conn = sqlite3.connect('tarefas.db')
        cursor = conn.cursor()
        # Criar a tabela se ela não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS tarefas (
                            nome TEXT,
                            descricao TEXT,
                            data DATE,
                            status TEXT
                          )''')
        cursor.execute('INSERT INTO tarefas VALUES (?, ?, ?, ?)', (self.nome, self.descricao, self.data, self.status))
        conn.commit()
        conn.close()

    @staticmethod
    def carregar_do_bd():
        conn = sqlite3.connect('tarefas.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tarefas')
        tarefas = cursor.fetchall()
        conn.close()
        return [Task(nome, descricao, data, status) for nome, descricao, data, status in tarefas]
    
    @staticmethod   
    def deletar_tarefa(nome):
        conn = sqlite3.connect('tarefas.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tarefas WHERE nome=?', (nome,))
        conn.commit()
        conn.close()

def adicionar_tarefa():
    nome_tarefa = input("Digite o nome da tarefa: ")
    descricao_tarefa = input("Digite a descrição desta tarefa: ")
    nova_tarefa = Task(nome_tarefa, descricao_tarefa, date.today())
    nova_tarefa.salvar_no_bd()
    print("Tarefa adicionada com sucesso.")

def listar_tarefas():
    tarefas = Task.carregar_do_bd()
    if not tarefas:
        print("Não há tarefas cadastradas.")
        return
    print("Tarefas cadastradas:")
    for i, tarefa in enumerate(tarefas, start=1):
        print(f"{i}. {tarefa.nome} - {tarefa.descricao} ({tarefa.status})")

def alterar_status():
    listar_tarefas()
    escolha = int(input("Escolha o número da tarefa que deseja alterar: "))
    novo_status = None
    while novo_status not in ["Pendente", "Em Andamento", "Concluida"]:
        opcao = input("Digite 2 para 'Em Andamento' ou 3 para 'Concluída': ")
        if opcao == '2':
            novo_status = 'Em Andamento'
        elif opcao == '3':
            novo_status = 'Concluida'
        else:
            print("Opção inválida.")
    tarefas = Task.carregar_do_bd()
    tarefa = tarefas[escolha - 1]
    tarefa.mudar_status(novo_status)
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tarefas SET status=? WHERE nome=?', (novo_status, tarefa.nome))
    conn.commit()
    conn.close()
    print("Status alterado com sucesso.")

def deletar_tarefa():
    listar_tarefas()
    escolha = int(input("Escolha o número da tarefa que deseja deletar: "))
    tarefas = Task.carregar_do_bd()
    tarefa = tarefas[escolha - 1]
    Task.deletar_tarefa(tarefa.nome)
    print("Tarefa deletada com sucesso.")    


while True:
    print("\n--- MENU ---")
    print("1. Adicionar nova tarefa")
    print("2. Listar tarefas")
    print("3. Alterar status de uma tarefa")
    print("4. Deletar uma tarefa")
    print("5. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        adicionar_tarefa()
    elif opcao == '2':
        listar_tarefas()
    elif opcao == '3':
        alterar_status()
    elif opcao == '4':
        deletar_tarefa()
    elif opcao == '5':
        print("Saindo...")
        break
    else:
        print("Opção inválida. Por favor, escolha novamente.")



