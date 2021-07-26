from app import app,db, Users
with app.app_context():
    db.create_all()
    admin = Users(username="admin",email='admin@admin.com', password='1' ,admin=True)
    db.session.add(admin)
    db.session.commit()