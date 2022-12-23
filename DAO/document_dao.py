import sqlite3 as sql
from templates import variables


def create_document(a_id, name, desc, date):  # Creating new Document
    with sql.connect('sdms.sqlite') as base:
        base.cursor().execute("insert into document(doc_assignment_id, doc_link_name, "
                              "doc_description, doc_date, sign_by, under_revision) "
                              "values (?, ?, ?, ?, ?, ?)", (a_id, name, desc, date, 'Нет подписи', 'Не отправлено'))
        base.commit()


def find_all_docx_for_admin():  # Searching all documents for ADMIN (which sign by HEAD)
    with sql.connect('sdms.sqlite') as base:
        documents = []
        docs = base.cursor().execute("select doc_link_name from Document where sign_by = ?", ('HEAD',)).fetchall()

        for i in docs:
            document = str(i[0]).replace(variables.server_path, '')
            documents.append(document)

        return documents


def find_all_docx_for_head():  # Searching all documents for HEAD OF DEPARTMENT (which sign by SPECIALIST)
    with sql.connect('sdms.sqlite') as base:
        documents = []
        docs = base.cursor().execute("select doc_link_name from Document where sign_by = ?", ('SPEC',)).fetchall()

        for i in docs:
            document = str(i[0]).replace(variables.server_path, '')
            documents.append(document)

        return documents


def find_all_docx_on_revision_for_head():  # Searching all documents for HEAD OF DEPARTMENT under_revision
    with sql.connect('sdms.sqlite') as base:
        documents_on_revision = []
        docs = base.cursor().execute("select doc_link_name from Document "
                                     "where under_revision = 'Отправлено на доработку' and sign_by = 'SPEC'").fetchall()

        for i in docs:
            document = str(i[0]).replace(variables.server_path, '')
            documents_on_revision.append(document)

        return documents_on_revision


def find_all_docx_on_revision_for_spec():  # Searching all documents for SPECIALIST under_revision
    with sql.connect('sdms.sqlite') as base:
        documents_on_revision = []
        docs = base.cursor().execute("select doc_link_name from Document "
                                     "where under_revision = 'Отправлено на доработку' and sign_by = 'Нет подписи'").fetchall()

        for i in docs:
            document = str(i[0]).replace(variables.server_path, '')
            documents_on_revision.append(document)

        return documents_on_revision


def find_all_docx_for_spec():  # Searching all documents for SPECIALIST (which sign by 'NO SIGN')
    with sql.connect('sdms.sqlite') as base:
        documents = []
        docs = base.cursor().execute("select doc_link_name from Document where sign_by = ?", ('Нет подписи',)).fetchall()

        for i in docs:
            document = str(i[0]).replace(variables.server_path, '')
            documents.append(document)

        return documents


def search_doc_id_by_name(d_name):  # Searching document by Document_id
    with sql.connect('sdms.sqlite') as base:
        return base.cursor().execute("select doc_id from document where doc_link_name=?", (d_name,)).fetchone()


def search_a_id_by_doc_name(d_name):  # Searching Assignment_id by Document_name
    with sql.connect('sdms.sqlite') as base:
        return base.cursor().execute("select doc_assignment_id from document where doc_link_name=?", (d_name,)).fetchone()


def check_on_sign(name):  # Checking for sign
    with sql.connect('sdms.sqlite') as base:
        return base.cursor().execute("select sign_by from document where doc_link_name=?", (name, )).fetchone()


def delete_doc_by_id(d_id):  # Delete Document by Document_id
    with sql.connect('sdms.sqlite') as base:
        base.cursor().execute("delete from document where doc_id = ?", (d_id,))
        base.commit()


def signing_by(doc_name, a_id, user_post):  # To signing Document
    with sql.connect('sdms.sqlite') as base:
        if user_post == 'ADMIN':
            base.cursor().execute("update Document set sign_by = 'ADMIN', under_revision='Отработан' "
                                  "where doc_link_name= ?", (doc_name,))

            base.cursor().execute("update Assignment set assignment_active = 'Закрыто' where assignment_id = ?",
                                  (a_id,))
            base.commit()

        elif user_post == 'HEAD':
            base.cursor().execute("update Document set sign_by = 'HEAD' where doc_link_name = ?", (doc_name,))
            base.commit()

        elif user_post == 'SPEC':
            base.cursor().execute("update Document set sign_by = 'SPEC' where doc_link_name = ?", (doc_name,))
            base.commit()


def send_to_revision(doc_id, sign_by):  # For send to revision
    with sql.connect('sdms.sqlite') as base:
        base.cursor().execute("update Document set under_revision='Отправлено на доработку', sign_by=? "
                              "where doc_id = ?", (sign_by, doc_id,))
        base.commit()
