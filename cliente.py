import socket
import struct

sock_dados = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_dados.connect(('127.0.0.1',50000))

opcao = None

while opcao != '5':

    opcao = input('Digite 1 para inserir, 2 para buscar, 3 para atualizar, 4 para remover, 5 para sair\n')

    match opcao:
        case '1':
            while True:
                nome = input('digite o nome do pokémon: ')
                if nome and not nome.isdigit(): # Verifica se não está vazio e se não é um número
                    break # Se for válido, sai do loop
                print("Erro: Nome inválido. Por favor, digite um texto.")
            while True:
                tipo = input('digite o tipo do pokémon: ')
                if tipo and not tipo.isdigit(): # Verifica se não está vazio e se não é um número
                    break # Se for válido, sai do loop
                print("Erro: Tipo inválido. Por favor, digite um texto.")
            while True:
                genero = input('digite o gênero do pokémon: ')
                if genero and not genero.isdigit(): # Verifica se não está vazio e se não é um número
                    break # Se for válido, sai do loop
                print("Erro: Gênero inválido. Por favor, digite um texto.")
            while True:
                try:
                    altura = float(input('digite a altura do pokémon: '))
                    break # Se for válido, sai do loop
                except ValueError:
                    print("Erro: Altura inválida. Por favor, digite um número.")
            while True:
                try:
                    peso = float(input('digite o peso do pokémon: '))
                    break # Se for válido, sai do loop
                except ValueError:
                    print("Erro: Peso inválido. Por favor, digite um número.")
            mensagem = 'c'.encode("utf-8")
            mensagem += len(nome.encode("utf-8")).to_bytes(1,'big') + nome.encode("utf-8")
            mensagem += len(tipo.encode("utf-8")).to_bytes(1,'big') + tipo.encode("utf-8")
            mensagem += len(genero.encode("utf-8")).to_bytes(1,'big') + genero.encode("utf-8")
            mensagem += struct.pack('>d',altura)
            mensagem += struct.pack('>d',peso)
            sock_dados.send(mensagem)
            id = int.from_bytes(sock_dados.recv(2),'big',signed=True)
            if (id >= 0):
                print('Dado inserido com id', id)
            else:
                print('Dado não foi inserido')
        case '2':
            id = int(input('digite id do pokémon: '))
            mensagem = 'b'.encode("utf-8")
            mensagem += id.to_bytes(2,'big')
            sock_dados.send(mensagem)
            retorno = sock_dados.recv(1)
            if not retorno:
                print('Erro de comunicação')
            elif retorno == b'n':
                print('Dado não encontrado')
            else:
                tam = int.from_bytes(retorno,'big')
                nome = sock_dados.recv(tam).decode("utf-8")
                tam = int.from_bytes(sock_dados.recv(1),'big')
                tipo = sock_dados.recv(tam).decode("utf-8")
                tam = int.from_bytes(sock_dados.recv(1),'big')
                genero = sock_dados.recv(tam).decode("utf-8")
                altura = struct.unpack(">d",sock_dados.recv(8))[0]
                peso = struct.unpack(">d",sock_dados.recv(8))[0]
                print('Dado encontrado:', nome, tipo, genero, altura, peso)
        case '3':
            while True:
                try:
                    id = int(input('digite id do pokémon: '))
                    if id > 0:
                        break
                except ValueError:
                    print("Erro: ID inválido. Por favor, digite um número positivo.")
            while True:
                nome = input('digite o nome do pokémon: ')
                if nome and not nome.isdigit(): # Verifica se não está vazio e se não é um número
                    break # Se for válido, sai do loop
                print("Erro: Nome inválido. Por favor, digite um texto.")
            while True:
                tipo = input('digite o tipo do pokémon: ')
                if tipo and not tipo.isdigit(): # Verifica se não está vazio e se não é um número
                    break # Se for válido, sai do loop
                print("Erro: Tipo inválido. Por favor, digite um texto.")
            while True:
                genero = input('digite o gênero do pokémon: ')
                if genero and not genero.isdigit(): # Verifica se não está vazio e se não é um número
                    break # Se for válido, sai do loop
                print("Erro: Gênero inválido. Por favor, digite um texto.")
            while True:
                try:
                    altura = float(input('digite a altura do pokémon: '))
                    break # Se for válido, sai do loop
                except ValueError:
                    print("Erro: Altura inválida. Por favor, digite um número.")
            while True:
                try:
                    peso = float(input('digite o peso do pokémon: '))
                    break # Se for válido, sai do loop
                except ValueError:
                    print("Erro: Peso inválido. Por favor, digite um número.")
            mensagem = 'a'.encode("utf-8")
            mensagem += id.to_bytes(2,'big')
            mensagem += len(nome.encode("utf-8")).to_bytes(1,'big') + nome.encode("utf-8")
            mensagem += len(tipo.encode("utf-8")).to_bytes(1,'big') + tipo.encode("utf-8")
            mensagem += len(genero.encode("utf-8")).to_bytes(1,'big') + genero.encode("utf-8")
            mensagem += struct.pack('>d',altura)
            mensagem += struct.pack('>d',peso)
            sock_dados.send(mensagem)
            retorno = sock_dados.recv(1)
            if not retorno:
                print('Erro de comunicação')
            elif retorno == b'y':
                print('Dado atualizado com sucesso')
            else:
                print('Dado não foi atualizado ou não encontrado')
        case '4':
            id = int(input('digite id do pokémon: '))
            mensagem = 'd'.encode("utf-8")
            mensagem += id.to_bytes(2,'big')
            sock_dados.send(mensagem)
            retorno = sock_dados.recv(1)
            if not retorno:
                print('Erro de comunicação')
            elif retorno == b'y':
                print('Dado removido com sucesso')
            else:
                print('Dado não foi removido ou não encontrado')