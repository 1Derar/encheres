from app import db
from flask_login import UserMixin
from datetime import datetime

class Utilisateur(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True)
    mot_de_passe = db.Column(db.String(255))
    jetons = db.Column(db.Integer, default=5)
    role = db.Column(db.String(10), default='client')
    offres = db.relationship('Offre', backref='utilisateur', lazy=True)

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    encheres = db.relationship("Enchere", backref="produit", lazy=True)

class Enchere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'))
    date_debut = db.Column(db.DateTime, default=datetime.utcnow)
    date_fin = db.Column(db.DateTime)
    jetons_par_mise = db.Column(db.Integer)
    statut = db.Column(db.String(20), default='en_cours')

class Offre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    enchere_id = db.Column(db.Integer, db.ForeignKey('enchere.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    date_offre = db.Column(db.DateTime, default=datetime.utcnow)

    utilisateur = db.relationship('Utilisateur', backref='offres')
    enchere = db.relationship('Enchere', backref='offres')

    def __repr__(self):
        return f'<Offre {self.montant}€ pour l\'enchère {self.enchere.id}>'