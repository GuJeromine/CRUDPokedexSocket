# Pokédex CRUD com Sockets TCP

Este projeto implementa um sistema CRUD (Create, Read, Update, Delete) completo para uma Pokédex, utilizando uma arquitetura cliente-servidor de baixo nível baseada no módulo `socket` do Python.

O sistema é dividido em três componentes principais, demonstrando uma arquitetura de três camadas:
1.  **`banco.py` (Camada de Dados / Model):** Gerencia a persistência dos dados com o SQLite.
2.  **`servidor.py` (Camada de Lógica / Controller):** Ouve conexões TCP, processa requisições e coordena o banco de dados.
3.  **`cliente.py` (Camada de Apresentação / View):** Fornece uma interface de linha de comando (CLI) para o usuário interagir com o servidor.

## Arquitetura do Projeto

### `banco.py` (Camada de Dados)
* **Tecnologia:** `sqlite3`
* **Responsabilidade:** Abstrai todo o acesso ao banco de dados.
* **Banco:** Conecta-se ao arquivo `pokedex.db`.
* **Tabela:** Cria e gerencia a tabela `teste` (com colunas `id`, `nome`, `tipo`, `genero`, `altura`, `peso`).
* **Métodos:** Fornece as quatro operações CRUD: `adicionar`, `buscar` (por ID), `atualizar` e `remover`.

### `servidor.py` (Servidor TCP)
* **Tecnologia:** `socket` (TCP Stream)
* **Endereço:** Ouve na porta `127.0.0.1:50000`.
* **Responsabilidade:** Aguarda conexões de clientes. Ele implementa a lógica de um **protocolo binário customizado** para receber comandos (opcodes) e dados, processá-los usando o `banco.py` e enviar uma resposta de volta ao cliente.
* **Protocolo:** Lida com o *unpacking* de dados usando `struct.unpack` (para números `double`) e leitura de strings com prefixo de tamanho.

### `cliente.py` (Cliente CLI)
* **Tecnologia:** `socket` (TCP Stream)
* **Responsabilidade:** Fornece a interface do usuário.
* **Menu:** Apresenta um menu de 5 opções (Inserir, Buscar, Atualizar, Remover, Sair).
* **Validação:** Valida a entrada do usuário (ex: garante que `nome` não seja um número e que `altura` seja um número).
* **Protocolo:** Implementa o lado do cliente do **protocolo binário customizado**. Ele monta os *payloads* de dados prefixando-os com um "opcode" (ex: `'c'` para criar) e empacota os dados usando `struct.pack` e prefixos de tamanho para strings.

## Protocolo Binário Customizado

A comunicação entre o cliente e o servidor usa um protocolo simples baseado em "opcodes" (códigos de operação) de 1 byte:

| Opcode | Operação | Direção | Payload de Dados |
| :--- | :--- | :--- | :--- |
| **`'c'`** | **C**riar | Cliente -> Servidor | `[opcode] + [tam_nome] + [nome] + [tam_tipo] + [tipo] + ... + [struct(altura)] + [struct(peso)]` |
| **`'b'`** | **B**uscar | Cliente -> Servidor | `[opcode] + [id]` |
| **`'a'`** | **A**tualizar | Cliente -> Servidor | `[opcode] + [id] + [tam_nome] + [nome] + ... + [struct(peso)]` |
| **`'d'`** | **D**eletar | Cliente -> Servidor | `[opcode] + [id]` |

* **Strings:** São enviadas com um prefixo de 1 byte indicando seu tamanho (`len(str).to_bytes(1,'big')`).
* **Números (Doubles):** São empacotados em 8 bytes usando `struct.pack('>d', ...)`.
* **IDs:** São enviados como inteiros de 2 bytes.
* **Respostas:** O servidor responde com códigos simples (ex: `b'y'` para sucesso, `b'n'` para falha/não encontrado) ou com os dados solicitados (no caso da busca).

## Como Executar

Para rodar este projeto, você precisa de dois terminais:

1.  **Terminal 1: Iniciar o Servidor**
    O servidor deve ser iniciado primeiro para que possa ouvir as conexões.
    ```bash
    python servidor.py
    ```

2.  **Terminal 2: Iniciar o Cliente**
    Após o servidor estar em execução, inicie o cliente.
    ```bash
    python cliente.py
    ```
    *O menu de opções aparecerá, e você poderá interagir com a Pokédex.*
