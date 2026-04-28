from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Post

app = FastAPI()

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Static + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Dependência do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# ROTAS
# =========================

@app.get("/")
async def index(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"posts": posts},
    )


@app.get("/post/{id}")
async def visualizar_post(request: Request, id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
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
async def criar_post(request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    novo_post = Post(
        titulo=form.get("titulo"),
        resumo=form.get("resumo"),
        conteudo=form.get("conteudo"),
        autor=form.get("autor"),
    )

    db.add(novo_post)
    db.commit()
    db.refresh(novo_post)

    return RedirectResponse(url="/", status_code=303)


@app.get("/edit/{id}")
async def pagina_editar(request: Request, id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"post": post},
    )


@app.post("/edit/{id}")
async def editar_post(request: Request, id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    form = await request.form()

    if post:
        post.titulo = form.get("titulo")
        post.resumo = form.get("resumo")
        post.conteudo = form.get("conteudo")
        post.autor = form.get("autor")

        db.commit()

    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{id}")
async def excluir_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()

    if post:
        db.delete(post)
        db.commit()

    return RedirectResponse(url="/", status_code=303)