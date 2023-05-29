import typing as t
from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from jinja2.sandbox import SandboxedEnvironment
from . import models, db
import json, fileinput

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Please enter a note!', category='error')
        else:
            new_note = models.Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Your note has been created', category='success')
    return render_template("home.html", user=current_user)

# this function is dedicated for the server-side template injection demo.
@views.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    if request.method == 'POST':
        email = request.form.get('edit-email')
        fname = request.form.get('edit-fn')
        lname = request.form.get('edit-ln')
        if len(email) > 0 or len(fname) > 0 or len(lname) > 0:
            return render_template('info.html', user=current_user, email=email, fname=fname, lname=lname)
    return render_template('info.html', user=current_user)

# override the is_safe_attribute function from jinja sandbox 
class MyEnvironment(SandboxedEnvironment):
    def is_safe_attribute(self, obj, attr: str) -> bool:
        if attr in ['os', 'subprocess', 'eval', 'exec']:
            return False
        return super().is_safe_attribute(obj, attr)
    
    def is_safe_callable(self, obj) -> bool:
        if obj in ['config']:
            return False
        return super().is_safe_callable(obj)
    
# this function is dedicated for the server-side template injection demo.
@views.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    if request.method == 'POST':
        email = request.form.get('edit-email')
        fname = request.form.get('edit-fn')
        lname = request.form.get('edit-ln')
        env = SandboxedEnvironment()
        if len(email) > 0 or len(fname) > 0 or len(lname) > 0:
            fn = "website/templates/test.html" # absolute path if necessary
            file = open(fn, "r")
            line = file.readlines()
            try:
                env.from_string(email + fname + lname).render()
                for str in line: 
                    tem = str
                    if 'Email: ' in str:
                        tem = "\t\t\t\tEmail: " + ' ' + email + '\n'
                    if 'First Name: ' in str:
                        tem = "\t\t\t\tFirst Name: " + ' ' + fname + '\n'
                    if 'Last Name: ' in str:
                        tem = "\t\t\t\tLast Name: " + ' ' + lname + '\n'
                    line[line.index(str)] = tem
                file.close()
                file = open(fn, "w")
                file.writelines(line)
                file.close()
            except:
                return render_template('test.html', user=current_user)
    return render_template('test.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = models.Note.query.get_or_404(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})