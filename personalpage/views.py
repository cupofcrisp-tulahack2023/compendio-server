from flask import Blueprint, render_template, request, redirect, flash, url_for
from typing import Sequence

from sqlalchemy.exc import IntegrityError

from personalpage.models import Boards
from auth.models import User
from sqlalchemy import select
from database import db

personal_app = Blueprint(
    "personal_app",
    __name__,
    url_prefix="/personal",
)


@personal_app.get("/")
def personal_start():
    return render_template(
        "personal/index.html"
    )

@personal_app.get("/boards/", endpoint="list")
def board_list():
    stmt = select(Boards)
    boards: Sequence[Boards] = db.session.scalars(stmt)
    return render_template(
        "personal/index.html",
        boards=boards
    )


@personal_app.route("/add/", methods={"GET", "POST"}, endpoint="add")
def create_board():
    if request.method == "GET":
        return render_template("personal/add.html")
    title = request.form.get("board-title")
    print(title)

    board = Boards(title=title)
    db.session.add(board)

    try:
        db.session.commit()
    except IntegrityError:
        flash(f"Sorry, something went wrong", category="warning")
        return redirect(request.path)


    url = url_for("personal_app.detail", board_id=board.id)
    return redirect(url)


def get_board_by_id_or_raise(board_id: int) -> Boards:
   board: Boards = db.get_or_404(
        Boards,
        board_id,
        description=f"Board #{board_id} not found!",
    )
   return board


@personal_app.get("/<int:board_id>/", endpoint="detail")
def get_board_by_id(board_id: int):
    return render_template(
        "personal/detail.html",
        board=get_board_by_id_or_raise(board_id),
    )


@personal_app.route(
    "/<int:board_id>/confirm-delete/",
    methods=["GET", "POST"],
    endpoint="confirm_delete",
)
def confirm_delete_board(board_id: int):
    board = get_board_by_id_or_raise(board_id)
    if request.method == "GET":
        return render_template(
            "personal/confirm-delete.html",
            board=board,
        )

    title = board.title
    db.session.delete(board)
    db.session.commit()
    flash(f"Board {title!r} deleted.", category="danger")
    return redirect(url_for("personal_app.list"))


