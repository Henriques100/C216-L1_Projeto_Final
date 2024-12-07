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
    prazo: Optional[str] = None  # Prazo limite no formato ISO 8601
    diario: bool = False  # Indica se é uma tarefa diária


@app.post("/api/v1/tarefas/", status_code=201)
async def adicionar_tarefa(tarefa: Tarefa):
    conn = await get_database()
    try:
        query = """
            INSERT INTO tarefas (titulo, descricao, concluida, prazo, diario) 
            VALUES ($1, $2, $3, $4, $5)
        """
        await conn.execute(query, tarefa.titulo, tarefa.descricao, tarefa.concluida, tarefa.prazo, tarefa.diario)
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

@app.patch("/api/v1/tarefas/{tarefa_id}")
async def atualizar_tarefa(tarefa_id: int, tarefa: Tarefa):
    conn = await get_database()
    try:
        query = """
            UPDATE tarefas 
            SET 
                titulo = COALESCE($1, titulo), 
                descricao = COALESCE($2, descricao), 
                concluida = COALESCE($3, concluida),
                prazo = COALESCE($4, prazo),
                diario = COALESCE($5, diario)
            WHERE id = $6
        """
        await conn.execute(query, tarefa.titulo, tarefa.descricao, tarefa.concluida, tarefa.prazo, tarefa.diario, tarefa_id)
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

# 7. Resetar banco de dados
@app.delete("/api/v1/tarefas/")
async def resetar_tarefas():
    init_sql = os.getenv("INIT_SQL", "db/init.sql")
    conn = await get_database()
    try:
        # Read SQL file contents
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        # Execute SQL commands
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!"}
    finally:
        await conn.close()
