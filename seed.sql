INSERT INTO public.clientes (nome, email, cpf) VALUES
	('Carlos Silva', 'carlos@email.com', '12345678901'),
	('Ana Souza', 'ana.souza@email.com', '23456789012'),
	('Marcos Pereira', 'marcos.p@email.com', '34567890123'),
	('Julia Costa', 'julia.c@email.com', '45678901234'),
	('Fernanda Lima', 'fernanda.l@email.com', '56789012345');

INSERT INTO public.produtos (produto, estoque, preco) VALUES
	('Café Espresso Tradicional', 100, 8.00),
	('Café Cappuccino Italiano', 70, 12.00),
	('Fatia de Bolo de Cenoura', 20, 10.00),
	('Pão de Queijo Recheado', 30, 7.00),
	('Café Coado na Mesa', 60, 6.00);

INSERT INTO public.pedidos (id_cliente, id_produto) VALUES
	(1, 1),
	(2, 2),
	(3, 3),
	(4, 3),
	(5, 4);
