import sqlite3
import pprint

pp = pprint.PrettyPrinter(indent=4).pprint

# conn = sqlite3.connect("example.db")
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute(
    """
CREATE TABLE users (
 id INTEGER PRIMARY KEY,
 name TEXT NOT NULL
);
"""
)
c.execute(
    """
CREATE TABLE lists (
 id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 user_id INTEGER NOT NULL REFERENCES user(id) ON DELETE RESTRICT
);
"""
)
c.execute(
    """
CREATE TABLE categories (
 id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 list_id INTEGER NOT NULL REFERENCES lists(id) ON DELETE RESTRICT,
 display_order INTEGER NOT NULL DEFAULT 0
);
"""
)
c.execute(
    """
CREATE TABLE items (
 id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 grams INTEGER NOT NULL
);
"""
)
c.execute(
    """
CREATE TABLE category_items (
 id INTEGER PRIMARY KEY,
 category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
 item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE RESTRICT,
 display_order INTEGER NOT NULL DEFAULT 0
);
"""
    # TODO: count, selected?
)

USERS = [("Thomas",), ("Marcus",), ("Kevin",), ("Alice",)]
LISTS = [
    ("Ultralight setup", 1),
    ("Budget backpacking", 2),
    ("Winter setup", 1),
]
CATEGORIES = [
    # Thomas' ultralight setup
    ("Cooking", 1, 2),
    ("Shelter", 1, 0),
    ("Sleep", 1, 1),
    # Marcus' budget backpacking list
    ("Shelter", 2, 0),
    ("Sleep", 2, 1),
    ("Cooking", 2, 2),
]
ITEMS = [
    ("Zpacks Duplex", 535),
    ("Katabatic 30", 601),
    ("Vargo stove", 195),
    # Budget backpacking
    ("REI tend", 780),
    ("Cheap bag", 654),
    ("MSR stove set", 390),
]
CATEGORY_ITEMS = [
    (1, 1, 0),
    (2, 2, 0),
    (3, 3, 0),
    # Budget backpacking
    (4, 4, 0),
    (5, 5, 0),
    (6, 6, 0),
]

c.executemany("INSERT INTO users (name) VALUES (?)", USERS)
c.executemany("INSERT INTO lists (name, user_id) VALUES (?, ?)", LISTS)
c.executemany(
    "INSERT INTO categories (name, list_id, display_order) VALUES (?, ?, ?)",
    CATEGORIES,
)
c.executemany("INSERT INTO items (name, grams) VALUES (?, ?)", ITEMS)
c.executemany(
    """
INSERT INTO category_items
(category_id, item_id, display_order)
VALUES (?, ?, ?)
""",
    CATEGORY_ITEMS,
)

# c.execute("DELETE FROM lists WHERE id = 1")

q = c.execute(
    """
SELECT
users.name AS user, 
lists.name AS list,
categories.name AS category,
items.name AS item,
items.grams AS grams
FROM items
JOIN category_items
ON category_items.item_id = items.id
JOIN categories
ON categories.id = category_items.category_id
JOIN lists
ON categories.list_id = lists.id
JOIN users
ON lists.user_id = users.id
ORDER BY
users.name,
lists.name,
categories.display_order,
category_items.display_order,
items.name
"""
)

from utils import chunk, by_key, indent

rows = [dict(i) for i in q]
pp(rows)
print("\n\n")

# first = q[0]
# print(first.keys())


for user, user_rows in by_key("user", rows):
    print()
    print(user)
    print("=" * len(user))
    for list_name, list_rows in by_key("list", user_rows):
        print(indent(1, list_name))
        print(indent(1, "-" * len(list_name)))
        for category, category_rows in by_key("category", list_rows):
            print(indent(2, category + ":"))
            # print(indent(2, "-" * len(list_name)))
            for item in category_rows:
                name = item["item"]
                grams = item["grams"]
                s = "- " + name + "\t" + str(grams) + "g"
                print(indent(3, s))


conn.close()
