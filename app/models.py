from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin

class UserRole(RoleEnum):
    ADMIN = 1
    YTa = 2
    BacSi = 3
    ThuNgan = 4
    USER = 5

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dpfbtypxx/image/upload/v1734261617/pengu_iaejdc.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)


class BenhNhan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=False)
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
    tenThuoc = Column(String(100), nullable=False)
    donViThuoc = Column(String(50), nullable=False)
    giaTien = Column(Float, nullable=False)
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

        # t1 = Thuoc(tenThuoc='Paracetamol', donViThuoc='Vi', giaTien=100000, loai_thuoc_id=2)
        # t2 = Thuoc(tenThuoc='Chlorpromazin', donViThuoc='Vien', giaTien=10000, loai_thuoc_id=1)
        # t3 = Thuoc(tenThuoc='Berberin', donViThuoc='Lo', giaTien=12000, loai_thuoc_id=3)
        # db.session.add_all([t1, t2, t3])

        bn1 = BenhNhan(name="Hồ Đức Trí", gender="Nam", phone="0914117036", birthday="02/02/2004")
        bn2 = BenhNhan(name="Nguyễn Kiều Phước", gender="Nam", phone="0914117036", birthday="02/02/2004")
        bn3 = BenhNhan(name="Hồ Kiều Phước", gender="Nam", phone="0914117036", birthday="02/02/2004")

        db.session.add_all([bn1, bn2, bn3])

        db.session.commit()