# Mini Fórum Web

Projeto desenvolvido em FastAPI + Jinja2, seguindo o padrão MVC.

## Como executar

1. Criar ambiente virtual:

```bash
python -m venv venv
```

2. Ativar ambiente virtual:

**Windows:**
```bash
venv\Scripts\activate.ps1
```

3. Instalar dependências:

```bash
pip install -r requirements.txt
```

4. Rodar servidor:

```bash
fastapi dev app.py
```

5. Abrir no navegador:

http://127.0.0.1:8000

---

## Funcionalidades

- Listar todos os posts  
- Visualizar um post completo  
- Criar novo post  
- Editar post existente  
- Excluir post  

---

## Tecnologias

- FastAPI: Framework web moderno  
- Jinja2: Motor de templates  
- FastAPI CLI: Execução do servidor  
- Dados em memória: Sem banco de dados  

---

## Estrutura

- `app.py`: Lógica da aplicação (Controller)  
- `templates/`: Interfaces HTML (View)  
- `static/`: Arquivos CSS, JS e imagens  
