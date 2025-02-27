from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Caminho para o arquivo JSON onde os produtos serão armazenados
PRODUCTS_FILE = 'produtos.json'

# Função para carregar os produtos do arquivo JSON
def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r') as f:
            return json.load(f)
    return {"products": []}  # Retorna um objeto com chave 'products' se o arquivo não existir

# Função para salvar os produtos no arquivo JSON
def save_products(products):
    with open(PRODUCTS_FILE, 'w') as f:
        json.dump(products, f, indent=4)

@app.route('/')
def index():
    # Carregar os produtos e exibi-los na página
    products_data = load_products()
    return render_template('index.html', products=products_data['products'])

@app.route('/admin')
def admin():
    # Carregar os produtos para exibição no painel administrativo
    products_data = load_products()
    return render_template('interface.html', products=products_data['products'])

@app.route('/add-product', methods=['POST'])
def add_product():
    # Garantir que o diretório para imagens exista
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    
    # Receber os dados do formulário, incluindo o arquivo
    name = request.form['name']
    price = float(request.form['price'])
    category = request.form['category']
    image = request.files['image']

    # Salvar a imagem no diretório adequado (se necessário)
    image_filename = image.filename
    image_path = os.path.join('static/images', image_filename)
    image.save(image_path)

    # Carregar os produtos existentes
    products_data = load_products()
    products = products_data['products']

    # Adicionar o novo produto
    new_product = {
        "name": name,
        "price": price,
        "category": category,
        "image": image_path  # Caminho para a imagem
    }
    products.append(new_product)

    # Salvar novamente os dados no arquivo
    products_data['products'] = products
    save_products(products_data)

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
