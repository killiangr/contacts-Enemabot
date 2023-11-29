import sys
import sqlite3
from pathlib import Path
from datetime import datetime
from faker import Faker

class Contacts:
    def __init__(self, db_path):
        self.db_path = db_path
        if not db_path.exists():
            print("Migrating db")
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE contacts(
                  id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL
                );
                
                CREATE UNIQUE INDEX index_contacts_email ON contacts(email);
              """
            )
            connection.commit()
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

    def insert_contacts(self, contacts: [str, str]):
        print("Inserting contacts")
        cursor = self.connection.cursor()

        for index, contact in enumerate(contacts):
            cursor.executemany("""
                insert into contacts(name, email) values (
                    ?, ?
                )
            """, [contact[0], contact[1]])

    def get_name_for_email(self, email):
        print("Looking for email", email)
        cursor = self.connection.cursor()
        start = datetime.now()
        cursor.execute(
            """
            SELECT * FROM contacts
            WHERE email = ?
            """,
            (email,),
        )
        row = cursor.fetchone()
        end = datetime.now()

        elapsed = end - start
        print("query took", elapsed.microseconds / 1000, "ms")
        if row:
            name = row["name"]
            print(f"Found name: '{name}'")
            return name
        else:
            print("Not found")


def yield_contacts(num_contacts: int):
    faker = Faker()
    yield "charlie", "charlie@acme.corp"
    for i in range(1, num_contacts):
        yield faker.name(), faker.email()


def main():
    num_contacts = int(sys.argv[1])
    db_path = Path("contacts.sqlite3")
    contacts = Contacts(db_path)
    contacts.insert_contacts(yield_contacts(num_contacts))
    charlie = contacts.get_name_for_email("charlie@acme.corp")


if __name__ == "__main__":
    main()