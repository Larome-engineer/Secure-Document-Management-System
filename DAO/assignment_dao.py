import sqlite3 as sql


def create_assignment(name, desc, date, owner, recipient):  # For creating new Assignment
    with sql.connect('sdms.sqlite') as base:
        base.cursor().execute("insert into assignment(assignment_name, "
                              "assignment_description, assignment_date, assignment_active, assignment_owner, "
                              "assignment_recipient) "
                              "values (?, ?, ?, ?, ?, ?)",
                              (name, desc, date, 'Активно', owner, recipient))
        base.commit()


def search_a_id_by_a_name(a_name):  # For searching Assignment_id by Assignment_name
    with sql.connect('sdms.sqlite') as base:
        return base.cursor().execute("select assignment_id from assignment where assignment_name=?",
                                     (a_name,)).fetchone()


def check_on_active(a_id):
    with sql.connect('sdms.sqlite') as base:
        return base.cursor().execute("select assignment_active from assignment where assignment_id=?", (a_id,)).fetchone()


def search_owner_by_a_name(a_name):  # For searching Assignment_owner by Assignment_name
    with sql.connect('sdms.sqlite') as base:
        return base.cursor().execute("select assignment_owner from assignment where assignment_name=?",
                                     (a_name,)).fetchone()


def cancel_assignment(a_id):  # To change active_status to 'CLOSED'
    with sql.connect('sdms.sqlite') as base:
        base.cursor().execute("update assignment set assignment_active = 'Закрыто' where assignment_id = ?", (a_id,))
        base.commit()


def delegated_assignment(delegated_for, a_id):  # To delegated Assignment by id and set recipient
    with sql.connect('sdms.sqlite') as base:
        base.cursor().execute("update assignment set assignment_recipient = ? where assignment_id = ?", (delegated_for, a_id,))
        base.commit()


def check_on_exists(a_name):  # Checking for exists by Assignment_name
    with sql.connect('sdms.sqlite') as base:
        all_exists = []
        check = base.cursor().execute("select assignment_id from assignment where assignment_name=?",
                                      (a_name,)).fetchall()

        for i in check:
            record = str(i[0])
            all_exists.append(record)
        return all_exists


def find_all_assignment():  # Searching all active_assignments (For ADMIN)
    with sql.connect('sdms.sqlite') as base:
        assignments = []
        a = base.cursor().execute("select assignment_name from assignment where assignment_active=?",
                                  ('Активно',)).fetchall()

        for i in a:
            assignment = str(i[0])
            assignments.append(assignment)

        return assignments


def find_all_assignment_for_head():  # Searching all active_assignments (For HEAD OF DEPARTMENT)
    with sql.connect('sdms.sqlite') as base:
        assignments = []
        a = base.cursor().execute("select assignment_name from assignment where assignment_recipient=? "
                                  "and assignment_active=?", ('HEAD', 'Активно',)).fetchall()

        for i in a:
            assignment = str(i[0])
            assignments.append(assignment)

        return assignments


def find_all_assignment_for_spec():  # Searching all active_assignments (For SPECIALIST)
    with sql.connect('sdms.sqlite') as base:
        assignments = []
        a = base.cursor().execute("select assignment_name from assignment where assignment_recipient=? "
                                  "and assignment_active=?", ('SPEC', 'Активно',)).fetchall()

        for i in a:
            assignment = str(i[0])
            assignments.append(assignment)

        return assignments
