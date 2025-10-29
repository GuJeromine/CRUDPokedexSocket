import sqlite3

class Banco:

    def __init__(self):
        self.conexao = sqlite3.connect("pokedex.db")
        cursor = self.conexao.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS teste(id INTEGER PRIMARY KEY, nome, tipo, genero, altura, peso)")
        self.conexao.commit()
        cursor.close()

    def adicionar(self, nome, tipo, genero, altura, peso):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO teste(nome, tipo, genero, altura, peso) VALUES(?,?,?,?,?)', (nome,tipo,genero,altura,peso))
        if(cursor.rowcount > 0):
            id = cursor.lastrowid
        else:
            id = None
        self.conexao.commit()
        cursor.close()
        return id
    
    # retorna uma tupla contendo todos os campos, na mesma ordem de criação do banco
    def buscar(self, id):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM teste WHERE id = ?', (id,))
        retorno = cursor.fetchone()
        cursor.close()
        return retorno

    def atualizar(self, id, nome, tipo, genero, altura, peso):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT id FROM teste WHERE id = ?', (id,))
        if cursor.fetchone() is None:
            cursor.close()
            return False
        cursor.execute('UPDATE teste SET nome = ?, tipo = ?, genero = ?, altura = ?, peso = ? WHERE id = ?', (nome,tipo,genero,altura,peso,id))
        self.conexao.commit()
        cursor.close()
        return True
    
    def remover(self, id):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT id FROM teste WHERE id = ?', (id,))
        if cursor.fetchone() is None:
            cursor.close()
            return False
        cursor.execute('DELETE FROM teste WHERE id = ?', (id,))
        self.conexao.commit()
        cursor.close()
        return True