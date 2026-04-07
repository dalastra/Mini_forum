from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

posts = [
    {
        "id": 1,
        "titulo": "Meu primeiro post",
        "resumo": "Uma breve apresentação do mini fórum feito com FastAPI.",
        "conteudo": "Este é o conteúdo completo do primeiro post. Aqui você pode mostrar o texto inteiro do post.",
        "autor": "Carlos",
    },
    {
        "id": 2,
        "titulo": "Segundo post",
        "resumo": "Exemplo de outro post salvo em memória.",
        "conteudo": "Todos os dados deste projeto ficam apenas em memória, sem uso de banco de dados.",
        "autor": "Ana",
    },
]


def buscar_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


def gerar_novo_id():
    if not posts:
        return 1
    return posts[-1]["id"] + 1


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"posts": posts},
    )


@app.get("/post/{id}")
async def visualizar_post(request: Request, id: int):
    post = buscar_post(id)
    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={"post": post},
    )


@app.get("/create")
async def pagina_criar(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={},
    )


@app.post("/create")
async def criar_post(request: Request):
    form = await request.form()

    novo_post = {
        "id": gerar_novo_id(),
        "titulo": form.get("titulo"),
        "resumo": form.get("resumo"),
        "conteudo": form.get("conteudo"),
        "autor": form.get("autor"),
    }

    posts.append(novo_post)
    return RedirectResponse(url="/", status_code=303)


@app.get("/edit/{id}")
async def pagina_editar(request: Request, id: int):
    post = buscar_post(id)
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"post": post},
    )


@app.post("/edit/{id}")
async def editar_post(request: Request, id: int):
    post = buscar_post(id)
    form = await request.form()

    if post is not None:
        post["titulo"] = form.get("titulo")
        post["resumo"] = form.get("resumo")
        post["conteudo"] = form.get("conteudo")
        post["autor"] = form.get("autor")

    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{id}")
async def excluir_post(id: int):
    post = buscar_post(id)
    if post is not None:
        posts.remove(post)

    return RedirectResponse(url="/", status_code=303)
