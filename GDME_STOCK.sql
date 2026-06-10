-- ============================================
-- DROP E RECRIAÇÃO DO BANCO DE DADOS
-- ============================================
USE master;

GO

IF EXISTS (SELECT name FROM sys.databases WHERE name = 'GDME_STOCK')
BEGIN
    ALTER DATABASE GDME_STOCK SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE GDME_STOCK;
END
GO

CREATE DATABASE GDME_STOCK;
GO

USE GDME_STOCK;
GO

-- ============================================
-- CRIAÇÃO DAS TABELAS
-- ============================================

CREATE TABLE dbo.usuario (
    id_usuario      INT          PRIMARY KEY IDENTITY(1,1),
    nome            VARCHAR(150) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    senha           VARCHAR(150) NOT NULL,
    tipo_usuario    VARCHAR(15)  NOT NULL,
    data_criacao    DATETIME     NOT NULL DEFAULT GETDATE()
);
GO

CREATE TABLE dbo.produto (
    id_produto          INT            PRIMARY KEY IDENTITY(1,1),
    nome_produto        VARCHAR(100)   NOT NULL,
    descricao           VARCHAR(50)    NOT NULL,
    categoria           VARCHAR(20)    NOT NULL,
    preco               DECIMAL(10,2)  NOT NULL,
    quantidade_estoque  INT            NOT NULL,
    status              VARCHAR(15)    NOT NULL,
    data_cadastro       DATETIME       NOT NULL DEFAULT GETDATE()
);
GO

CREATE TABLE dbo.clientes (
    id_cliente      INT          PRIMARY KEY IDENTITY(1,1),
    nome_cliente    VARCHAR(50)  NOT NULL,
    cpf_cnpj        VARCHAR(18)  NOT NULL UNIQUE,
    telefone        VARCHAR(15)  NOT NULL,
    email_empresa   VARCHAR(50)  NOT NULL,
    endereco        VARCHAR(150) NOT NULL,
    data_cadastro   DATETIME     NOT NULL DEFAULT GETDATE()
);
GO

CREATE TABLE dbo.pedidos (
    id_pedido        INT           PRIMARY KEY IDENTITY(1,1),
    id_cliente       INT           NOT NULL,
    id_usuario       INT           NOT NULL,
    data_pedido      DATETIME      NOT NULL DEFAULT GETDATE(),
    valor_total      DECIMAL(10,2) NOT NULL,
    forma_pagamento  VARCHAR(30)   NOT NULL,
    status           VARCHAR(15)   NOT NULL,
    CONSTRAINT FK_Pedidos_Clientes FOREIGN KEY (id_cliente) REFERENCES dbo.clientes(id_cliente),
    CONSTRAINT FK_Pedidos_Usuario  FOREIGN KEY (id_usuario) REFERENCES dbo.usuario(id_usuario)
);
GO

CREATE TABLE dbo.itens_pedido (
    id_item         INT           PRIMARY KEY IDENTITY(1,1),
    id_pedido       INT           NOT NULL,
    id_produto      INT           NOT NULL,
    quantidade      INT           NOT NULL,
    preco_unitario  DECIMAL(10,2) NOT NULL,
    subtotal        DECIMAL(10,2) NOT NULL,
    CONSTRAINT FK_Itens_Pedidos  FOREIGN KEY (id_pedido)  REFERENCES dbo.pedidos(id_pedido),
    CONSTRAINT FK_Itens_Produto  FOREIGN KEY (id_produto) REFERENCES dbo.produto(id_produto)
);
GO

CREATE TABLE dbo.movimentacoes_estoque (
    id_movimentacoes    INT          PRIMARY KEY IDENTITY(1,1),
    id_produto          INT          NOT NULL,
    tipo_movimentacoes  VARCHAR(15)  NOT NULL,
    quantidade          INT          NOT NULL,
    data_movimentacao   DATETIME     NOT NULL DEFAULT GETDATE(),
    observacao          VARCHAR(100),
    CONSTRAINT FK_Movimentacao_Produto FOREIGN KEY (id_produto) REFERENCES dbo.produto(id_produto)
);
GO

-- ============================================
-- INSERT -- dbo.usuario
-- ============================================
INSERT INTO dbo.usuario (nome, email, senha, tipo_usuario) VALUES
('Guilherme', 'guigui@gdme.com', 'senha123', 'admin'),
('Marcos',    'tutucho@gdme.com',    'senha123', 'operador'),
('Douglas',   'dodo@gdme.com',   'senha123', 'operador'),
('Esther',    'ester@gdme.com',    'senha123', 'gerente'),
('Thiago',    'tiago@gdme.com',    'senha123', 'operador'),
('Vitooria',  'vitoria@gdme.com',  'senha123', 'admin');

GO

-- ============================================
-- INSERT -- dbo.produto
-- ============================================
INSERT INTO dbo.produto (nome_produto, descricao, categoria, preco, quantidade_estoque, status) VALUES
('Notebook Dell',      'Notebook i5 8GB RAM',    'Informatica', 3200.00, 15, 'ativo'),
('Mouse Logitech',     'Mouse sem fio 1200dpi',  'Informatica',  150.00, 80, 'ativo'),
('Teclado Mecanico',   'Teclado switch blue',    'Informatica',  350.00, 40, 'ativo'),
('Monitor 24"',        'Monitor Full HD IPS',    'Informatica', 1200.00, 20, 'ativo'),
('Cadeira Gamer',      'Cadeira ergonomica',     'Moveis',       950.00, 10, 'ativo'),
('Mesa Escritorio',    'Mesa 1.50m MDF',         'Moveis',       600.00,  8, 'ativo'),
('Headset Sony',       'Headset com microfone',  'Audio',        280.00, 30, 'ativo'),
('Webcam Full HD',     'Webcam 1080p USB',       'Informatica',  220.00, 25, 'ativo'),
('Impressora HP',      'Impressora jato tinta',  'Informatica',  750.00, 12, 'ativo'),
('Pendrive 64GB',      'Pendrive USB 3.0',       'Informatica',   60.00, 100,'ativo');
GO

-- ============================================
-- INSERT -- dbo.clientes
-- ============================================
INSERT INTO dbo.clientes (nome_cliente, cpf_cnpj, telefone, email_empresa, endereco) VALUES
('Tech Solutions Ltda',  '12.345.678/0001-90', '(61)99101-0001', 'contato@tech.com',    'SIG Quadra 01 Lote 10, Brasilia-DF'),
('InfoParts SA',         '23.456.789/0001-01', '(61)99101-0002', 'compras@infoparts.com','SCS Quadra 02 Bloco B, Brasilia-DF'),
('Mega Office Ltda',     '34.567.890/0001-12', '(61)99101-0003', 'nf@megaoffice.com',   'SCN Quadra 03 Lote 5, Brasilia-DF'),
('DataSys Corp',         '45.678.901/0001-23', '(11)98800-0004', 'ti@datasys.com',      'Av. Paulista 1000, Sao Paulo-SP'),
('StartHub Tecnologia',  '56.789.012/0001-34', '(21)97700-0005', 'rh@starthub.com',     'Rua XV de Novembro 200, Rio-RJ');
GO

-- ============================================
-- INSERT -- dbo.pedidos
-- ============================================
INSERT INTO dbo.pedidos (id_cliente, id_usuario, valor_total, forma_pagamento, status) VALUES
(1, 1,  4850.00, 'Boleto',          'concluido'),
(2, 2,  1500.00, 'Cartao Credito',  'concluido'),
(3, 3,  2400.00, 'Pix',             'concluido'),
(4, 4,  9600.00, 'Transferencia',   'pendente'),
(5, 5,  1130.00, 'Boleto',          'concluido'),
(1, 6,  3150.00, 'Pix',             'pendente'),
(2, 1,   720.00, 'Cartao Debito',   'cancelado'),
(3, 2,  2200.00, 'Boleto',          'concluido'),
(4, 3,  4400.00, 'Cartao Credito',  'concluido'),
(5, 4,  1800.00, 'Pix',             'pendente');
GO

-- ============================================
-- INSERT -- dbo.itens_pedido
-- ============================================
INSERT INTO dbo.itens_pedido (id_pedido, id_produto, quantidade, preco_unitario, subtotal) VALUES
(1,  1, 1, 3200.00, 3200.00),
(1,  2, 2,  150.00,  300.00),
(1,  3, 1,  350.00,  350.00),
(2,  2, 4,  150.00,  600.00),
(2,  7, 2,  280.00,  560.00),
(2,  3, 1,  350.00,  350.00),
(3,  4, 2, 1200.00, 2400.00),
(4,  1, 3, 3200.00, 9600.00),
(5,  5, 1,  950.00,  950.00),
(5,  9, 1,  750.00,  750.00),  -- ajuste: 950+750=1700 (pedido 5 valor_total era 1130; corrigido abaixo via UPDATE)
(6,  6, 1,  600.00,  600.00),
(6,  8, 2,  220.00,  440.00),
(6,  3, 2,  350.00,  700.00),
(7, 10, 3,   60.00,  180.00),
(7,  2, 2,  150.00,  300.00),
(7,  9, 1,  750.00,  750.00),
(8,  4, 1, 1200.00, 1200.00),
(8,  1, 1, 3200.00, 3200.00),  -- subtotal maior; pedido 8 era 2200; UPDATE abaixo
(9,  1, 1, 3200.00, 3200.00),
(9,  4, 1, 1200.00, 1200.00),
(10, 5, 1,  950.00,  950.00),
(10, 7, 3,  280.00,  840.00);
GO

-- Corrige valor_total dos pedidos para bater com os itens inseridos
UPDATE dbo.pedidos SET valor_total = 3850.00  WHERE id_pedido = 1;
UPDATE dbo.pedidos SET valor_total = 1510.00  WHERE id_pedido = 2;
UPDATE dbo.pedidos SET valor_total = 2400.00  WHERE id_pedido = 3;
UPDATE dbo.pedidos SET valor_total = 9600.00  WHERE id_pedido = 4;
UPDATE dbo.pedidos SET valor_total = 1700.00  WHERE id_pedido = 5;
UPDATE dbo.pedidos SET valor_total = 1740.00  WHERE id_pedido = 6;
UPDATE dbo.pedidos SET valor_total = 1230.00  WHERE id_pedido = 7;
UPDATE dbo.pedidos SET valor_total = 4400.00  WHERE id_pedido = 8;
UPDATE dbo.pedidos SET valor_total = 4400.00  WHERE id_pedido = 9;
UPDATE dbo.pedidos SET valor_total = 1790.00  WHERE id_pedido = 10;
GO

-- ============================================
-- INSERT -- dbo.movimentacoes_estoque
-- ============================================
INSERT INTO dbo.movimentacoes_estoque (id_produto, tipo_movimentacoes, quantidade, observacao) VALUES
(1,  'entrada',  20, 'Compra inicial de estoque'),
(1,  'saida',     5, 'Vendas pedidos 4 e 8 e 9'),
(2,  'entrada', 100, 'Compra inicial de estoque'),
(2,  'saida',    10, 'Vendas pedidos 1, 2 e 7'),
(3,  'entrada',  50, 'Compra inicial de estoque'),
(3,  'saida',     4, 'Vendas pedidos 1, 2 e 6'),
(4,  'entrada',  25, 'Compra inicial de estoque'),
(4,  'saida',     4, 'Vendas pedidos 3, 8 e 9'),
(5,  'entrada',  15, 'Compra inicial de estoque'),
(5,  'saida',     2, 'Vendas pedidos 5 e 10'),
(6,  'entrada',  10, 'Compra inicial de estoque'),
(6,  'saida',     1, 'Venda pedido 6'),
(7,  'entrada',  35, 'Compra inicial de estoque'),
(7,  'saida',     5, 'Vendas pedidos 2 e 10'),
(8,  'entrada',  30, 'Compra inicial de estoque'),
(8,  'saida',     2, 'Venda pedido 6'),
(9,  'entrada',  15, 'Compra inicial de estoque'),
(9,  'saida',     2, 'Vendas pedidos 5 e 7'),
(10, 'entrada', 110, 'Compra inicial de estoque'),
(10, 'saida',     3, 'Venda pedido 7');
GO

-- ============================================
-- CONSULTAS (SELECTs)
-- ============================================

SELECT * FROM dbo.usuario;
GO

SELECT * FROM dbo.produto;
GO

SELECT * FROM dbo.clientes;
GO

SELECT * FROM dbo.pedidos;
GO

SELECT * FROM dbo.itens_pedido;
GO

SELECT * FROM dbo.movimentacoes_estoque;
GO
