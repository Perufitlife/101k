from datetime import date
from flask import Blueprint, render_template, flash, redirect, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.forms import UpdateProfileForm
from app.models.user import Campaign, Order, Product

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    return render_template('index.html')

@dashboard.route('/dashboard')
@login_required
def show_dashboard():
    ventas_diarias = db.session.query(func.sum(Order.total)).filter(Order.date == date.today()).scalar() or 0
    ingresos_totales = db.session.query(func.sum(Order.total)).scalar() or 0
    pedidos_pendientes = Order.query.filter_by(status='pending').count()
    tasa_conversion = db.session.query(func.avg(Campaign.conversion_rate)).scalar() or 0
    productos_bajo_stock = Product.query.filter(Product.stock < 10).count()
    gastos_marketing = db.session.query(func.sum(Campaign.cost)).scalar() or 0

    stats = {
        "ventas_diarias": ventas_diarias,
        "ingresos_totales": ingresos_totales,
        "pedidos_pendientes": pedidos_pendientes,
        "tasa_conversion": tasa_conversion,
        "productos_bajo_stock": productos_bajo_stock,
        "gastos_marketing": gastos_marketing
    }
    return render_template('dashboard.html', stats=stats)

@dashboard.route('/inventario')
@login_required
def inventario():
    return render_template('inventario.html')

@dashboard.route('/pedidos')
@login_required
def pedidos():
    return render_template('pedidos.html')

@dashboard.route('/marketing')
@login_required
def marketing():
    return render_template('marketing.html')

@dashboard.route('/finanzas')
@login_required
def finanzas():
    return render_template('finanzas.html')

@dashboard.route('/configuraciones')
@login_required
def configuraciones():
    return render_template('configuraciones.html')

@dashboard.route('/configuraciones/facebook')
@login_required
def config_facebook():
    return render_template('config_facebook.html')

@dashboard.route('/configuraciones/tiktok')
@login_required
def config_tiktok():
    return render_template('config_tiktok.html')

@dashboard.route('/configuraciones/mapping')
@login_required
def config_mapping():
    return render_template('config_mapping.html')

@dashboard.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.current_password.data and not check_password_hash(current_user.password, form.current_password.data):
            flash('Current password is incorrect.', 'danger')
        else:
            current_user.username = form.username.data
            current_user.email = form.email.data
            if form.new_password.data:
                hashed_password = generate_password_hash(form.new_password.data, method='pbkdf2:sha256')
                current_user.password = hashed_password
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('dashboard.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('profile.html', form=form)

