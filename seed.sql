INSERT INTO public.clientes (nome, email, cpf) VALUES
	('Carlos Silva', 'carlos@email.com', '12345678901'),
	('Ana Souza', 'ana.souza@email.com', '23456789012'),
	('Marcos Pereira', 'marcos.p@email.com', '34567890123'),
	('Julia Costa', 'julia.c@email.com', '45678901234'),
	('Fernanda Lima', 'fernanda.l@email.com', '56789012345');

INSERT INTO public.produtos (nome_produto, preco) VALUES
	('Café Espresso Tradicional', 8.00),
	('Café Cappuccino Italiano', 12.00),
	('Fatia de Bolo de Cenoura', 10.00),
	('Pão de Queijo Recheado', 7.00),
	('Café Coado na Mesa', 6.00);

INSERT INTO public.estoque (id_produto, quantidade) VALUES
	(1, 150), 
	(2, 80),  
	(3, 15),  
	(4, 40),  
	(5, 200);

INSERT INTO public.pedidos (id_cliente, data_pedido) VALUES
	(1, '2026-05-25'),
	(2, '2026-05-26'),
	(3, '2026-05-27'),
	(4, '2026-05-28'),
	(5, '2026-05-29');

INSERT INTO public.produto_pedido (id_pedido, id_produto, quantidade) VALUES
	(1, 1, 2), 
	(1, 3, 1), 
	(2, 2, 1), 
	(3, 4, 3), 
	(4, 5, 1), 
	(5, 1, 1);