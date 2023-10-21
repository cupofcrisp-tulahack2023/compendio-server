from database import db
from sqlalchemy.orm import Mapped, mapped_column


class Boards(db.Model):
    __tablename__ = "board"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str | None]
    # user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


class Lessons(Boards):
    __tablename__ = "lessons"

    name: Mapped[str] = mapped_column(nullable=False)
    descriptions: Mapped[str]












