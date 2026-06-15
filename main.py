from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from pydantic import BaseModel
from typing import List
import bcrypt
import asyncpg

app = FastAPI(title="API Loja de Café - IFRN")

DATABASE_URL = "postgresql://postgres:%23Ngpc2008@localhost:5432/api_loja" #Alterar

async def get_db_connection():
    try:
        return await asyncpg.connect(DATABASE_URL)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao conectar ao banco de dados: {str(e)}"
        )


#Models
class ProdutoSchema(BaseModel):
    produto: str
    estoque: int
    preco: float

class UsuarioSchema(BaseModel):
    nome: str
    sobrenome: str
    email: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: str

class LoginSchema(BaseModel):
    email: str
    senha: str

class ClienteSchema(BaseModel):
    nome: str
    email: str
    cpf: str

class PedidoSchema(BaseModel):
    id_cliente: int
    id_produto: int

class ProdutoResponse(ProdutoSchema):
    id: int

class ClienteResponse(ClienteSchema):
    id: int

class PedidoResponse(PedidoSchema):
    id: int
    data: datetime

class PedidoResponseJoin(PedidoResponse):
    cliente: str
    produto: str
    preco: float

class PedidoPOST(PedidoSchema):
    debitar_estoque: bool

@app.get("/test")
async def testar_conexão_postgres():
    conn = await get_db_connection()
    await conn.close()
    return 'Conexão bem sucedida'



#CREATE
@app.post("/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar_produto(produto: ProdutoSchema):
    try:
        conn = await get_db_connection()
        row = await conn.fetchrow("""INSERT INTO public.produtos (produto, estoque, preco)
            VALUES ($1, $2, $3) RETURNING id, produto, estoque, preco;""", 
            produto.produto, produto.estoque, produto.preco)
        return dict(row)
    finally:
        await conn.close()

@app.post("/clientes", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def criar_cliente(cliente: ClienteSchema):
    try:
        conn = await get_db_connection()
        row = await conn.fetchrow("""INSERT INTO public.clientes (nome, email, cpf)
            VALUES ($1, $2, $3) RETURNING id, nome, email, cpf;""", 
            cliente.nome, cliente.email, cliente.cpf)
        return dict(row)
    finally:
        await conn.close()

@app.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def criar_usuario(usuario: UsuarioSchema):
    try:
        conn = await get_db_connection()

        senha_hash = bcrypt.hashpw(
            usuario.senha.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        row = await conn.fetchrow("""INSERT INTO public.usuarios (nome, sobrenome, email, senha)
            VALUES ($1, $2, $3, $4) RETURNING id, nome, sobrenome, email; """,
            usuario.nome, usuario.sobrenome, usuario.email, senha_hash)
        return dict(row)
    finally:
        await conn.close()

@app.post("/verificar-senha", status_code=status.HTTP_200_OK)
async def verificar_senha(login: LoginSchema):
    try:
        conn = await get_db_connection()

        usuario = await conn.fetchrow("""SELECT email, senha FROM public.usuarios WHERE email = $1""", 
        login.email)

        if usuario is None:
            return {"Resultado": "Usuário não encontrado."}

    
        senha_correta = bcrypt.checkpw(
            login.senha.encode("utf-8"),
            usuario["senha"].encode("utf-8")
        )

        if senha_correta:
            return {"Resultado": "Sucesso!"}
        
        return {"Resultado": "Senha incorreta!"}
    
    finally:
        await conn.close()

@app.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
async def criar_pedido(pedido: PedidoPOST):
    try:
        conn = await get_db_connection()

        #verifica se o produto existe
        produto = await conn.fetchrow("""SELECT * FROM public.produtos WHERE id = $1""", pedido.id_produto)
        if not produto:
            raise HTTPException(status_code=404, detail='Produto não existe')
        
        #verifica se tem estoque
        if pedido.debitar_estoque:
            if not dict(produto).get('estoque') > 0:
                raise HTTPException(status_code=400, detail='Estoque insuficiente')

        #verifica se o cliente existe
        cliente = await conn.fetchrow("""SELECT * FROM public.clientes WHERE id = $1""", pedido.id_cliente)
        if not cliente:
            raise HTTPException(status_code=404, detail='Cliente não existe')

        #faz o insert propriamente dito
        row = await conn.fetchrow("""INSERT INTO public.pedidos (id_cliente, id_produto)
            VALUES ($1, $2) RETURNING id, id_cliente, id_produto, data;""", 
            pedido.id_cliente, pedido.id_produto)
        
        #altera o estoque
        if pedido.debitar_estoque:
            await conn.execute("""UPDATE public.produtos SET estoque = estoque - 1 WHERE id = $1""", pedido.id_produto)

        return dict(row)
    finally:
        await conn.close()



#READ
@app.get("/produtos", response_model=List[ProdutoResponse], status_code=status.HTTP_200_OK)
async def listar_produtos():
    try:
        conn = await get_db_connection()
        rows = await conn.fetch("""SELECT * FROM public.produtos ORDER BY id;""")
        return [dict(row) for row in rows]
    finally:
        if conn:
            await conn.close()

@app.get("/produtos/{id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
async def buscar_produto_por_id(id: int):
    try:
        conn = await get_db_connection()
        row = await conn.fetchrow("""SELECT * FROM public.produtos WHERE id = $1;""", id)
        if not row:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
            
        return dict(row)
    finally:
        if conn:
            await conn.close()

@app.get("/clientes", response_model=List[ClienteResponse], status_code=status.HTTP_200_OK) 
async def listar_clientes():
    try:
        conn = await get_db_connection()
        rows = await conn.fetch("""SELECT * FROM public.clientes""")
        return [dict(row) for row in rows]
    finally:
        if conn:
            await conn.close()

@app.get("/clientes/{id}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
async def buscar_cliente_por_id(id: int):
    try:
        conn = await get_db_connection()
        row = await conn.fetchrow("""SELECT * FROM public.clientes WHERE id = $1""", id)
        if not row:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        return dict(row)
    finally:
        if conn:
            await conn.close()

@app.get("/pedidos", response_model=List[PedidoResponseJoin], status_code=status.HTTP_200_OK)
async def listar_pedidos():
    try:
        conn = await get_db_connection()
        rows = await conn.fetch("""SELECT pe.id, c.id AS id_cliente, pr.id AS id_produto, c.nome AS cliente, 
            pr.produto, pr.preco AS preco, pe.data FROM public.pedidos pe
            INNER JOIN public.produtos pr ON pe.id_produto = pr.id
            INNER JOIN public.clientes c ON pe.id_cliente = c.id""")
        return [dict(row) for row in rows]
    finally:
        if conn:
            await conn.close()

@app.get("/pedidos/{id}", response_model=PedidoResponse, status_code=status.HTTP_200_OK)
async def buscar_pedido_por_id(id: int):
    try:
        conn = await get_db_connection()
        row = await conn.fetchrow("""SELECT pe.id, c.id AS id_cliente, pr.id AS id_produto, c.nome AS cliente, 
            pr.produto, pr.preco AS preco, pe.data FROM public.pedidos pe
            INNER JOIN public.produtos pr ON pe.id_produto = pr.id
            INNER JOIN public.clientes c ON pe.id_cliente = c.id WHERE pe.id = $1""", id)
        if not row:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return dict(row)
    finally:
        if conn:
            await conn.close()



#UPDATE
@app.put("/produtos/{id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
async def atualizar_produto(id: int, produto: ProdutoSchema):
    try:
        conn = await get_db_connection()
        row = await conn.fetchrow("""UPDATE public.produtos SET produto = $1, estoque = $2, preco = $3
            WHERE id = $4 RETURNING id, produto, estoque, preco;""", 
            produto.produto, produto.estoque, produto.preco, id)
        return dict(row)
    finally:
        await conn.close()

@app.put("/clientes/{id}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
async def atualizar_cliente(id: int, cliente: ClienteSchema):
    try:
        conn = await get_db_connection()        
        row = await conn.fetchrow("""UPDATE public.clientes SET nome = $1, email = $2, cpf = $3
            WHERE id = $4 RETURNING id, nome, email, cpf;""",
            cliente.nome, cliente.email, cliente.cpf, id)
        return dict(row)
    finally:
        await conn.close()



#DELETE
@app.delete("/produtos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_produto(id: int):
    try:
        conn = await get_db_connection()
        row = await conn.fetchrow("DELETE FROM public.produtos WHERE id = $1 RETURNING *", id)
        if not row:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
    finally:
        await conn.close()

@app.delete("/clientes/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_cliente(id: int):
    try:
        conn = await get_db_connection()
        row = await conn.fetchrow("DELETE FROM public.clientes WHERE id = $1 RETURNING *", id)
        if not row:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
    finally:
        await conn.close()

@app.delete("/pedidos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_pedido(id: int):
    try:
        conn = await get_db_connection()
        row = await conn.fetchrow("DELETE FROM public.pedidos WHERE id = $1 RETURNING *", id)
        if not row:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
    finally:
        await conn.close()