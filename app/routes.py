import os
import json
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import User, Category, Product, CartItem, Order, OrderItem, Review
from app.forms import (RegistrationForm, LoginForm, ProfileForm, OrderForm,
                       ReviewForm, ProductForm)


def get_cart_count():
    if current_user.is_authenticated:
        return CartItem.query.filter_by(user_id=current_user.id).count()
    return 0


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.context_processor
def inject_globals():
    categories = Category.query.filter(Category.parent_id.is_(None)).all()
    return {
        'cart_count': get_cart_count(),
        'categories': categories,
        'now': datetime.now()
    }


# ==================== ГЛАВНАЯ СТРАНИЦА ====================

@app.route('/')
def index():
    featured_products = Product.query.filter_by(is_featured=True, is_active=True).limit(8).all()
    new_products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(4).all()
    reviews = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).limit(6).all()
    return render_template('index.html',
                         featured_products=featured_products,
                         new_products=new_products,
                         reviews=reviews)


# ==================== КАТАЛОГ ====================

@app.route('/catalog/')
@app.route('/catalog/<slug>/')
def catalog(slug=None):
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'name')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    query = Product.query.filter_by(is_active=True)

    category = None
    if slug:
        category = Category.query.filter_by(slug=slug).first_or_404()
        # Include subcategories
        category_ids = [category.id]
        for child in category.children:
            category_ids.append(child.id)
        query = query.filter(Product.category_id.in_(category_ids))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'newest':
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.name.asc())

    products = query.paginate(page=page, per_page=12, error_out=False)
    return render_template('catalog.html', products=products, category=category, sort=sort)


@app.route('/product/<slug>/')
def product_detail(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    reviews = Review.query.filter_by(product_id=product.id, is_approved=True).order_by(Review.created_at.desc()).all()
    review_form = ReviewForm()
    return render_template('product_detail.html',
                         product=product,
                         related_products=related_products,
                         reviews=reviews,
                         review_form=review_form)


# ==================== КОРЗИНА ====================

@app.route('/cart/')
def cart():
    if not current_user.is_authenticated:
        flash('Для просмотра корзины необходимо войти в систему.', 'info')
        return redirect(url_for('login'))

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.total_price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/cart/add/<int:product_id>/', methods=['POST'])
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        flash('Для добавления в корзину необходимо войти.', 'info')
        return redirect(url_for('login'))

    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity', 1, type=int)

    if product.stock < quantity:
        flash('Недостаточно товара на складе.', 'danger')
        return redirect(request.referrer or url_for('product_detail', slug=product.slug))

    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    flash(f'{product.name} добавлен в корзину.', 'success')
    return redirect(request.referrer or url_for('catalog'))


@app.route('/cart/update/<int:item_id>/', methods=['POST'])
def update_cart(item_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        flash('Доступ запрещен.', 'danger')
        return redirect(url_for('cart'))

    quantity = request.form.get('quantity', 1, type=int)
    if quantity <= 0:
        db.session.delete(cart_item)
        flash('Товар удален из корзины.', 'info')
    else:
        if cart_item.product.stock < quantity:
            flash('Недостаточно товара на складе.', 'danger')
        else:
            cart_item.quantity = quantity
            flash('Количество обновлено.', 'success')

    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/cart/remove/<int:item_id>/')
def remove_from_cart(item_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        flash('Доступ запрещен.', 'danger')
        return redirect(url_for('cart'))

    db.session.delete(cart_item)
    db.session.commit()
    flash('Товар удален из корзины.', 'info')
    return redirect(url_for('cart'))


# ==================== ОФОРМЛЕНИЕ ЗАКАЗА ====================

@app.route('/checkout/', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Ваша корзина пуста.', 'info')
        return redirect(url_for('catalog'))

    total = sum(item.total_price for item in cart_items)
    form = OrderForm()

    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=form.shipping_address.data,
            shipping_city=form.shipping_city.data,
            shipping_phone=form.shipping_phone.data,
            comment=form.comment.data
        )
        db.session.add(order)
        db.session.flush()  # Get order ID

        for item in cart_items:
            if item.product.stock < item.quantity:
                flash(f'Недостаточно товара: {item.product.name}', 'danger')
                db.session.rollback()
                return redirect(url_for('cart'))

            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            db.session.add(order_item)

        # Clear cart
        for item in cart_items:
            db.session.delete(item)

        db.session.commit()
        flash(f'Заказ №{order.id} успешно оформлен!', 'success')
        return redirect(url_for('order_success', order_id=order.id))

    # Pre-fill form
    if request.method == 'GET':
        form.shipping_phone.data = current_user.phone
        form.shipping_address.data = current_user.address

    return render_template('checkout.html', cart_items=cart_items, total=total, form=form)


@app.route('/order/success/<int:order_id>/')
@login_required
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Доступ запрещен.', 'danger')
        return redirect(url_for('index'))
    return render_template('order_success.html', order=order)


@app.route('/orders/')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)


@app.route('/order/<int:order_id>/')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Доступ запрещен.', 'danger')
        return redirect(url_for('index'))
    return render_template('order_detail.html', order=order)


# ==================== ОТЗЫВЫ ====================

@app.route('/product/<int:product_id>/review/', methods=['POST'])
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            product_id=product_id,
            user_name=form.user_name.data,
            rating=int(form.rating.data),
            text=form.text.data
        )
        db.session.add(review)
        db.session.commit()
        flash('Отзыв отправлен на модерацию.', 'success')
    return redirect(url_for('product_detail', slug=product.slug))


# ==================== АВТОРИЗАЦИЯ ====================

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Добро пожаловать, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Неверное имя пользователя или пароль.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))


@app.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Профиль обновлен.', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.address.data = current_user.address
    return render_template('profile.html', form=form)


# ==================== ПОИСК ====================

@app.route('/search/')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)

    if query:
        products = Product.query.filter(
            Product.is_active == True,
            (Product.name.ilike(f'%{query}%') |
             Product.description.ilike(f'%{query}%'))
        ).paginate(page=page, per_page=12, error_out=False)
    else:
        products = None

    return render_template('search.html', query=query, products=products)


# ==================== СТАТИЧЕСКИЕ СТРАНИЦЫ ====================

@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')


@app.route('/delivery/')
def delivery():
    return render_template('delivery.html')


# ==================== API ====================

@app.route('/api/cart/count/')
def api_cart_count():
    return jsonify({'count': get_cart_count()})


@app.route('/api/products/featured/')
def api_featured_products():
    products = Product.query.filter_by(is_featured=True, is_active=True).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'image': p.image
    } for p in products])


# ==================== ОБРАБОТКА ОШИБОК ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
