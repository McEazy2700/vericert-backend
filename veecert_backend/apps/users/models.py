from typing import List, Optional
import uuid
from sqlalchemy import JSON, UUID, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from veecert_backend.config.database import Base
from veecert_backend.constants.table_names import TableNames
from .managers.client import ClientManager
from .managers.user import UserManager
from .managers.client_package import ClientPackageManager
from .managers.auth_token import AuthTokenManager
from .managers.package import PackageManager


class User(Base):
    __tablename__ = TableNames.USER
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str]
    password_hash: Mapped[Optional[str]] = mapped_column(nullable=True)

    client: Mapped[Optional["Client"]] = relationship(back_populates="user")
    auth_token: Mapped[Optional["AuthToken"]] = relationship(back_populates="user")

    manager = UserManager

    @validates("email")
    def validate_email(self, _, address: str):
        if "@" not in address:
            raise ValueError("Failed simple email validation")
        return address


class Package(Base):
    __tablename__ = TableNames.PACKAGE
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str]
    price: Mapped[int] = mapped_column(BigInteger, comment="Price in micro algos")
    storage_capacity: Mapped[int] = mapped_column(
        BigInteger, comment="Storage capacity in KB"
    )
    offers: Mapped[List[str]] = mapped_column(JSON, default=[])
    monthly_requests: Mapped[int] = mapped_column(BigInteger)
    client_packages: Mapped[List["ClientPackage"]] = relationship(
        back_populates="package"
    )

    manager = PackageManager


class ClientPackage(Base):
    __tablename__ = TableNames.CLIENT_PACKAGE
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey(f"{TableNames.CLIENT}.id"))
    package_id: Mapped[int] = mapped_column(ForeignKey(f"{TableNames.PACKAGE}.id"))
    txn_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    api_public_key: Mapped[str] = mapped_column(unique=True, index=True)
    api_secret_key: Mapped[str] = mapped_column(unique=True)
    has_pending_payment: Mapped[bool] = mapped_column(default=False)

    client: Mapped["Client"] = relationship(
        back_populates="client_package", foreign_keys=[client_id], uselist=False
    )
    package: Mapped[Package] = relationship(
        back_populates="client_packages", foreign_keys=[package_id]
    )

    manager = ClientPackageManager


class Client(Base):
    __tablename__ = TableNames.CLIENT
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    image_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    used_storage: Mapped[int] = mapped_column(BigInteger, default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey(f"{TableNames.USER}.id"))

    user: Mapped["User"] = relationship(
        back_populates="client", foreign_keys=[user_id], uselist=False
    )
    client_package: Mapped["ClientPackage"] = relationship(
        back_populates="client", uselist=False
    )
    ipfs_assets: Mapped[List["IPFSAsset"]] = relationship(back_populates="client")

    manager = ClientManager


class AuthToken(Base):
    __tablename__ = TableNames.AUTH_TOKEN
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    auth_token: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey(f"{TableNames.USER}.id"))
    user: Mapped[User] = relationship(
        back_populates="auth_token", foreign_keys=[user_id], uselist=False
    )

    manager = AuthTokenManager


from veecert_backend.apps.assets.models import IPFSAsset
