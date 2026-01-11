# Studio Beauty Manager

**Studio Beauty Manager** é uma aplicação Desktop desenvolvida em Python para gerenciamento de estúdios de beleza. O objetivo é facilitar o cadastro de clientes, agendamentos e controle de serviços.

## Tecnologias Utilizadas
- **Linguagem**: Python 3
- **Interface Gráfica**: Tkinter (Nativo do Python)
- **Banco de Dados**: SQLite

## Estrutura do Projeto (Arquitetura Modular)
O projeto segue uma arquitetura modular para separar responsabilidades:

- **`main.py`**: Ponto de entrada da aplicação. Inicializa a janela principal.
- **`database.py`**: Gerencia a conexão com o banco de dados SQLite e execução de queries.
- **`controllers.py`**: Camada lógica que conecta a interface (UI) com o banco de dados. Contém as regras de negócio.
- **`ui.py`**: Contém as classes da interface gráfica (Janelas, Frames, Botões, etc).

## Como Rodar a Aplicação

Certifique-se de ter o Python instalado.

1. Clone o repositório (se ainda não o fez).
2. Execute o arquivo principal:
   ```bash
   python main.py
   ```

---
*Projeto em desenvolvimento.*
