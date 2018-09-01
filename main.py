import sqlite3

# conn = sqlite3.connect("example.db")
conn = sqlite3.connect(":memory:")
c = conn.cursor()

c.execute(
    """
CREATE TABLE users (
 id INTEGER PRIMARY KEY,
 name TEXT
);
"""
)

USERS = [("Thomas",), ("Marcus",), ("Kevin",), ("Alice",)]

c.executemany(
    """
INSERT INTO users (
  name
)
VALUES (
  ?
)""",
    USERS,
)

users = c.execute(
    """
SELECT * FROM users
"""
)

print(list(users))


conn.close()
