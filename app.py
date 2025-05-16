from flask import Flask, render_template, request, flash, abort, redirect, url_for, jsonify
import sqlite3
import pandas
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_hotspot(id):
    conn = get_db_connection()
    hotspot = conn.execute('SELECT * FROM hotspots WHERE id = ?', (id,)).fetchone()
    conn.close()
    if hotspot is None:
        abort(404)
    return hotspot
def exists_in_db(name):
    conn = get_db_connection()
    result = conn.execute('SELECT exists(SELECT 1 FROM hotspots WHERE call_number = ?)', (name,)).fetchone()[0]
    conn.close()
    return result

def update_status(to_disable, to_enable):
    conn = get_db_connection()
    for disable in to_disable:
        conn.execute('INSERT INTO hotspots (call_number, is_disabled) VALUES (?, ?)', (disable, True))
        conn.commit()
    for enable in to_enable:
        conn.execute('UPDATE hotspots SET is_disabled = ?' 'WHERE call_number = ?', (False, enable['call_number']))
        conn.commit()
    conn.close()

def delete_enabled():
    conn = get_db_connection()
    conn.execute('DELETE FROM hotspots WHERE is_disabled = ?', (False, ))
    conn.commit()
    conn.close()
    
def get_actions(file):
    to_enable.clear()
    to_disable.clear()
    file.save(file.filename)
    data = pandas.read_excel(file)
    current_list = []

    # iterate rows
    for index, row in data.iterrows():
        # if its a hotspot name
        name = row['CallNumber']
        if type(name) == str and name[:7] == "HOTSPOT":
            # if it does not already exist as an entry and ignore CPL and MMC
            if (name[8:11] != "CPL" and name[8:11] != "MMC"):
                current_list.append(name[8:])

                # if not in database it will add to table and list of spots to disable
                # it is entered at enabled
                if not exists_in_db(name[8:]):
                    conn = get_db_connection()
                    # hotspot = conn.execute('INSERT INTO hotspots (call_number, is_disabled)', (name[8:], False))
                    to_disable.append(name[8:])
                    conn.close()
                    
    
    # checks if hotspot is no longer on the list -- to enable
    conn = get_db_connection()
    disabled_hotspots = conn.execute('SELECT * FROM hotspots WHERE is_disabled = ?', (True,)).fetchall()
    for hotspot in disabled_hotspots:
        print("was disabled: " + hotspot['call_number'])
        if hotspot['call_number'] not in current_list:
            to_enable.append(hotspot)
            
            # conn.execute('UPDATE hotspots SET is_disabled = ?' 'WHERE id = ?', (False, hotspot['id']))
    conn.close()
    
    return to_disable, to_enable

def search(query):
    conn = get_db_connection()
    search_results = conn.execute("SELECT * FROM hotspots WHERE call_number LIKE ?", ('%' + query + '%',)).fetchall()
    conn.close()
    return search_results

to_disable = []
to_enable = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        update_status(to_disable, to_enable)
    
    results = []

    if request.args.get('is_searching'):
        results = search(request.args.get('search_query'))
        return render_template('results.html', hotspots = results)
    else:
        conn = get_db_connection()
        results = conn.execute('SELECT * FROM hotspots').fetchall()
        conn.close()
    
    return render_template('index.html', hotspots = results)
    

@app.route('/upload', methods=['GET', "POST"])
def upload():
    if request.method == "POST":
        
        if request.files['file'].filename == '':
            flash("please upload a file", 'error')
        else:
            flash('Changes from "{}" read'.format(request.files['file'].filename), 'success')
            file = request.files['file']
            to_disable, to_enable = get_actions(file)
            return render_template('upload.html', to_enable = to_enable, to_disable = to_disable, submitted=True)
        
    return render_template('upload.html', to_enable = [], to_disable = [], submitted=False)

@app.route('/confirm_delete', methods=['GET', 'POST'])
def confirm_delete():
    if request.method == "POST":
        delete_enabled()
        flash('Deleted all enabled hotspots!', 'success')
    
    return redirect(url_for('index'))

@app.route('/<int:id>/toggle', methods=("POST", "GET"))
def toggle(id):
    hotspot = get_hotspot(id)
    new_val = 1 ^ hotspot['is_disabled']
    conn = get_db_connection()
    conn.execute('UPDATE hotspots SET is_disabled = ?' 'WHERE id = ?', (new_val, id))
    conn.commit()
    conn.close()
    flash('"{}" status changed'.format(hotspot['call_number']), "success")
    return redirect(url_for('index'))

@app.route('/<int:id>/delete', methods=("POST",))
def delete(id):
    hotspot = get_hotspot(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM hotspots WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" deleted'.format(hotspot['call_number']), 'success')
    return redirect(url_for('index'))

@app.route('/create', methods=("POST",))
def create():
    if request.method == "POST":
        call_number = request.form['name']
        is_disabled = 'disable' == request.form['disabled']
        conn = get_db_connection()
        conn.execute('INSERT INTO hotspots (call_number, is_disabled) VALUES (?, ?)', (call_number, is_disabled))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
@app.route('/<int:id>/edit', methods=("POST", "GET"))
def edit(id):
    hotspot = get_hotspot(id)
    is_disabled = hotspot['is_disabled']
    
    if request.method == "POST":
        is_disabled = 'disable' == request.form['disabled']
        call_number = request.form['name']
        conn = get_db_connection()
        conn.execute('UPDATE hotspots SET call_number = ?, is_disabled = ?' 'WHERE id = ?', (call_number, is_disabled,id))
        conn.commit()
        conn.close()
        flash('"{}" updated'.format(hotspot['call_number']), 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', hotspot=hotspot, is_disabled=is_disabled)

