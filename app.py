from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__, template_folder = 'templates')

lista_produtos = []
ids = []

@app.route('/')
def index():
    return render_template('pages/index.html', titulo_pagina='Pagina Inicial')

@app.route('/cadastrar_produto')
def cadastrar_produto():
    msg = request.args.get("msg")
    return render_template('pages/cadastrar_produto.html', titulo_pagina='Cadastro de Produto', msg=msg)

@app.route('/produtos')
def produtos():
    msg = request.args.get("msg")
    return render_template('pages/produtos.html', titulo_pagina='Pagina Inicial', lista_produtos=lista_produtos, msg=msg)

@app.route('/register', methods = ['POST'])
def register():
    id = len(ids)
    ids.append(id)

    name = request.form['name']
    desc = request.form['desc']
    price = request.form['price']

    lista_produtos.append([id,name,desc,price])

    return redirect(url_for('cadastrar_produto', msg=f'Produto {name} Cadastrado'))

@app.route('/ver_produto/<int:id>')
def ver_produto(id):
    produto = searchProduto(id)
    
    return render_template('pages/ver_produto.html', titulo_pagina='Informações do Produto', produto=produto)

@app.route('/edit_produto/<int:id>')
def edit_produto(id):
    produto = searchProduto(id)
    return render_template('pages/edit_produto.html', titulo_pagina=f'Editar produto {produto[0][1]}', id=id, produto=produto)

@app.route('/edit/<int:id>')
def edit(id):
    name = request.form.get('name')
    desc = request.form.get('desc')
    price = request.form.get('price')

    for item in lista_produtos:
        if item[0] == id:
            lista_produtos[item[0]][1] = name
            lista_produtos[item[0]][2] = desc
            lista_produtos[item[0]][3] = price
    return redirect(url_for('produtos'))

@app.route('/delete_produto/<int:id>', methods=['DELETE', 'GET'])
def delete_produto(id):
    for indice, linha in enumerate(lista_produtos):
        if linha[0] == id:
            indice_encontrado = indice
            break
    del lista_produtos[indice]
    
    return redirect(url_for('produtos', msg='Produto deletado !'))

def searchProduto(id):
    id_produto = id
    id_produto = int(id_produto)
    produto = [item for item in lista_produtos if item[0] == id_produto]
    return produto

if __name__ == '__main__':
    app.run(debug= True)