from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime


app = Flask(__name__)
app.secret_key="EstaEsLaClaveSecreta"  
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='to_do_list'
mysql.init_app(app)


@app.route('/')
def index():
    sql = "SELECT * FROM `to_do_list`.`task`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    task=cursor.fetchall()
    conn.commit()
    return render_template('todolist/index.html', tasks=task)


@app.route('/task/<int:id>')
def task(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `to_do_list`.`task` WHERE id=%s", (id))
    task=cursor.fetchall()
    fecha = task[0][4]
    # Tratar de llevar la fecha legible al template
    fecha_legible = fecha.strftime('%d/%m/%Y %H:%M')
    #
    conn.commit()
    return render_template('todolist/task.html', tasks=task)


@app.route('/create')
def create():
    return render_template('todolist/create.html')


@app.route('/store', methods=["POST"])
def storage():
    _titulo = request.form['titulo']
    _descripcion = request.form['descripcion']
    _prioridad = request.form['prioridad']
    _fecha = datetime.now()

    if _titulo == '' or _prioridad == '':
        flash('Datos incompletos. Debes llenar todos los campos del formulario')
        return redirect(url_for('create'))

    sql = "INSERT INTO `to_do_list`.`task` (`id`, `title`, `description`, `type`, `datetime`) VALUES (NULL, %s, %s, %s, %s);"
    datos=(_titulo, _descripcion, _prioridad, _fecha)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    flash('Tarea agregada con éxito')
    return redirect('/')


@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `to_do_list`.`task` WHERE id=%s", (id))
    task=cursor.fetchall()
    conn.commit()
    return render_template('todolist/edit.html', tasks=task)


@app.route('/update', methods=['POST'])
def update():
    id=request.form['id']
    _titulo = request.form['titulo']
    _descripcion = request.form['descripcion']
    _prioridad = request.form['prioridad']

    sql = "UPDATE `to_do_list`.`task` SET `title`=%s, `description`=%s, `type`=%s WHERE id=%s;"
    datos = (_titulo, _descripcion, _prioridad, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `to_do_list`.`task` WHERE id=%s", (id))
    conn.commit()
    flash('Tarea eliminada con éxito')
    return redirect('/')


if __name__=='__main__':
    app.run(debug=True)