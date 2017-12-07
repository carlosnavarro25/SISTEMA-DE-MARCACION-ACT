from flask import Flask, request, flash
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SistemaMarcacion.sqlite3'
app.config['SECRET_KEY'] = 'uippc3'

db = SQLAlchemy(app)

def _get_date():
    return datetime.now()

"""
   Clase en donde se crea la tablas de la base de datos y se declaran las columnas
    """

class Super(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    codigo= db.Column(db.Integer)
    entrada = db.Column(db.String)
    salida = db.Column(db.String)



    def __init__(self, nombre, codigo, entrada): #<< agregar date.time
        self.nombre = nombre
        self.codigo = codigo
        self.entrada = entrada
db.create_all()


"""Esta es la Ruta Principal donde se muestran las columnas con sus resultados, se muestra atraves del archivo mostrar_todo.html"""
@app.route('/')
def supers_list():
    supers = Super.query.all()
    return render_template('mostrar_todo.html', supers=supers)




"""     Esta ruta agrega los resultados en la db, si no se agregan datos tira error en el flash
    """
@app.route('/super', methods=['POST'])
def add_super():
    nombre = request.form.get('nombre')
    codigo = request.form.get('codigo')
    entrada = request.form.get('entrada')

    if not request.form['nombre'] or not request.form['codigo']:
        flash('Debes llenar todos los campos')
        return redirect('/')
    super = Super(nombre,codigo,entrada)
    db.session.add(super)
    db.session.commit()
    flash('Registro guardado con exito!')
    return redirect('/')


@app.route('/delete/<int:super_id>')
def delete_super(super_id):
    super = Super.query.get(super_id)
    if not super:

        return redirect('/')

    db.session.delete(super)
    db.session.commit()
    time = datetime.now().time()
    print("Hora de SALIDA::")
    print(time)
    flash('Se borro con exito!')
    return redirect('/')


app.static_folder = 'static'

if __name__ == '__main__':
    db.create_all()
    app.run()
