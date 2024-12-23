from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from CLINICAPP.app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin
from datetime import datetime
import hashlib

class UserRole(RoleEnum):
    ADMIN = 1
    YTa = 2
    BacSi = 3
    ThuNgan = 4
    USER = 5

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    gender = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=False)
    email = Column(String(100), nullable=True)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dpfbtypxx/image/upload/v1734261617/pengu_iaejdc.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)


class BenhNhan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=False)
    email = Column(String(100), nullable=True)
    age  = Column(String(30), nullable=False)

class ADMIN(User):
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)


class BacSi(User):
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    chungChi = Column(String(100), nullable=True)
    chuyenKhoa = Column(String(100), nullable=True)
    bangCap = Column(String(100), nullable=True)


class YTa(User):
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    chungChi = Column(String(100), nullable=True)
    chuyenMon = Column(String(100), nullable=True)


class ThuNgan(User):
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    bangCap = Column(String(100), nullable=True)


class LoaiThuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenLoaiThuoc = Column(String(100), nullable=False)
    thuoc = relationship('Thuoc', backref='loai_thuoc', lazy=True)

    def __str__(self):
        return self.tenLoaiThuoc


class Thuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    loai_thuoc_id = Column(Integer, ForeignKey(LoaiThuoc.id), nullable=False)

    def __str__(self):
        return self.name

class DsKham(db.Model):
    __tablename__ ='ds_kham'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    dangKyKhams = relationship("DangKyKham", backref="ds_kham")

class DangKyKham(db.Model):
    __tablename__ ='dang_ky_kham'
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_date = Column(DateTime, default=datetime.now())
    created_date = Column(DateTime)
    state = Column(Boolean, nullable=True)
    benhNhan_id = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    dsKham_id = Column(Integer, ForeignKey(DsKham.id))



class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # l1 = LoaiThuoc(tenLoaiThuoc="Kháng sinh")
        # l2 = LoaiThuoc(tenLoaiThuoc="Cảm cúm")
        # l3 = LoaiThuoc(tenLoaiThuoc="Đau bụng")
        # db.session.add_all([l1,l2,l3])

        # t1 = Thuoc(name='Paracetamol', unit='Vi', price=100000, loai_thuoc_id=2)
        # t2 = Thuoc(name='Chlorpromazin', unit='Vien', price=10000, loai_thuoc_id=1)
        # t3 = Thuoc(name='Berberin', unit='Lo', price=12000, loai_thuoc_id=3)
        # db.session.add_all([t1, t2, t3])

        # bn1 = BenhNhan(name="Hồ Đức Trí", gender="Nam", phone="0914117036", birthday="02/02/2004")
        # bn2 = BenhNhan(name="Nguyễn Kiều Phước", gender="Nam", phone="0914117036", birthday="02/02/2004")
        # bn3 = BenhNhan(name="Hồ Kiều Phước", gender="Nam", phone="0914117036", birthday="02/02/2004")
        #
        # db.session.add_all([bn1, bn2, bn3])

        # doctors = [
        #     {
        #         "name": "Nguyen Van A",
        #         "username": "doctorA",
        #         "password": "123",  # MD5 của "admin"
        #         "gender": "Male",
        #         "phone": "0912345678",
        #         "email": "nguyenvana@example.com",
        #         "avatar": "https://res.cloudinary.com/dpfbtypxx/image/upload/v1734261617/pengu_iaejdc.jpg",
        #         "user_role": 3,
        #         "chungChi": "Chứng chỉ Nội khoa",
        #         "chuyenKhoa": "Nội tổng quát",
        #         "bangCap": "Bác sĩ Nội khoa"
        #     },
        #     {
        #         "name": "Tran Thi B",
        #         "username": "doctorB",
        #         "password": "123",  # MD5 của "password"
        #         "gender": "Female",
        #         "phone": "0912345679",
        #         "email": "tranthib@example.com",
        #         "avatar": "https://res.cloudinary.com/dpfbtypxx/image/upload/v1734261617/pengu_iaejdc.jpg",
        #         "user_role": 3,
        #         "chungChi": "Chứng chỉ Nhi khoa",
        #         "chuyenKhoa": "Nhi tổng quát",
        #         "bangCap": "Bác sĩ Nhi khoa"
        #     },
        #     {
        #         "name": "Le Van C",
        #         "username": "doctorC",
        #         "password": "123",  # MD5 của "test"
        #         "gender": "Male",
        #         "phone": "0912345680",
        #         "email": "levanc@example.com",
        #         "avatar": "https://res.cloudinary.com/dpfbtypxx/image/upload/v1734261617/pengu_iaejdc.jpg",
        #         "user_role": 3,
        #         "chungChi": "Chứng chỉ Phẫu thuật",
        #         "chuyenKhoa": "Ngoại tổng quát",
        #         "bangCap": "Bác sĩ Ngoại khoa"
        #     },
        #     {
        #         "name": "Pham Thi D",
        #         "username": "doctorD",
        #         "password": "123",  # MD5 của "qwerty"
        #         "gender": "Female",
        #         "phone": "0912345681",
        #         "email": "phamthid@example.com",
        #         "avatar": "https://res.cloudinary.com/dpfbtypxx/image/upload/v1734261617/pengu_iaejdc.jpg",
        #         "user_role": 3,
        #         "chungChi": "Chứng chỉ Chẩn đoán hình ảnh",
        #         "chuyenKhoa": "Chẩn đoán hình ảnh",
        #         "bangCap": "Bác sĩ Chẩn đoán hình ảnh"
        #     },
        #     {
        #         "name": "Nguyen Van E",
        #         "username": "doctorE",
        #         "password": "123",  # MD5 của "123456"
        #         "gender": "Male",
        #         "phone": "0912345682",
        #         "email": "nguyenvane@example.com",
        #         "avatar": "https://res.cloudinary.com/dpfbtypxx/image/upload/v1734261617/pengu_iaejdc.jpg",
        #         "user_role": 3,
        #         "chungChi": "Chứng chỉ Thần kinh",
        #         "chuyenKhoa": "Thần kinh học",
        #         "bangCap": "Bác sĩ Thần kinh"
        #     },
        #     {
        #         "name": "Tran Thi F",
        #         "username": "doctorF",
        #         "password": "123",  # MD5 của "12345678"
        #         "gender": "Female",
        #         "phone": "0912345683",
        #         "email": "tranthif@example.com",
        #         "avatar": "https://res.cloudinary.com/dpfbtypxx/image/upload/v1734261617/pengu_iaejdc.jpg",
        #         "user_role": 3,
        #         "chungChi": "Chứng chỉ Tim mạch",
        #         "chuyenKhoa": "Tim mạch",
        #         "bangCap": "Bác sĩ Tim mạch"
        #     }
        # ]
        #
        # for doc in doctors:
        #     doctor = BacSi(
        #         name=doc['name'],
        #         username=doc['username'],
        #         password=str(hashlib.md5(doc['password'].encode('utf-8')).hexdigest()),  # MD5 hash đã được tạo sẵn
        #         gender=doc['gender'],
        #         phone=doc['phone'],
        #         email=doc['email'],
        #         avatar=doc['avatar'],
        #         user_role=UserRole.BacSi,  # Enum cho vai trò bác sĩ
        #         chungChi=doc['chungChi'],
        #         chuyenKhoa=doc['chuyenKhoa'],
        #         bangCap=doc['bangCap']
        #         )
        #     db.session.add(doctor)

        # receipt1 = Receipt(user_id=1, created_date="2024-10-01")
        # receipt2 = Receipt(user_id=2, created_date="2024-04-15")
        # receipt3 = Receipt(user_id=3, created_date="2024-05-20")
        # db.session.add_all([receipt1, receipt2, receipt3])

        # detail1 = ReceiptDetails(receipt_id=5, thuoc_id=1, quantity=2, unit_price=100.0)
        # detail2 = ReceiptDetails(receipt_id=6, thuoc_id=2, quantity=6, unit_price=150.0)
        # detail3 = ReceiptDetails(receipt_id=7, thuoc_id=3, quantity=1, unit_price=200.0)
        # db.session.add_all([detail1, detail2, detail3])

        # admin_user = ADMIN(
        #     name="Admin User",
        #     username="adminuser",
        #     password=str(hashlib.md5('Admin@123'.encode('utf-8')).hexdigest()),
        #     gender="Male",
        #     phone="1234567890",
        #     email="admin@example.com",
        #     avatar='https://res.cloudinary.com/dpfbtypxx/image/upload/v1734261617/pengu_iaejdc.jpg',
        #     user_role=UserRole.ADMIN
        # )
        # db.session.add(admin_user)

        db.session.commit()