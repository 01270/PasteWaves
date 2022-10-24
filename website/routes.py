from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from .models import Paste, User
from .enc import decode, encode
from . import db

routes =  Blueprint("rotes", __name__)


@routes.route("/")
def home():
    pastes = Paste.query.all()
    return render_template("home.html", p=pastes, titles=[(encode(str(i.id))) for i in pastes])


@routes.route("/new/", methods=['GET', 'POST'])
def new_paste():
    if request.method == 'POST':
        text = request.form.get("text")
        if '<' in text or '>' in text: return 'XSS Won\'t work here sir'
        else:
            user = User.query.filter_by(ip_address=request.remote_addr).first()
            if not user: 
                new_user = User(ip_address=request.remote_addr)
                db.session.add(new_user)
                db.session.commit()
            
            user_query = User.query.filter_by(ip_address=request.remote_addr).first()
            new_paste = Paste(text=text, author=user_query.id, views=0)
            db.session.add(new_paste)
            db.session.commit()
            return redirect(url_for('rotes.view_paste', paste_id=encode(str(new_paste.id))))
    return render_template("new_paste.html")


@routes.route("/delte-paste/<paste_id>/", methods=['POST'])
def delte_paste(paste_id):
    user_ip = request.form.get("user_ip")
    user = User.query.filter_by(ip_address=user_ip).first()
    for i in user.pastes:
        if str(i.id) == str(paste_id):
            Paste.query.filter_by(id=paste_id).delete()
            db.session.commit()
            return redirect(url_for('rotes.home'))
    return jsonify({"ok": False})


@routes.route("/raw/<paste_id>/")
def view_raw_paste(paste_id):
    paste_id = decode(paste_id)
    paste = Paste.query.filter_by(id=paste_id).first()
    if not paste: return 'Paste Not Found'
    else:
        paste.views = int(paste.views)+1
        db.session.commit()
        return f'<pre style="overflow-wrap: break-word; white-space: pre-wrap; position: relative;">{paste.text}</pre>'


@routes.route("/<paste_id>/")
def view_paste(paste_id):
    paste_id = decode(paste_id)
    paste = Paste.query.filter_by(id=paste_id).first()
    user = User.query.filter_by(ip_address=request.remote_addr).first()
    if not paste: return 'Paste Not Found'
    else:
        paste.views = int(paste.views)+1
        db.session.commit()
        return render_template("paste.html", p=paste, user=(user if user else None), title=encode(str(paste_id)), ip_address=request.remote_addr)

