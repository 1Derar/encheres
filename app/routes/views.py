from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Utilisateur, Produit, Enchere, Offre
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import abort
from app.models import Produit






views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        password = request.form['password']
        if Utilisateur.query.filter_by(email=email).first():
            flash('Email déjà utilisé.')
            return redirect(url_for('views.register'))
        user = Utilisateur(nom=nom, email=email, mot_de_passe=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Compte créé avec succès.')
        return redirect(url_for('views.login'))
    return render_template('register.html')

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Utilisateur.query.filter_by(email=email).first()
        if user and check_password_hash(user.mot_de_passe, password):
            login_user(user)
            return redirect(url_for('views.dashboard'))
        flash('Identifiants invalides.')
    return render_template('login.html')

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views.route('/encheres')
@login_required
def encheres():
    liste = Enchere.query.all()
    return render_template('encheres.html', encheres=liste)

@views.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@views.route('/contact')
def contact():
    return render_template('contact.html')
@views.route('/jetons', methods=['GET', 'POST'])
@login_required
def acheter_jetons():
    if request.method == 'POST':
        montant = int(request.form['montant'])
        current_user.jetons += montant
        db.session.commit()
        flash(f'{montant} jetons ajoutés à votre compte.')
        return redirect(url_for('views.dashboard'))
    return render_template('jetons.html')

@views.route('/paiement/<int:montant>', methods=['GET', 'POST'])
@login_required
def paiement(montant):
    if request.method == 'POST':
        current_user.jetons += montant
        db.session.commit()
        flash(f"{montant} jetons ajoutés à votre compte.")
        return redirect(url_for('views.dashboard'))
    return render_template('paiement.html', montant=montant)

def admin_required(f):
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@views.route('/admin/produits', methods=['GET', 'POST'])
@admin_required
def admin_produits():
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        image = request.form['image']
        produit = Produit(nom=nom, description=description, image_url=image)
        db.session.add(produit)
        db.session.commit()
        flash('Produit ajouté.')
        return redirect(url_for('views.admin_produits'))
    produits = Produit.query.all()
    return render_template('admin/produits.html', produits=produits)

@views.route('/encheres/<int:enchere_id>', methods=['GET', 'POST'])
@login_required
def detail_enchere(enchere_id):
    enchere = Enchere.query.get_or_404(enchere_id)
    if request.method == 'POST':
        montant = float(request.form['montant'])
        if current_user.jetons < enchere.jetons_par_mise:
            flash("Pas assez de jetons.")
            return redirect(url_for('views.detail_enchere', enchere_id=enchere.id))
        offre = Offre(utilisateur_id=current_user.id, enchere_id=enchere.id, montant=montant)
        current_user.jetons -= enchere.jetons_par_mise
        db.session.add(offre)
        db.session.commit()
        flash("Offre placée.")
    offres = Offre.query.filter_by(enchere_id=enchere.id).order_by(Offre.montant.asc()).all()
    return render_template('detail_enchere.html', enchere=enchere, offres=offres)


print("✅ Fichier views.py chargé jusqu'au bout.")
