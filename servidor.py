import socket
import struct
import banco

banco = banco.Banco()

conector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conector.bind(('127.0.0.1',50000))
conector.listen(1)

while True:

    [sock_dados, _] = conector.accept()

    while True:

        opcode = sock_dados.recv(1)

        if not opcode:
            break
        opcode = opcode.decode("UTF-8")
        
        match(opcode):
            case 'c':
                tam = int.from_bytes(sock_dados.recv(1),'big')
                nome = sock_dados.recv(tam).decode("utf-8")
                tam = int.from_bytes(sock_dados.recv(1),'big')
                tipo = sock_dados.recv(tam).decode("utf-8")
                tam = int.from_bytes(sock_dados.recv(1),'big')
                genero = sock_dados.recv(tam).decode("utf-8")
                altura = struct.unpack(">d",sock_dados.recv(8))[0]
                peso = struct.unpack(">d",sock_dados.recv(8))[0]
                print(nome,tipo,genero,altura,peso)
                id = banco.adicionar(nome,tipo,genero,altura,peso)
                if id is None:
                    id = -1
                mensagem_retorno = id.to_bytes(2,'big',signed=True)
                sock_dados.send(mensagem_retorno)
            case 'b':
                id = int.from_bytes(sock_dados.recv(2),'big')
                retorno = banco.buscar(id)
                if retorno is None:
                    sock_dados.send(b'n')
                else:
                    nome = retorno[1]
                    tipo = retorno[2]
                    genero = retorno[3]
                    altura = retorno[4]
                    peso = retorno[5]
                    mensagem_retorno = len(nome.encode("utf-8")).to_bytes(1,'big') + nome.encode("utf-8")
                    mensagem_retorno += len(tipo.encode("utf-8")).to_bytes(1,'big') + tipo.encode("utf-8")
                    mensagem_retorno += len(genero.encode("utf-8")).to_bytes(1,'big') + genero.encode("utf-8")
                    mensagem_retorno += struct.pack('>d',altura)
                    mensagem_retorno += struct.pack('>d',peso)
                    sock_dados.send(mensagem_retorno)
            case 'a':
                id = int.from_bytes(sock_dados.recv(2),'big')
                tam = int.from_bytes(sock_dados.recv(1),'big')
                nome = sock_dados.recv(tam).decode("utf-8")
                tam = int.from_bytes(sock_dados.recv(1),'big')
                tipo = sock_dados.recv(tam).decode("utf-8")
                tam = int.from_bytes(sock_dados.recv(1),'big')
                genero = sock_dados.recv(tam).decode("utf-8")
                altura = struct.unpack(">d",sock_dados.recv(8))[0]
                peso = struct.unpack(">d",sock_dados.recv(8))[0]
                sucesso = banco.atualizar(id,nome,tipo,genero,altura,peso)
                if sucesso:
                    print(nome,tipo,genero,altura,peso)
                    sock_dados.send(b'y')
                else:
                    sock_dados.send(b'n')
            case 'd':
                id = int.from_bytes(sock_dados.recv(2),'big')
                sucesso = banco.remover(id)
                if sucesso:
                    sock_dados.send(b'y')
                else:
                    sock_dados.send(b'n')