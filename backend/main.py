from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncpg
import os

app = FastAPI()

async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/tarefas")
    return await asyncpg.connect(DATABASE_URL)

class Tarefa(BaseModel):
    id: Optional[int] = None
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False

@app.post("/api/v1/tarefas/", status_code=201)
async def adicionar_tarefa(tarefa: Tarefa):
    conn = await get_database()
    try:
        query = "INSERT INTO tarefas (titulo, descricao, concluida) VALUES ($1, $2, $3)"
        await conn.execute(query, tarefa.titulo, tarefa.descricao, tarefa.concluida)
        return {"message": "Tarefa adicionada com sucesso!"}
    finally:
        await conn.close()

@app.get("/api/v1/tarefas/", response_model=List[Tarefa])
async def listar_tarefas():
    conn = await get_database()
    try:
        query = "SELECT * FROM tarefas"
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]
    finally:
        await conn.close()

@app.get("/api/v1/tarefas/{tarefa_id}")
async def buscar_tarefa(tarefa_id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM tarefas WHERE id = $1"
        tarefa = await conn.fetchrow(query, tarefa_id)
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
        return dict(tarefa)
    finally:
        await conn.close()

@app.patch("/api/v1/tarefas/{tarefa_id}")
async def atualizar_tarefa(tarefa_id: int, tarefa: Tarefa):
    conn = await get_database()
    try:
        query = "UPDATE tarefas SET titulo = COALESCE($1, titulo), descricao = COALESCE($2, descricao), concluida = COALESCE($3, concluida) WHERE id = $4"
        await conn.execute(query, tarefa.titulo, tarefa.descricao, tarefa.concluida, tarefa_id)
        return {"message": "Tarefa atualizada com sucesso!"}
    finally:
        await conn.close()

@app.delete("/api/v1/tarefas/{tarefa_id}")
async def excluir_tarefa(tarefa_id: int):
    conn = await get_database()
    try:
        query = "DELETE FROM tarefas WHERE id = $1"
        await conn.execute(query, tarefa_id)
        return {"message": "Tarefa excluída com sucesso!"}
    finally:
        await conn.close()
