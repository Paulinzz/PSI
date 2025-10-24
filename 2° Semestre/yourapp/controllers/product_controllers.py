from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.product import Product

product_bp = Blueprint('products', __name__, template_folder='../templates/products')

@product_bp.route('/products')
@login_required
def list_products():
    products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('list.html', products=products)

@product_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])

        if not name or not price:
            flash('Nome e preço são obrigatórios.', 'danger')
            return redirect(url_for('create.html'))
        
        try:
            price = float(price)
        except ValueError:
            flash('Preço inválido.', 'danger')
            return redirect(url_for('create.html'))

        product = Product(
            name=name,
            description=description,
            price=price,
            user_id=current_user.id
        )

        db.session.add(product)
        db.session.commit()

        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('products.list_products'))

    return render_template('create.html')

@product_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if product.user_id != current_user.id:
        flash('Você não tem permissão para editar este produto.', 'danger')
        return redirect(url_for('products.list_products'))

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))

        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('products.list_products'))

    return render_template('edit.html', product=product)

@product_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required 
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    if product.user_id != current_user.id:
        flash('Você não tem permissão para deletar este produto.', 'danger')
        return redirect(url_for('products.list_products'))

    db.session.delete(product)
    db.session.commit()
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('products.list_products'))


@product_bp.route('/api/products', methods=['GET'])
@login_required
def api_get_products():
    products = Product.query.filter_by(user_id=current_user.id).all()
    return jsonify([product.to_dict() for product in products])