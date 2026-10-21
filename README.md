# Gerenciador de Tarefas CLI

Aplicação de linha de comando em Python para gerenciar tarefas, com dados salvos em JSON.
Sem dependências externas (somente biblioteca padrão).

## Uso
```bash
python tarefas.py add "Estudar para a entrevista"
python tarefas.py list
python tarefas.py list --pendentes
python tarefas.py done 1
python tarefas.py rm 1
```

## Conceitos aplicados
- `argparse` com subcomandos
- Leitura e escrita de JSON
- Funções pequenas com responsabilidade única
- Type hints
