import sqlite3

import pytest
from birdy.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
