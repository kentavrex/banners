from sqlalchemy import ForeignKey

from sqlalchemy.orm import mapped_column, Mapped, relationship

from repositories.sql import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("user_roles.id"))
    role: Mapped[list["UserRole"]] = relationship(lazy="joined", back_populates="users")


class UserRole(Base):
    __tablename__ = 'user_roles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)

    users: Mapped[list["User"]] = relationship(lazy="joined", back_populates="role")


class Banner(Base):
    __tablename__ = 'banners'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    feature_id: Mapped[int] = mapped_column(ForeignKey("features.id"))

    feature: Mapped[list["Feature"]] = relationship(lazy="joined", back_populates="banners")
    tags: Mapped[list["Tag"]] = relationship(lazy="joined", secondary="banners_tags", back_populates="banners")


class Feature(Base):
    __tablename__ = 'features'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    banners: Mapped[list["Banner"]] = relationship(lazy="joined", back_populates="feature")


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    banners: Mapped[list["Banner"]] = relationship(lazy="joined", secondary="banners_tags", back_populates="tags")


class BannerTag(Base):
    __tablename__ = "banners_tags"

    banner_id: Mapped[int] = mapped_column(ForeignKey("banners.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    banner: Mapped["Banner"] = relationship(lazy="joined", cascade="all, delete")
    tag: Mapped["Tag"] = relationship(lazy="joined", cascade="all, delete")
