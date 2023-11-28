import sqlite3


conn = sqlite3.connect("client.sqlite")
cursor = conn.cursor()

new_mashines = [
    ("Сварочный аппарат №1", "true"),
    ("Пильный аппарат №2", "true"),
    ("Фрезер №3", "true"),
]

cursor.executemany("INSERT INTO endpoints (name, active) VALUES (?, ?)", new_mashines)

new_endpoints = ("Сварочный аппарат №1", "Пильный аппарат №2", "Фрезер №3")
cursor.execute("SELECT id FROM endpoints WHERE name IN (?, ?, ?)", new_endpoints)
new_endpoint_ids = cursor.fetchall()

for new_endpoint_id in new_endpoint_ids:
    cursor.execute(
        "INSERT INTO endpoint_groups (endpoint_id, name) VALUES (?, ?)",
        (new_endpoint_id[0], "Цех №2"),
    )

old_endpoints = ("Фрезерный станок", "Старый ЧПУ", "Сварка")
cursor.execute(
    "SELECT DISTINCT endpoint_id, reason_name, reason_hierarchy FROM endpoint_reasons WHERE endpoint_id IN (SELECT id FROM endpoints WHERE name IN (?, ?, ?))",
    old_endpoints,
)
reasons = cursor.fetchall()

for new_endpoint_id in new_endpoint_ids:
    unique_reasons = set()
    for reason in reasons:
        unique_reason = (reason[1], reason[2])
        if unique_reason not in unique_reasons:
            cursor.execute(
                "INSERT INTO endpoint_reasons (endpoint_id, reason_name, reason_hierarchy) VALUES (?, ?, ?)",
                (new_endpoint_id[0], reason[1], reason[2]),
            )
            unique_reasons.add(unique_reason)

conn.commit()

conn.close()
