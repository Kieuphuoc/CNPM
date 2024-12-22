from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin
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
    birthday = Column(String(30), nullable=False)



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


class Thuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    loai_thuoc_id = Column(Integer, ForeignKey(LoaiThuoc.id), nullable=False)

class PhieuDangKy(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phoneNumber = Column(String(20), nullable=False)
    gender = Column(String(30), nullable=False)
    birthDay = Column(String(50), nullable=False)
    diaChi = Column(String(100), nullable=True)




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

        db.session.commit()