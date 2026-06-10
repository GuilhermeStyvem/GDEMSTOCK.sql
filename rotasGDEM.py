from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List
from database import get_connection

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# MODELS
# ============================================

class UsuarioCadastro(BaseModel):
    nome: str
    email: str
    senha: str
    tipo_usuario: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class ProdutoCadastro(BaseModel):
    nome_produto: str
    descricao: str
    categoria: str
    preco: float
    quantidade_estoque: int
    status: str

class ClienteCadastro(BaseModel):
    nome_cliente: str
    cpf_cnpj: str
    email_empresa: str
    telefone: str
    endereco: str

class PedidoCadastro(BaseModel):
    cliente_id: int
    usuario_id: int
    forma_pagamento: str
    produtos: List[dict]

class MovimentacaoEstoque(BaseModel):
    id_produto: int
    tipo_movimentacoes: str
    quantidade: int
    observacao: str

# ============================================
# DEPENDÊNCIA ADMIN
# ============================================

async def verificar_admin(isAdmin: bool = Query(False)) -> bool:
    if not isAdmin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return isAdmin

# ============================================
# ROTAS -- USUÁRIO
# ============================================

@app.post("/usuario/cadastro")
async def cadastro_usuario(usuario: UsuarioCadastro):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO dbo.usuario (nome, email, senha, tipo_usuario)
            VALUES (?, ?, ?, ?)
        """, usuario.nome, usuario.email, usuario.senha, usuario.tipo_usuario)
        conn.commit()
        return {"message": "Usuário cadastrado com sucesso!", "dados": usuario.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.post("/usuarios/login")
async def login(login_data: UsuarioLogin):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id_usuario, nome, email, tipo_usuario
            FROM dbo.usuario
            WHERE email = ? AND senha = ?
        """, login_data.email, login_data.senha)
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=401, detail="Email ou senha inválidos")
        return {
            "message": "Login realizado com sucesso!",
            "dados": {
                "id_usuario":   usuario[0],
                "nome":         usuario[1],
                "email":        usuario[2],
                "tipo_usuario": usuario[3]
            }
        }
    finally:
        conn.close()

# ============================================
# ROTAS -- PRODUTO
# ============================================

@app.post("/produtos/cadastro")
async def cadastro_produto(produto: ProdutoCadastro):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO dbo.produto (nome_produto, descricao, categoria, preco, quantidade_estoque, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, produto.nome_produto, produto.descricao, produto.categoria,
             produto.preco, produto.quantidade_estoque, produto.status)
        conn.commit()
        return {"message": "Produto cadastrado com sucesso!", "dados": produto.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/produtos/listar")
async def listar_produtos():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id_produto, nome_produto, descricao, categoria, preco, quantidade_estoque, status
            FROM dbo.produto
        """)
        rows = cursor.fetchall()
        produtos = [
            {
                "id_produto":         r[0],
                "nome_produto":       r[1],
                "descricao":          r[2],
                "categoria":          r[3],
                "preco":              float(r[4]),
                "quantidade_estoque": r[5],
                "status":             r[6]
            }
            for r in rows
        ]
        return {"message": "Lista de produtos", "dados": produtos}
    finally:
        conn.close()

@app.put("/produtos/atualizar/{id}")
async def atualizar_produto(id: int, produto: ProdutoCadastro):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE dbo.produto
            SET nome_produto = ?, descricao = ?, categoria = ?,
                preco = ?, quantidade_estoque = ?, status = ?
            WHERE id_produto = ?
        """, produto.nome_produto, produto.descricao, produto.categoria,
             produto.preco, produto.quantidade_estoque, produto.status, id)
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Produto com ID:{id} não encontrado")
        conn.commit()
        return {"message": f"Produto com ID:{id} atualizado com sucesso!", "dados": produto.dict()}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.delete("/produtos/deletar/{id}")
async def deletar_produto(id: int, isAdmin: bool = Depends(verificar_admin)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM dbo.produto WHERE id_produto = ?", id)
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Produto com ID:{id} não encontrado")
        conn.commit()
        return {"message": f"Produto com ID:{id} deletado com sucesso!"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# ============================================
# ROTAS -- CLIENTES
# ============================================

@app.post("/clientes/cadastro")
async def cadastro_cliente(cliente: ClienteCadastro):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO dbo.clientes (nome_cliente, cpf_cnpj, telefone, email_empresa, endereco)
            VALUES (?, ?, ?, ?, ?)
        """, cliente.nome_cliente, cliente.cpf_cnpj, cliente.telefone,
             cliente.email_empresa, cliente.endereco)
        conn.commit()
        return {"message": "Cliente cadastrado com sucesso!", "dados": cliente.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/clientes/listar/{id}")
async def listar_cliente(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id_cliente, nome_cliente, cpf_cnpj, telefone, email_empresa, endereco
            FROM dbo.clientes
            WHERE id_cliente = ?
        """, id)
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Cliente com ID:{id} não encontrado")
        return {
            "message": f"Cliente com ID:{id} listado com sucesso!",
            "dados": {
                "id_cliente":    row[0],
                "nome_cliente":  row[1],
                "cpf_cnpj":      row[2],
                "telefone":      row[3],
                "email_empresa": row[4],
                "endereco":      row[5]
            }
        }
    finally:
        conn.close()

@app.get("/clientes/listar")
async def listar_todos_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id_cliente, nome_cliente, cpf_cnpj, telefone, email_empresa, endereco
            FROM dbo.clientes
        """)
        rows = cursor.fetchall()
        clientes = [
            {
                "id_cliente":    r[0],
                "nome_cliente":  r[1],
                "cpf_cnpj":      r[2],
                "telefone":      r[3],
                "email_empresa": r[4],
                "endereco":      r[5]
            }
            for r in rows
        ]
        return {"message": "Lista de clientes", "dados": clientes}
    finally:
        conn.close()

# ============================================
# ROTAS -- PEDIDOS
# ============================================

@app.post("/criar_pedidos")
async def criar_pedido(pedido: PedidoCadastro):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        valor_total = sum(p["preco_unitario"] * p["quantidade"] for p in pedido.produtos)

        cursor.execute("""
            INSERT INTO dbo.pedidos (id_cliente, id_usuario, valor_total, forma_pagamento, status)
            OUTPUT INSERTED.id_pedido
            VALUES (?, ?, ?, ?, ?)
        """, pedido.cliente_id, pedido.usuario_id, valor_total, pedido.forma_pagamento, "pendente")
        id_pedido = cursor.fetchone()[0]

        for p in pedido.produtos:
            subtotal = p["preco_unitario"] * p["quantidade"]
            cursor.execute("""
                INSERT INTO dbo.itens_pedido (id_pedido, id_produto, quantidade, preco_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, id_pedido, p["id_produto"], p["quantidade"], p["preco_unitario"], subtotal)

            cursor.execute("""
                UPDATE dbo.produto
                SET quantidade_estoque = quantidade_estoque - ?
                WHERE id_produto = ?
            """, p["quantidade"], p["id_produto"])

        conn.commit()
        return {
            "message": "Pedido criado com sucesso!",
            "dados": {
                "id_pedido":       id_pedido,
                "cliente_id":      pedido.cliente_id,
                "forma_pagamento": pedido.forma_pagamento,
                "valor_total":     valor_total,
                "status":          "pendente",
                "produtos":        pedido.produtos
            }
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# ============================================
# ROTAS -- MOVIMENTAÇÕES DE ESTOQUE
# ============================================

@app.post("/estoque/movimentacoes")
async def movimentacao_estoque(mov: MovimentacaoEstoque):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO dbo.movimentacoes_estoque (id_produto, tipo_movimentacoes, quantidade, observacao)
            VALUES (?, ?, ?, ?)
        """, mov.id_produto, mov.tipo_movimentacoes, mov.quantidade, mov.observacao)

        if mov.tipo_movimentacoes == "entrada":
            cursor.execute("""
                UPDATE dbo.produto SET quantidade_estoque = quantidade_estoque + ?
                WHERE id_produto = ?
            """, mov.quantidade, mov.id_produto)
        elif mov.tipo_movimentacoes == "saida":
            cursor.execute("""
                UPDATE dbo.produto SET quantidade_estoque = quantidade_estoque - ?
                WHERE id_produto = ?
            """, mov.quantidade, mov.id_produto)

        conn.commit()
        return {"message": "Movimentação de estoque registrada com sucesso!", "dados": mov.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/estoque/movimentacoes")
async def listar_movimentacoes():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT m.id_movimentacoes, p.nome_produto, m.tipo_movimentacoes,
                   m.quantidade, m.data_movimentacao, m.observacao
            FROM dbo.movimentacoes_estoque m
            JOIN dbo.produto p ON m.id_produto = p.id_produto
            ORDER BY m.data_movimentacao DESC
        """)
        rows = cursor.fetchall()
        movimentacoes = [
            {
                "id_movimentacoes":  r[0],
                "nome_produto":      r[1],
                "tipo_movimentacao": r[2],
                "quantidade":        r[3],
                "data_movimentacao": str(r[4]),
                "observacao":        r[5]
            }
            for r in rows
        ]
        return {"message": "Lista de movimentações", "dados": movimentacoes}
    finally:
        conn.close()
