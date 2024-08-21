# ---------------------------- CONEXÃO AO BANCO DE DADOS -----------------------
import os
import oracledb
connection = oracledb.connect(
    user = "BD150224424",
    password = 'Qwiji4',    
    dsn = "172.16.12.14/xe")
print("Successfully Connected")
cursor = connection.cursor()
#
alfanumerico = 'ZABCDEFGHIJKLMNOPQRSTUVWXY'
chave = [[4, 3], [1, 2]]
chave_inversa = [[42, -63], [-21, 84]]
#
def hill_criptografia(desc_prod, chave): #CRIPTOGRAFA E DESCRIPTOGRAFA
    numeros = [] #CONVERTE LETRA EM NUMERO
    for index in range(len(desc_prod)):
        for indec in range(len(alfanumerico)):
            if desc_prod[index] == alfanumerico[indec]:
                numeros.append(indec)
    #
    parNumeros = [] #SEPARA OS NUMEROS EM PARES
    for i in range(0, len(numeros), 2):
        parNumeros.append(numeros[i:i+2])
    #
    multi = [] #MULTIPLICA OS NUMEROS PELA CHAVE
    for par in parNumeros:
        soma = 0
        soma = [(((chave[0][0] * par[0]) + (chave[0][1] * par[1])) % 26), 
                (((chave[1][0] * par[0]) + (chave[1][1] * par[1])) % 26)]
        multi.append(soma)
    #
    desc_cripto = '' #CONVERTE NUMERO EM LETRA
    for index in multi:
        for numero in index:
            for indec in range(len(alfanumerico)):
                if [numero] == [indec]:
                    desc_cripto += alfanumerico[indec]
    return desc_cripto
def verificacao_para_criptografia(desc_prod): #VERIFICA SE A DESCRICAO É IMPAR
    if (len(desc_prod) % 2 != 0):
            desc_prod += desc_prod[-1]
    return desc_prod

def calculo_print_tabela(cod_prod, nome_prod, desc_prod, CP, CF, CV, IV, ML): #CALCULA E IMPRIME A TABELA
    PV = CP/(1-((CF+CV+IV+ML)/100)) #CALCULAR O VALOR PARA VENDA DO PRODUTO
    #
    OCpor = CF+CV+IV          #OUTROS CUSTOS '%'
    CFnum = (PV*CF)/100       #CUSTO FIXO 'VALOR'
    CVnum = (PV*CV)/100       #COMISSAO 'VALOR'
    IVnum = (PV*IV)/100       #IMPOSTOS 'VALOR'
    OCnum = CFnum+CVnum+IVnum #OUTROS CUSTOS 'VALOR'
    RBnum = PV-CP             #RECEITA BRUTA 'VALOR'
    Rnum  = RBnum-OCnum       #RENTABILIDADE 'VALOR'
    CPpor = (CP*100)/PV       #CUSTO PRODUTO '%'
    RBpor = 100-CPpor         #RECEITA BRUTA '%'
    Rpor  = RBpor-OCpor       #RENTABILIDADE '%'
    #
    if Rpor > 20:
        ClassLucro = 'LUCRO ALTO'
    elif 10 <= Rpor <= 20:
        ClassLucro = 'LUCRO MÉDIO'
    elif 0 < Rpor < 10:
        ClassLucro = 'LUCRO BAIXO'
    elif Rpor == 0:
        ClassLucro = 'EQUILÍBRIO'
    elif Rpor < 0:
        ClassLucro = 'PREJUÍZO'
    #
    print(f'''                      
=========================================================
 CÓDIGO: {cod_prod}\t\t\t\t\t\t
 PRODUTO: {nome_prod}\t\t\tVALOR\t  %
 DESCRIÇÃO: {desc_prod}\t\t\t\t\t\t           
=========================================================
 A. Preço de Venda\t\t¦ R${PV:.2f}\t¦  100%\t
 B. Custo de Aquisição\t\t¦ R${CP:.2f}\t¦  {CPpor:.0f}% \t
 C. Receita Bruta(A-B)\t\t¦ R${RBnum:.2f}\t¦  {RBpor:.0f}% \t
 D. Custo Fixo/Administrativo\t¦ R${CFnum:.2f}\t¦  {CF:.0f}% \t                   
 E. Comissão de Vendas\t\t¦ R${CVnum:.2f}\t¦  {CV:.0f}% \t
 F. Impostos\t\t\t¦ R${IVnum:.2f}\t¦  {IV:.0f}% \t
 G. Outros Custos(D+E+F)\t¦ R${OCnum:.2f}\t¦  {OCpor:.0f}% \t
 H. Rentabilidade(C-G)\t\t¦ R${Rnum:.2f}\t¦  {Rpor:.0f}% \t
=========================================================
 CLASSIFICAÇÃO DE LUCRO:\t {ClassLucro}\t\t
=========================================================
        ''')

# [1] CADASTRAR PRODUTO
def cadastrar_produto():
    # ---------------------------- CADASTRO DOS PRODUTOS ----------------------------
        cod_prod = int(input('Código do Produto: '))       #CODIGO DO PRODUTO
        #
        cursor.execute(f"SELECT * FROM PRODUTOS WHERE COD_PROD = {cod_prod}")
        for row in cursor:
            print("CÓDIGO JA EXISTE")
        if (cursor.rowcount == 0):
            nome_prod = str(input('Nome Produto: '))           #NOME DO PRODUTO
            desc_prod = str(input('Descrição do Produto: ')).upper()   #DESCRIÇÃO DO PRODUTO

            CP = float(input('Custo do  Produto: '))              #CUSTO PAGO PELO PRODUTO PARA O FORNECEDOR
            ML = float(input('Margem de Lucro sobre a Venda: '))  #MARGEM DE LUCRO SOBRE A VENDA DO PRODUTO
            CF = float(input('Custo Fixo/Administrativo(%): '))   #CUSTO FIXO (ESPAÇO FÍSICO, DESPESAS, FUNCIONÁRIOS...)
            CV = float(input('Comissão de Vendas(%): '))          #COMISSÃO SOBRE A VENDA DO PRODUTO
            IV = float(input('Impostos(%): '))                    #IMPOSTOS SOBRE A VENDA DO PRODUTO
            #
            os.system('cls')
            calculo_print_tabela(cod_prod, nome_prod, desc_prod, CP, CF, CV, IV, ML)
            #
            desc_prod = verificacao_para_criptografia(desc_prod)
            desc_prod = hill_criptografia(desc_prod, chave)
            #
            cursor.execute(f"INSERT INTO produtos VALUES ({cod_prod}, '{nome_prod}', '{desc_prod}', {CP}, {CF},{CV}, {IV}, {ML})")
            connection.commit()
            #
            print("PRODUTO CADASTRADO COM SUCESSO!!!")

# [4] MOSTRAR ESTOQUE
def mostrar_estoque():
    cursor.execute("SELECT * FROM PRODUTOS")
    for row in cursor:
        #
        cod_prod = row[0]
        nome_prod = row[1]
        desc_prod = row[2]
        CP = row[3]
        CF = row[4]
        CV = row[5]
        IV = row[6]
        ML = row[7]
        #
        desc_prod = hill_criptografia(desc_prod, chave_inversa)
        calculo_print_tabela(cod_prod, nome_prod, desc_prod, CP, CF, CV, IV, ML)

# [2a] VERIFICAÇÃO DA ALTERAÇÃO
def verificacao_alterar(cod_alterar, alteracao, index):
    resp_alterar = str(input(f'CONFIRMAR A ALTERAÇÃO DO PRODUTO | {cod_alterar} <S/N>: ')).upper()
    if resp_alterar == "S":
        cursor.execute(f"UPDATE produtos SET {index} = '{alteracao}' WHERE cod_prod = {cod_alterar}")
        connection.commit()
        print(">>> PRODUTO ALTERADO COM SUCESSO!!!")
    else:
        print("PRODUTO NÃO ALTERADO")

# [2b].ALTERAR PRODUTO
def alterar_produto():
    try:
        cod_alterar = int(input('Digite o código do produto que deseja alterar: '))
        cursor.execute("SELECT * FROM PRODUTOS WHERE COD_PROD = :1", (cod_alterar,))
        produto = cursor.fetchone()

        if produto is None:
            print(">>> PRODUTO NÃO ENCONTRADO")
        else:
            print(">>> PRODUTO ENCONTRADO")
            menu_alterar = int(input('''                   
    =============================
    ¦ O QUE DESEJA ALTERAR:     ¦
    =============================
    ¦ [1].NOME                  ¦
    ¦ [2].DESCRICAO             ¦
    ¦ [3].CUSTO DO PRODUTO      ¦
    ¦ [4].MARGEM DE LUCRO       ¦
    ¦ [5].CUSTO FIXO            ¦
    ¦ [6].COMISSAO DE VENDAS    ¦
    ¦ [7].IMPOSTOS              ¦                                                     
    =============================
            OPÇÃO: '''))   
            
            if (menu_alterar == 1):
                index = "nome_prod"
                alteracao = str(input('NOVO Nome Produto: '))
                verificacao_alterar(cod_alterar, alteracao, index)
            elif (menu_alterar == 2):
                index = "desc_prod"
                alteracao = str(input('NOVA Descrição do Produto: ')).upper()
                alteracao = verificacao_para_criptografia(alteracao)
                alteracao = hill_criptografia(alteracao, chave)
                verificacao_alterar(cod_alterar, alteracao, index)       
            elif (menu_alterar == 3):
                index = "cp"
                alteracao = float(input('NOVO Custo do  Produto: '))
                verificacao_alterar(cod_alterar, alteracao, index)
            elif (menu_alterar == 4):
                index = "ml"
                alteracao = float(input('NOVA Margem de Lucro sobre a Venda: '))
                verificacao_alterar(cod_alterar, alteracao, index)            
            elif (menu_alterar == 5):
                index = "cf"
                alteracao = float(input('NOVO Custo Fixo/Administrativo(%): '))
                verificacao_alterar(cod_alterar, alteracao, index)
            elif (menu_alterar == 6):
                index = "cv"
                alteracao = float(input('NOVA Comissão de Vendas(%): '))
                verificacao_alterar(cod_alterar, alteracao, index)
            elif (menu_alterar == 7):
                index = "iv"
                alteracao = float(input('NOVO Impostos(%)?: '))
                verificacao_alterar(cod_alterar, alteracao, index)
    except oracledb.Error as error:
        print("Erro ao alterar produto:", error)


        
# [3].DELETAR PRODUTO
def apagar_produto():
    try:
        cod_apagar = int(input('Digite o codigo do produto que deseja apagar: '))

        cursor.execute("SELECT * FROM PRODUTOS WHERE COD_PROD = :1", (cod_apagar,))
        produto = cursor.fetchone()
        if produto is None:
            print(">>> PRODUTO NÃO ENCONTRADO")
        else:
            print(">>> PRODUTO ENCONTRADO")
            
            resp_apagar = str(input(f'CONFIRMAR A EXCLUSÃO DO PRODUTO | {cod_apagar} <S/N>: ')).upper()
            if resp_apagar == "S":
                cursor.execute(f'DELETE FROM produtos WHERE cod_prod = {cod_apagar}')
                connection.commit()
                print('''
                PRODUTO APAGADO COM SUCESSO!!!''')
            else:
                print("NENHUM PRODUTO APAGADO")
    except oracledb.Error as error:
        print("Erro ao apagar produto:", error)






# [0].CRIAR TABELA
def criar_tabela():
    cursor.execute ("""
            CREATE TABLE PRODUTOS (
            COD_PROD INTEGER NOT NULL PRIMARY KEY,
            NOME_PROD VARCHAR2(255) NOT NULL,
            DESC_PROD VARCHAR2(255) NOT NULL,
            CP NUMBER NOT NULL,
            CF NUMBER NOT NULL,
            CV NUMBER NOT NULL,
            IV NUMBER NOT NULL,
            ML NUMBER NOT NULL)""")
    connection.commit()

# [-1] DELETAR TABELA
def deletar_tabela():
    cursor.execute("DROP TABLE PRODUTOS")
    print("TABELA DELETADA!!!")