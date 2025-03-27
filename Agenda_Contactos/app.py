from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.String, nullable=False, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


with app.app_context():
    db.create_all()


@app.route('/')
def lista_agenda():
    contactos = Contacto.query.all()
    return render_template('index.html', contactos=contactos)


@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_contacto(id):
    contacto = Contacto.query.get_or_404(id)
    db.session.delete(contacto)
    db.session.commit()
    return redirect(url_for('lista_agenda'))

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_contacto():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        telefono = request.form['telefono']

        nuevo_contacto = Contacto(name=name, email=email, telefono=telefono)
        db.session.add(nuevo_contacto)
        db.session.commit()

        return redirect(url_for('lista_agenda'))

    return render_template('agregar.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_contacto(id):
    contacto = Contacto.query.get_or_404(id)

    if request.method == 'POST':
        contacto.name = request.form['name']
        contacto.email = request.form['email']
        contacto.telefono = request.form['telefono']

        db.session.commit()
        return redirect(url_for('lista_agenda'))

    return render_template('editar.html', contacto=contacto)


if __name__ == '__main__':
    app.run(debug=True)
