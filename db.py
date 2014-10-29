# coding=utf-8
from __future__ import unicode_literals
import sqlite3


class DBHelper(object):
    def __init__(self):
        self.cursor = None
        self.connection = None
        self.count = 0
        self.connect()
        self.create_db()

    def connect(self):
        self.connection = sqlite3.connect('linkedin.db')
        self.cursor = self.connection.cursor()

    def create_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS COMPANIES
           (ENTITY_ID      TEXT,
           NAME           TEXT     NOT NULL,
           SITE           TEXT,
           NUM_OF_EMPLOYEES TEXT);''')

    def add_to_db(self, company):
        self.count += 1
        print '|%s|%s|%s|%s|%s|' % (self.count, company.entity_id, company.name, company.site, company.num_of_employees)
        self.cursor.execute(
            "INSERT INTO COMPANIES VALUES ('%s','%s','%s','%s');" %
            (company.entity_id, company.name, company.site, company.num_of_employees)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()
