#!/usr/bin/env python3
import subprocess
import os


def getListaRAs(arquivo):
    with open(arquivo) as f:
        return list(filter(None, (f.read().splitlines())))


def formatarRA(aluno):
    if len(aluno) > 3:
        aluno = "".join(c for c in aluno if c.isnumeric())
        return aluno[:-1] + "-" + aluno[-1]


def getEmailAluno(aluno, sufixo):
    return "".join(["ra-", aluno, sufixo])


def listarAlias(email, aluno):
    retorno = subprocess.Popen(["gam", "info", "user", email], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    retorno = retorno.decode("utf-8")
    if "ERROR" in retorno or "Email Aliases" not in retorno:
        print("\033[091mRegistro NÃO possui alias: {0}\033[0m".format(aluno))
        if "userNotFound" in retorno:
            print("\033[091mUsuário não encontrado!\033[0m")
        return False
    retorno = retorno.split("\r")
    listaAlias = [i for i in retorno if "@" in i and "address" in i]
    return [i.replace("\n address: ", "") for i in listaAlias]


def atualizarEmail(automatico, email, aluno, listaAlias=False):
    if listaAlias:
        if len(listaAlias) == 1:
            subprocess.Popen(["gam", "update", "user", email, "email", listaAlias[0]]).communicate()
        else:
            if automatico:
                # atualiza com o 1 email alias disponivel
                subprocess.Popen(["gam", "update", "user", email, "email", listaAlias[0]]).communicate()
            else:
                while True:
                    print("\n\033[093mInforme o alias que deseja utilizar para o registro: {}\033[0m".format(aluno))
                    for a, b in enumerate(listaAlias):
                        print("{0}) {1}".format(a, b))
                    indice = str(input("novo email> "))
                    if indice in [str(i) for i, j in enumerate(listaAlias)]:
                        break
                    else:
                        print("\033[093mValor inválido.\033[0m")
                subprocess.Popen(["gam", "update", "user", email, "email", listaAlias[int(indice)]]).communicate()
        print("\033[092mRegistro atualizado: {0}\033[0m".format(aluno))


def selecionarDominio():
    while True:
        tipo = str(input("Selecione o domínio dos emails[dev/prod]:\n    1) @alunos.sandbox.unicesumar.edu.br\n    2) @alunos.unicesumar.edu.br \n> "))
        if tipo == "1":
            sufixo = "@alunos.sandbox.unicesumar.edu.br"
            break
        elif tipo == "2":
            sufixo = "@alunos.unicesumar.edu.br"
            break
        else:
            os.system("cls || clear")
            print("\033[093mValor inválido.\033[0m")
    return sufixo
            
def opcaoAtualizarEmail(arquivo):
    sufixo = selecionarDominio()
    while True:
        tipo = str(input("Deseja selecionar o email manualmente caso exista mais de 1 alias para o mesmo usuário?[s/n]\n> ").lower())
        if tipo == "s":
            automatico = False
            break
        elif tipo == "n":
            automatico = True
            break
        else:
            os.system("cls || clear")
            print("\033[093mValor inválido.\033[0m")
    listaRA = getListaRAs(arquivo)
    print("\nExecutando...\n")
    for aluno in listaRA:
        aluno = formatarRA(aluno)
        email = getEmailAluno(aluno, sufixo)
        listaAlias = listarAlias(email, aluno)
        atualizarEmail(automatico, email, aluno, listaAlias)
    print("\nAtualização concluída!")


def opcaoConsultarEmail(arquivo):
    listaRA = getListaRAs(arquivo)
    sufixo = selecionarDominio()
    os.system("cls || clear")
    print("\nLista Emails:\n")
    for aluno in listaRA:
        aluno = formatarRA(aluno)
        email = getEmailAluno(aluno, sufixo)
        print("\n\033[092mRegistro: {}\033[0m".format(aluno))
        retorno = subprocess.Popen(["gam", "info", "user", email], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        retorno = retorno.decode("utf-8")
        if retorno:
            emailPrincipal = [i for i in retorno.split("\r") if "@" in i and "User" in i][0]
            if "ERROR" in retorno or "Email Aliases" not in retorno:
                print("\033[091mNão possui alias!\033[0m")
                if "userNotFound" in retorno:
                    print("\033[091mUsuário não encontrado!\033[0m")
                continue
            listaAlias = [i for i in retorno.split("\r") if "@" in i and "address" in i]
            listaAlias = [i.replace("\n address: ", "") for i in listaAlias]
            print("{} (principal)".format(emailPrincipal.replace("User:", "").strip()))
            if listaAlias:
                for i in listaAlias:
                    print(i)
        else:
            print("\033[091mUsuário não encontrado!\033[0m")

def opcaoConsultarDados(arquivo):
    listaRA = getListaRAs(arquivo)
    sufixo = selecionarDominio()
    os.system("cls || clear")
    print("\nConsulta Alunos:\n")
    for aluno in listaRA:
        aluno = formatarRA(aluno)
        email = getEmailAluno(aluno, sufixo)
        print("\n\033[092mRegistro: {}\033[0m".format(aluno))
        subprocess.Popen(["gam", "info", "user", email]).communicate()


try:
    os.system("cls || clear")
    opcao = os.sys.argv[1]
    arquivo = os.sys.argv[2]
    if opcao == "atualizar-email":
        opcaoAtualizarEmail(arquivo)
    elif opcao == "consultar-email":
        opcaoConsultarEmail(arquivo)
    elif opcao == "lista-dados-usuario":
        opcaoConsultarDados(arquivo)
    else:
        raise Exception("")
except Exception as e:
    listaComandos = [("atualizar-email", "Substituir email principal pelo alias."),
        ("consultar-email", "Listar email principais e alias para cada aluno."),
        ("lista-dados-usuario", "Listar dados do aluno."),
    ]
    print("\033[091m\nParâmetros inválidos!\033[0m")
    print("\nSintaxe:\n   python {0} [opção] [arquivo]".format(os.path.basename(__file__)))
    print("\nOpções:")
    for i, j in listaComandos:
        print("    {}{:^8}{}".format(i, "-", j))
    print("\nexemplo:\n   python {0} update-email lista_RA_alunos.txt".format(os.path.basename(__file__)))
    print(e)