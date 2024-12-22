import math
from flask import render_template, request, redirect, session, jsonify
import dao
from app import app, login
from flask_login import login_user, logout_user
from app.models import UserRole



@app.route("/")
def index():
    if 'cart' not in session:
        session['cart'] = {}

    kw = request.args.get('kw')
    type_ = request.args.get('type', '')

    show_patients = True if type_ == 'patients' else False

    patients = dao.load_patients(kw) if show_patients else []
    medicines = dao.load_medicines(kw) if not show_patients else []

    return render_template('index.html', patients=patients, medicines=medicines, show_patients=show_patients)


# DANG NHAP
@app.route("/login", methods=['get', 'post'])
def login_process():
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user)
            return redirect('/')

    return render_template('login.html')


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/login')


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)


# PHIEU KHAM BENH
@app.route('/save_form_data', methods=['POST'])
def save_form_data():
    data = request.json  # Nhận dữ liệu dưới dạng JSON từ frontend

    # Lưu thông tin vào session (hoặc bạn có thể lưu vào database)
    session['form_data'] = data

    return jsonify({"message": "Data saved successfully!"})


@app.route('/get_form_data', methods=['get'])
def get_form_data():
    # Lấy lại dữ liệu đã lưu trong session
    form_data = session.get('form_data', {})

    return jsonify(form_data)  # Trả lại dữ liệu dưới dạng JSON


@app.route('/api/carts', methods=['post'])
def add_to_cart():
    """
    {
        "1": {
            "id": "1",
            "name": "..",
            "unit": "Vi",
            "quantity": 2
        }, "2": {
            "id": "2",
            "name": "..",
            "unit": "Vien",
            "quantity": 1
        }
    }
    """
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))
    name = request.json.get('name')
    unit = request.json.get('unit')

    print(f"Received data: id={id}, name={name}, unit={unit}")

    if id in cart:
        cart[id]["quantity"] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "unit": unit,
            "quantity": 1
        }

    session['cart'] = cart

    print(cart)

    return jsonify(cart)


@app.route('/api/carts/<id>', methods=['put'])
def update_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        quantity = int(request.json.get('quantity', 0))
        cart[id]['quantity'] = quantity

    session['cart'] = cart

    return jsonify(cart)


@app.route('/api/carts/<id>', methods=['delete'])
def delete_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        del cart[id]

    session['cart'] = cart

    return jsonify(cart)





if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
