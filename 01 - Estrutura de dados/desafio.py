import textwrap


class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Conta:
    def __init__(self, agencia, numero, cliente):
        self.agencia = agencia
        self.numero = numero
        self.cliente = cliente
        self.saldo = 0
        self.extrato = ""

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Valor inválido! @@@")


class ContaCorrente(Conta):
    def __init__(self, agencia, numero, cliente, limite=500, limite_saques=3):
        super().__init__(agencia, numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if valor > self.saldo:
            print("\n@@@ Saldo insuficiente! @@@")

        elif valor > self.limite:
            print("\n@@@ Valor excede o limite! @@@")

        elif self.numero_saques >= self.limite_saques:
            print("\n@@@ Número máximo de saques excedido! @@@")

        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")

        else:
            print("\n@@@ Valor inválido! @@@")


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def criar_usuario(clientes):
    cpf = input("Informe o CPF: ")

    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento: ")
    endereco = input("Endereço: ")

    cliente = Cliente(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def filtrar_cliente(cpf, clientes):
    return next((c for c in clientes if c.cpf == cpf), None)


def criar_conta(agencia, numero_conta, clientes, contas):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = ContaCorrente(agencia, numero_conta, cliente)
    cliente.adicionar_conta(conta)
    contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        linha = f"""
        Agência:\t{conta.agencia}
        Conta:\t\t{conta.numero}
        Titular:\t{conta.cliente.nome}
        """
        print("=" * 40)
        print(textwrap.dedent(linha))


def selecionar_conta(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    return cliente.contas[0]  # simplificado (1 conta)


def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    print("Não houve movimentações." if not conta.extrato else conta.extrato)
    print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("=========================================")


def main():
    AGENCIA = "0001"

    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "nu":
            criar_usuario(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(AGENCIA, numero_conta, clientes, contas)

        elif opcao in ["d", "s", "e"]:
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            conta = selecionar_conta(cliente)

            if not conta:
                continue

            if opcao == "d":
                valor = float(input("Valor do depósito: "))
                conta.depositar(valor)

            elif opcao == "s":
                valor = float(input("Valor do saque: "))
                conta.sacar(valor)

            elif opcao == "e":
                exibir_extrato(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida! @@@")


main()
