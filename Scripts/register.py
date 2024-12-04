from flask import Blueprint, render_template, request, redirect, url_for

# Crear un blueprint para registro
register_bp = Blueprint('register', __name__)

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password:
            return redirect(url_for('login.login'))
        else:
            return "Error al registrar usuario. Intenta nuevamente."
        
    return render_template('register.html')