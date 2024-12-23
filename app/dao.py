from CLINICAPP.app.models import User, BenhNhan, Thuoc, Receipt, ReceiptDetails, LoaiThuoc, DangKyKham, BacSi
from CLINICAPP.app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from datetime import datetime
from sqlalchemy import func


def get_user_by_id(id):
    return User.query.get(id)


def load_patients(kw=None):
    query = BenhNhan.query

    if kw:
        query = query.filter(BenhNhan.name.contains(kw))

    return query.all()


def load_medicines(kw=None):
    query = Thuoc.query

    if kw:
        query = query.filter(Thuoc.name.contains(kw))

    return query.all()


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User.query.filter(User.username.__eq__(username.strip()),
                          User.password.__eq__(password))
    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()


def revenue_stats(kw=None):
    query = db.session.query(Thuoc.id, Thuoc.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price)) \
        .join(ReceiptDetails, ReceiptDetails.thuoc_id.__eq__(Thuoc.id)).group_by(Thuoc.id)

    if kw:
        query = query.filter(Thuoc.name.contains(kw))

    return query.all()


def period_stats(p='month', year=datetime.now().year):
    return db.session.query(func.extract(p, Receipt.created_date),
                            func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price)) \
        .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id)) \
        .group_by(func.extract(p, Receipt.created_date), func.extract('year', Receipt.created_date)) \
        .order_by().all()


def stats_products():
    return db.session.query(LoaiThuoc.id, LoaiThuoc.tenLoaiThuoc, func.count(Thuoc.id)) \
        .join(Thuoc, Thuoc.LoaiThuoc_id.__eq__(LoaiThuoc.id), isouter=True).group_by(LoaiThuoc.id).all()


def load_doctors(kw=None):
    query = BacSi.query

    if kw:
        query = query.filter(BacSi.name.contains(kw))

    return query.all()


def add_ExamineForm(phone,name, age, gender, email, appointment_date):

    patient = BenhNhan.query.filter(BenhNhan.phone.__eq__(phone)).first()
    if not patient:
        patient = BenhNhan(
            name=name,
            phone=phone,
            age=age,
            gender=gender,
            email=email,

        )
        db.session.add(patient)
        db.session.commit()

    new_DangKyKham = DangKyKham(
        benhNhan_id=patient.id,
        appointment_date=appointment_date,
        created_date=datetime.now(),
        state=False
    )
    db.session.add(new_DangKyKham)
    db.session.commit()
    return {"message": "Đăng kí khám đã được ghi nhận, xin vui lòng chờ mail từ chúng tôi!"}, 201

if __name__ == '__main__':
    with app.app_context():
        print(period_stats())
