from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


vehicle_category = Table(
    "vehicle_category",
    Base.metadata,
    Column("vehicle_id", ForeignKey("vehicle.id"), primary_key=True),
    Column("category_id", ForeignKey("category.id"), primary_key=True),
)


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    cnpj: Mapped[Optional[str]] = mapped_column(String(18), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="organization")
    users: Mapped[list["User"]] = relationship(back_populates="organization")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="organization")
    sales: Mapped[list["Sale"]] = relationship(back_populates="organization")


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    vehicles: Mapped[list["Vehicle"]] = relationship(
        secondary=vehicle_category,
        back_populates="categories",
    )


class Owner(Base):
    __tablename__ = "owner"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    document: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="owner")


class Vehicle(Base):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand: Mapped[str] = mapped_column(String(80), nullable=False)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    year_manufacture: Mapped[int] = mapped_column(Integer, nullable=False)
    year_model: Mapped[int] = mapped_column(Integer, nullable=False)
    plate: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, unique=True)
    chassis: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)
    color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    mileage: Mapped[float] = mapped_column(Float, default=0.0)
    fuel_type: Mapped[str] = mapped_column(String(50), nullable=False)
    transmission: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    condition: Mapped[str] = mapped_column(String(50), nullable=False, default="novo")
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("owner.id"), nullable=True)

    organization: Mapped[Organization] = relationship(back_populates="vehicles")
    owner: Mapped[Optional[Owner]] = relationship(back_populates="vehicles")
    categories: Mapped[list[Category]] = relationship(
        secondary=vehicle_category,
        back_populates="vehicles",
    )
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="vehicle")
    sales: Mapped[list["Sale"]] = relationship(back_populates="vehicle")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    profile: Mapped[str] = mapped_column(String(80), default="operador")

    organization_id: Mapped[Optional[int]] = mapped_column(ForeignKey("organization.id"), nullable=True)
    organization: Mapped[Optional[Organization]] = relationship(back_populates="users")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="user")
    sales: Mapped[list["Sale"]] = relationship(back_populates="seller")


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    document: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="client")
    sales: Mapped[list["Sale"]] = relationship(back_populates="buyer")


class Reservation(Base):
    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ativo")
    observation: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)

    vehicle: Mapped[Vehicle] = relationship(back_populates="reservations")
    user: Mapped[User] = relationship(back_populates="reservations")
    client: Mapped[Client] = relationship(back_populates="reservations")
    organization: Mapped[Organization] = relationship(back_populates="reservations")


class Sale(Base):
    __tablename__ = "sale"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), nullable=False)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("client.id"), nullable=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    sale_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    final_price: Mapped[float] = mapped_column(Float, default=0.0)
    payment_method: Mapped[str] = mapped_column(String(50), default="dinheiro")
    status: Mapped[str] = mapped_column(String(50), default="concluida")
    observation: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    vehicle: Mapped[Vehicle] = relationship(back_populates="sales")
    buyer: Mapped[Client] = relationship(back_populates="sales")
    seller: Mapped[User] = relationship(back_populates="sales")
    organization: Mapped[Organization] = relationship(back_populates="sales")
