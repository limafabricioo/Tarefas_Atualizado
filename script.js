document.addEventListener("DOMContentLoaded", function() {
    const tarefasDiv = document.getElementById('tarefas');

    function carregarTarefas() {
        fetch('/api/tarefas')
            .then(response => response.json())
            .then(data => {
                tarefasDiv.innerHTML = '';
                data.forEach(tarefa => {
                    const tarefaDiv = document.createElement('div');
                    tarefaDiv.classList.add('tarefa');
                    tarefaDiv.innerHTML = `
                        <strong>${tarefa.nome}</strong>: ${tarefa.descricao}
                        <button class="botao-alterar" data-nome="${tarefa.nome}">Alterar Status</button>
                        <button class="botao-excluir" data-nome="${tarefa.nome}">Excluir</button>
                    `;
                    tarefasDiv.appendChild(tarefaDiv);
                });
            });
    }

    function adicionarTarefa() {
        const nome = prompt('Digite o nome da tarefa:');
        const descricao = prompt('Digite a descrição da tarefa:');
        if (nome && descricao) {
            fetch('/api/adicionar_tarefa', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({nome, descricao})
            })
            .then(() => {
                carregarTarefas();
            });
        }
    }

    function alterarStatus(nomeTarefa) {
        fetch(`/api/alterar_status/${nomeTarefa}`)
            .then(() => {
                carregarTarefas();
            });
    }

    function excluirTarefa(nomeTarefa) {
        fetch(`/api/excluir_tarefa/${nomeTarefa}`, {
            method: 'DELETE'
        })
        .then(() => {
            carregarTarefas();
        });
    }

    document.getElementById('adicionar').addEventListener('click', adicionarTarefa);

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('botao-alterar')) {
            const nome = event.target.dataset.nome;
            alterarStatus(nome);
        } else if (event.target.classList.contains('botao-excluir')) {
            const nome = event.target.dataset.nome;
            excluirTarefa(nome);
        }
    });

    // Carregar tarefas quando a página for carregada
    carregarTarefas();
});
