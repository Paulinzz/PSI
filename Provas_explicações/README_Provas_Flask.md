
# 📚 Explicação dos Códigos - Provas PSI (Flask)

Este arquivo contém explicações organizadas dos projetos Flask criados como simulações de provas avaliativas de Programação para Sistemas Internet.

---

## ✅ PROVA 1 - Projeto Base com Session em Memória

### Estrutura de Pastas:
- `app.py`: Arquivo principal da aplicação Flask.
- `templates/`: Contém os arquivos HTML da aplicação.
- `static/`: Contém o CSS.
- `requirements.txt`: Lista dos pacotes usados.

### Funcionalidades:
- Cadastro: Usuário e senha armazenados em dicionários.
- Login: Com `login_user`, sessão com `flask-login`, validação de senha com `check_password_hash`.
- Sessão: Login persistente até logout.
- Tarefas: Armazenadas por usuário na memória (dicionário global).
- Cookies: Saudação personalizada após login.
- Flash: Mensagens visuais para ações (erro, sucesso).
- Logout: Remove o usuário logado com `logout_user()`.

---

## ✅ PROVA 2 - Projeto com Session e Carrinho por Usuário

(Similar ao anterior, mas com ênfase em session por usuário)

### Extras:
- Cada usuário vê apenas suas tarefas.
- `@login_required`: Protege a rota `/tarefas`.
- `current_user.id`: Acessa o nome do usuário logado.
- `session` e `cookie`: Usados para personalizar e controlar a navegação.

---

## ✅ PROVA 3 - Versão com JSON como "banco de dados"

### Objetivo:
Persistir dados mesmo com o servidor sendo reiniciado, **sem banco real**.

### Novidades:
- `usuarios.json`: Armazena dados de login (criptografados).
- `tarefas.json`: Armazena tarefas por usuário.
- `ler_json(nome)`: Carrega um dicionário do arquivo .json.
- `salvar_json(nome, dados)`: Salva um dicionário no arquivo .json.

### Fluxo:
- Cadastro: Salva no JSON do usuário + inicializa sua lista de tarefas.
- Login: Lê o JSON e autentica.
- Adição/remoção de tarefas: Modifica o JSON de tarefas e salva.

### Por que usar JSON?
- Fácil de manipular sem banco.
- Útil para provas, protótipos ou POCs.
- Evita a necessidade de instalar SQLite/Postgre.

---

## 🧠 Dicas Finais para a Prova:

- Estude bem `session`, `flask-login`, `request.form`, `POST/GET` e `flash()`.
- Saiba como proteger rotas com `@login_required`.
- Entenda `@login_manager.user_loader` e a classe `UserMixin`.
- Saiba gerar `requirements.txt`: `pip freeze > requirements.txt`

Boa sorte! 🚀

