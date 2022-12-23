import sqlite3 as sql


def create_person(tg_id, username, post, password):
    with sql.connect('sdms.sqlite') as base:
        base.cursor().execute("insert into person(tg_id, username, post, password) values (?, ?, ?, ?)",
                              (tg_id, username, post, password))
        base.commit()


def search_on_exists(tg_id):
    with sql.connect('sdms.sqlite') as base:
        return base.cursor().execute("select tg_id from person where tg_id = ?", (tg_id,)).fetchone()


def search_post_by_tg_id(user_tg_id):
    with sql.connect('sdms.sqlite') as base:
        return base.cursor().execute("select post from person where tg_id = ?;", (user_tg_id,)).fetchone()


