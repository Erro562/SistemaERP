import pymysql.cursors

#Conexão com o banco de dados
conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)
#inicializador de false para segurança
autentico = False

#Função para Organizar e facilitar uso e manutenção de codigo
def logarCadastrar():
    usuarioExistente = 0
    autenticado = False
    usuarioMaster = False

    if decisao == 1:
        nome = input("Digite seu nome: ")
        senha = input("Digite sua senha: ")

        #Percorre no banco de dados para verificar o login
        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False

        if not autenticado:
            print('Nome ou senha Errado')

    #Cadastra o Usuario
    elif decisao == 2:
        print('Faça seu cadastro')
        nome = input("Digite seu nome: ")
        senha = input("Digite sua senha: ")

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1

        if usuarioExistente == 1:
            print('Usuario já cadastrado tente um nome ou senha diferente')
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into cadastros(nome ,senha , nivel) values (%s , %s , %s)',(nome , senha, 1))
                    conexao.commit() #salva no banco de dados
                    print("Usuario cadastrado com sucesso!")

            except:
                print('Erro ao inserir os dados')

    return autenticado,usuarioMaster

def cadastrarProduto():
    nome = input('Digite o nome do produto: ')
    ingredientes = input('Digite os ingredientes do produto: ')
    grupo = input('Digite o grupo pertencente ao produto: ')
    preco = float(input('Digite o preço do produto: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into produtos (nome , ingredientes , grupo , preco) values(%s , %s ,%s ,%s)',(nome,ingredientes,grupo,preco))
            conexao.commit() #salva no banco de dados
            print('Produto Cadastrado com sucesso')

    except:
        print('Erro ao inserir o produto no banco de dados')

def listarProdutos():
    produtos = []

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtosCadastrados = cursor.fetchall()

    except:
        print('Erro ao conectar ao banco de dados')

    for i in produtosCadastrados:
        produtos.append(i)

    if len(produtos) != 0:
        for i in range(0, len(produtos)):
            print(produtos[i])
    else:
        print('Nenhum produto cadastrado')

def excluirProdutos():
    idDeletar = int(input('Digite o ID referente ao produto que deseja apagar: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('delete from produtos where id = {}'.format(idDeletar))
    except:
        print('erro ao excluir o produto')

def listarPedidos():
    pedidos = []
    decision = 0

    while decision != 2:
        pedidos.clear()

        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from pedidos')
                listarPedidos = cursor.fetchall()

        except:
            print('Erro no banco de dados')

        for i in listarPedidos:
            pedidos.append(i)

        if len(pedidos) != 0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])

        else:
            print("nenhum pedido foi feito")

        decision =int(input('Digite 1 para dar um produto como entregue e 2 para voltar'))

        if decision == 1:
            idDeletar = int(input('Digite o id do pedido entregue: '))

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('delete from pedidos where id = {}'.format(idDeletar))
                    print('produto dado como entregue')

            except:
                print('Erro ao dar pedido como entregue')

#loop Principal
while not autentico:
    decisao = int(input('Digite ( 1 ) para Logar e ( 2 ) para Cadastrar: '))

    try:
        with conexao.cursor() as cursor: #Abrindo a conexão
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()  #RETONA UM dicionario (printa as linhas do mysql)

    except:
        print('Error ao conectar no banco de dados')

    autentico,usuarioSupremo = logarCadastrar()

if autentico:
    print('autenticado')

    if usuarioSupremo == True:
        decisaoUsuario = 1

    while decisaoUsuario != 0:
        decisaoUsuario = int(input('Digite ( 0 ) para sair , ( 1 ) para cadastrar produtos , ( 2 ) para listar produtos cadastrados ( 3 ) para listar os pedidos: '))

        if decisaoUsuario == 1:
            cadastrarProduto()
        elif decisaoUsuario == 2:
            listarProdutos()

            delete = int(input('digite ( 1 ) para excluir e ( 2 ) para sair: '))
            if delete == 1:
                excluirProdutos()

        elif decisaoUsuario == 3:
            listarPedidos()
