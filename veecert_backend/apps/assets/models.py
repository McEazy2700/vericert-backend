from datetime import datetime
import enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from veecert_backend.config.database import Base
from veecert_backend.constants.table_names import TableNames
from .managers.ipfs_asset import IPFSAssetManager
from .managers.document import DocumentManager

if TYPE_CHECKING:
    from veecert_backend.apps.users.models import Client
    from .graphql.types.enums import DocumentVisibilityType


class DocumentVisibility(enum.Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

    def to_gql(self) -> "DocumentVisibilityType":
        from .graphql.types.enums import DocumentVisibilityType

        match self:
            case DocumentVisibility.PUBLIC:
                return DocumentVisibilityType.PUBLIC
            case DocumentVisibility.PRIVATE:
                return DocumentVisibilityType.PRIVATE


class IPFSAsset(Base):
    __tablename__ = TableNames.IPFS_ASSET

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ipfs_hash: Mapped[str] = mapped_column(unique=True)
    pin_size: Mapped[int] = mapped_column(BigInteger)
    timestamp: Mapped[datetime]
    is_duplicate: Mapped[bool]
    extension: Mapped[Optional[str]] = mapped_column(nullable=True)
    client_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(f"{TableNames.CLIENT}.id"), nullable=True
    )

    client: Mapped[Optional["Client"]] = relationship(
        back_populates="ipfs_assets", foreign_keys=[client_id]
    )
    document: Mapped[Optional["Document"]] = relationship(back_populates="ipfs_asset")

    manager = IPFSAssetManager


class Document(Base):
    __tablename__ = TableNames.DOCUMENT
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str]
    asset_id: Mapped[int] = mapped_column(BigInteger)
    visibility: Mapped[DocumentVisibility] = mapped_column(
        default=DocumentVisibility.PUBLIC
    )
    authorised_email: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    ipfs_asset_id: Mapped[int] = mapped_column(
        ForeignKey(f"{TableNames.IPFS_ASSET}.id")
    )

    ipfs_asset: Mapped[IPFSAsset] = relationship(
        back_populates="document", foreign_keys=[ipfs_asset_id], uselist=False
    )

    manager = DocumentManager
