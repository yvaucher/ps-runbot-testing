# -*- coding: utf-8 -*-
import re
re_write_db = re.compile(r'\b(update|delete|insert)\b', re.I)
from odoo.sql_db import Cursor
from psycopg2 import sql

old_execute = Cursor.execute

def new_execute(self, query, params=None, log_exceptions=None):
    result = old_execute(self, query, params, log_exceptions)

    if isinstance(query, sql.Composable):
        query = query.as_string(self.connection)
    if re_write_db.search(query):
        self.method_is_writing_in_db = True
    return result

Cursor.execute = new_execute
