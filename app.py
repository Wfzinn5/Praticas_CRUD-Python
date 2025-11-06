from flask import Flask, render_template, request, redirect, url_for 
# url_for = parâmetro
# request = requisição
# render_template = voltar a página ?

import mysql.connector
# Criação da aplicação Flask
app = Flask(__name__)
# Configuração da conexão com o banco de dados MySQL
db = mysql.connector.connect(
 host="",
 user="",
 password="",
 database=""
)
# Criar cursor para executar queries
cursor = db.cursor(dictionary=True)

# 1. Rota Inicial
@app.route('/')
def index():
 return render_template('index.html')

# 2. Rota para Fórmulário de Criação do Livro
@app.route('/criar')
def pagina_criar():
 return render_template('criar.html')


# 3. Rota para Criar Livro no Banco de Dados
@app.route('/criar/novo', methods=['POST'])
def criar_livro():
 titulo = request.form['titulo']
 ano_publicacao = request.form['ano_publicacao']
 editora = request.form['editora']
 isbn = request.form['isbn']

 query = "INSERT INTO livro (titulo, ano_publicacao, editora, isbn) VALUES (%s, %s, %s, %s)"
 values = (titulo, ano_publicacao, editora, isbn)

 cursor.execute(query, values)
 db.commit()

 return redirect('/')


#  4. Rota para Listar Livros
@app.route('/listar')
def listar():
 cursor.execute("SELECT * FROM livro")
 livros = cursor.fetchall()
 return render_template('listar.html', livros=livros)

# 4.5. Rota para Página de Edição
@app.route('/editar/<int:id>')
def pagina_editar(id):
 cursor.execute("SELECT * FROM livro WHERE id = %s", (id,))
 livro = cursor.fetchone()
 return render_template('editar.html', livro=livro)

# 4.6. Rota para Editar Livro
@app.route('/editar/salvar/<int:id>', methods=['POST'])
def editar_livro(id):
 titulo = request.form['titulo']
 ano_publicacao = request.form['ano_publicacao']
 editora = request.form['editora']
 isbn = request.form['isbn']

 query = "UPDATE livro SET titulo = %s, ano_publicacao = %s, editora = %s, isbn = %s WHERE id = %s"
 values = (titulo, ano_publicacao, editora, isbn, id)

 cursor.execute(query, values)
 db.commit()

 return redirect(url_for('listar'))

# 4.7. Rota para Deletar Livro
@app.route('/deletar/<int:id>')
def deletar(id):
 cursor.execute("DELETE FROM livro WHERE id = %s", (id,))
 db.commit()
 return redirect(url_for('listar'))


# Inicialização do servidor
if __name__ == '__main__':
 app.run(debug=True)