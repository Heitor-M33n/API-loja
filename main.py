from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import asyncpg
from typing import List

app = FastAPI(title="API Loja de Café - IFRN")

DATABASE_URL = "postgresql://postgres:%23Ngpc2008@localhost:5432/Loja%20de%20café"

async def get_db_connection():
    try:
        return await asyncpg.connect(DATABASE_URL)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao conectar ao banco de dados: {str(e)}"
        )

class ProdutoSchema(BaseModel):
    nome_produto: str
    preco: float

class ProdutoResponse(BaseModel):
    id_produto: int
    nome_produto: str
    preco: float

class EstoqueResponse(BaseModel):
    id_produto: int
    quantidade: int


@app.post("/produtos/criar", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar_produto(produto: ProdutoSchema):
    conn = await get_db_connection()
    try:
        query = """
            INSERT INTO public.produtos (nome_produto, preco) 
            VALUES ($1, $2) 
            RETURNING id_produto, nome_produto, preco;
        """
        row = await conn.fetchrow(query, produto.nome_produto, produto.preco)
        return dict(row)
    finally:
        await conn.close()


@app.get("/produtos", response_model=List[ProdutoResponse])
async def listar_produtos():
    conn = await get_db_connection()
    try:
        query = """
            SELECT id_produto, nome_produto, preco FROM public.produtos ORDER BY id_produto;
        """
        rows = await conn.fetch(query)
        
        return [dict(row) for row in rows]
    finally:
        await conn.close()


@app.get("/produtos/{id}", response_model=ProdutoResponse)
async def buscar_produto_por_id(id: int):
    conn = await get_db_connection()
    try:
        query = """
            SELECT id_produto, nome_produto, preco FROM public.produtos WHERE id_produto = $1;
            """
        row = await conn.fetchrow(query, id)
        
        if not row:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
            
        return dict(row)
    finally:
        await conn.close()

@app.put("/produtos/atualizar/{id}", response_model=ProdutoResponse)
async def atualizar_produto(id: int, produto: ProdutoSchema):
    conn = await get_db_connection()
    try:
        check_query = """
            SELECT id_produto FROM public.produtos WHERE id_produto = $1;
            """
        exists = await conn.fetchval(check_query, id)
        if not exists:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
            
        query = """
            UPDATE public.produtos 
            SET nome_produto = $1, preco = $2 
            WHERE id_produto = $3 
            RETURNING id_produto, nome_produto, preco;
        """
        row = await conn.fetchrow(query, produto.nome_produto, produto.preco, id)
        return dict(row)
    finally:
        await conn.close()


@app.delete("/produtos/deletar/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_produto(id: int):
    conn = await get_db_connection()
    try:
        check_query = """
            SELECT id_produto FROM public.produtos WHERE id_produto = $1;
            """
        exists = await conn.fetchval(check_query, id)
        if not exists:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
            
        query = "DELETE FROM public.produtos WHERE id_produto = $1;"
        await conn.execute(query, id)
        return None
    finally:
        await conn.close()


@app.put("/estoque/atualizar/{id}", response_model=EstoqueResponse)
async def atualizar_estoque(id: int, quantidade: int):
    conn = await get_db_connection()
    try:
        check_query = """
            SELECT id_produto FROM public.estoque WHERE id_produto = $1;
        """
        exists = await conn.fetchval(check_query, id)
        if not exists:
            raise HTTPException(status_code=404, detail="Registro de estoque para este produto não encontrado")

        query = """
            UPDATE public.estoque 
            SET quantidade = $1 
            WHERE id_produto = $2 
            RETURNING id_produto, quantidade;
        """
        row = await conn.fetchrow(query, quantidade, id)
        return dict(row)
    finally:
        await conn.close()