from app import create_app, db
from app.models import Produit, Enchere
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    db.create_all()
    p1 = Produit(nom='PS5 Slim', description='Console Sony nouvelle génération', image_url='ps5.jpg')
    p2 = Produit(nom='Iphone 14', description='Smartphone Apple haut de gamme', image_url='iphone.jpg')
    db.session.add_all([p1, p2])
    db.session.commit()
    e1 = Enchere(produit_id=p1.id, date_fin=datetime.utcnow() + timedelta(days=1), jetons_par_mise=2)
    e2 = Enchere(produit_id=p2.id, date_fin=datetime.utcnow() + timedelta(days=2), jetons_par_mise=3)
    db.session.add_all([e1, e2])
    db.session.commit()
    print("Données initiales ajoutées.")