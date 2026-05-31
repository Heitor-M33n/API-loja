-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

-- Drop table

-- DROP TABLE public.clientes;

CREATE TABLE IF NOT EXISTS public.clientes (
	id_cliente serial4 NOT NULL,
	nome varchar(100) NOT NULL,
	email varchar(100) NULL,
	cpf varchar(11) NULL,
	CONSTRAINT clientes_pkey PRIMARY KEY (id_cliente)
);

-- Drop table

-- DROP TABLE public.estoque;

CREATE TABLE IF NOT EXISTS public.estoque (
	id_estoque serial4 NOT NULL,
	id_produto int4 NOT NULL,
	quantidade int4 NOT NULL,
	CONSTRAINT estoque_pkey PRIMARY KEY (id_estoque),
	CONSTRAINT estoque_id_produto_fkey FOREIGN KEY (id_produto) REFERENCES public.produtos(id_produto) ON DELETE CASCADE
);

-- Drop table

-- DROP TABLE public.pedidos;

CREATE TABLE IF NOT EXISTS public.pedidos (
	id_pedido serial4 NOT NULL,
	id_cliente int4 NOT NULL,
	data_pedido date DEFAULT CURRENT_DATE NOT NULL,
	CONSTRAINT pedidos_pkey PRIMARY KEY (id_pedido),
	CONSTRAINT pedidos_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES public.clientes(id_cliente) ON DELETE CASCADE
);

-- Drop table

-- DROP TABLE public.produtos;

CREATE TABLE IF NOT EXISTS public.produtos (
	id_produto int4 DEFAULT nextval('produto_id_produto_seq'::regclass) NOT NULL,
	nome_produto varchar NULL,
	preco numeric(10, 2) NULL,
	CONSTRAINT produto_pkey PRIMARY KEY (id_produto)
);

-- Drop table

-- DROP TABLE public.produto_pedido;

CREATE TABLE IF NOT EXISTS public.produto_pedido (
	id_item_pedido serial4 NOT NULL,
	id_pedido int4 NOT NULL,
	id_produto int4 NOT NULL,
	quantidade int4 NOT NULL,
	CONSTRAINT produto_pedido_pkey PRIMARY KEY (id_item_pedido),
	CONSTRAINT produto_pedido_id_pedido_fkey FOREIGN KEY (id_pedido) REFERENCES public.pedidos(id_pedido) ON DELETE CASCADE,
	CONSTRAINT produto_pedido_id_produto_fkey FOREIGN KEY (id_produto) REFERENCES public.produtos(id_produto) ON DELETE CASCADE
);