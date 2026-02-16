from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

import psycopg2
import random
from datetime import date, timedelta

DB_CONFIG = {
    "dbname": os.getenv("PG_DATABASE"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT"),
}


DDL = """
DROP TABLE IF EXISTS sales   CASCADE;
DROP TABLE IF EXISTS albums  CASCADE;
DROP TABLE IF EXISTS artists CASCADE;

CREATE TABLE artists (
    artist_id   SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    genre       VARCHAR(100),
    country     VARCHAR(100)
);

CREATE TABLE albums (
    album_id    SERIAL PRIMARY KEY,
    title       VARCHAR(300) NOT NULL,
    artist_id   INTEGER NOT NULL REFERENCES artists(artist_id),
    release_date DATE,
    price       NUMERIC(8, 2)
);

CREATE TABLE sales (
    sale_id     SERIAL PRIMARY KEY,
    album_id    INTEGER NOT NULL REFERENCES albums(album_id),
    sale_date   DATE NOT NULL,
    quantity    INTEGER NOT NULL DEFAULT 1,
    total_amount NUMERIC(10, 2) NOT NULL
);
"""


ARTISTS = [
    ("Taylor Swift", "Pop", "USA"),
    ("Ed Sheeran", "Pop", "UK"),
    ("Kendrick Lamar", "Hip-Hop", "USA"),
    ("Adele", "Soul", "UK"),
    ("Bad Bunny", "Reggaeton", "Puerto Rico"),
    ("BTS", "K-Pop", "South Korea"),
    ("Drake", "Hip-Hop", "Canada"),
    ("Billie Eilish", "Alt-Pop", "USA"),
    ("The Weeknd", "R&B", "Canada"),
    ("Dua Lipa", "Pop", "UK"),
]

ALBUMS_PER_ARTIST = [
    # (title, release_date, price) — one list per artist
    [("Midnights", "2022-10-21", 14.99), ("1989 (TV)", "2023-10-27", 13.99)],
    [("Subtract", "2023-05-05", 12.99), ("Equals", "2021-10-29", 11.99)],
    [("Mr. Morale", "2022-05-13", 13.99), ("GNX", "2023-07-14", 14.99)],
    [("30", "2021-11-19", 14.99), ("Easy On Me (Single)", "2023-03-10", 1.29)],
    [("Un Verano Sin Ti", "2022-05-06", 11.99), ("Nadie Sabe", "2023-09-01", 12.99)],
    [("Proof", "2022-06-10", 19.99), ("Take Two", "2023-06-09", 1.29)],
    [("Her Loss", "2022-11-04", 13.99), ("For All The Dogs", "2023-10-06", 14.99)],
    [("Happier Than Ever", "2021-07-30", 13.99), ("What Was I Made For?", "2023-07-21", 1.29)],
    [("Dawn FM", "2022-01-07", 12.99), ("Starboy Deluxe", "2023-04-15", 14.99)],
    [("Future Nostalgia", "2020-03-27", 11.99), ("Radical Optimism", "2023-11-10", 13.99)],
]


def seed():
    DB_CONNECTION = psycopg2.connect(**DB_CONFIG)
    DB_CONNECTION.autocommit = True # by default it uses transactions, but we want to execute DDL and multiple inserts without manual commit
    DB = DB_CONNECTION.cursor()

    # ── Create tables using DDL ──────────────────────────────────────────────────────────
    DB.execute(DDL)
    print("Tables created")

    # ── artists ──────────────────────────────────────────────────────
    artist_ids = []
    for name, genre, country in ARTISTS:
        DB.execute(
            "INSERT INTO artists (name, genre, country) VALUES (%s, %s, %s) RETURNING artist_id",
            (name, genre, country),
        )
        artist_ids.append(DB.fetchone()[0])
    print(f"Inserted {len(artist_ids)} artists")

    # ── albums ───────────────────────────────────────────────────────
    album_rows: list[tuple[int, float]] = []  # (album_id, price)
    for artist_id, albums in zip(artist_ids, ALBUMS_PER_ARTIST):
        for title, rel_date, price in albums:
            DB.execute(
                "INSERT INTO albums (title, artist_id, release_date, price) "
                "VALUES (%s, %s, %s, %s) RETURNING album_id",
                (title, artist_id, rel_date, price),
            )
            album_rows.append((DB.fetchone()[0], price))
    print(f"Inserted {len(album_rows)} albums")

    # ── sales (randomised) ───────────────────────────────────────────
    random.seed(42)
    sale_count = 0
    start = date(2022, 1, 1)
    end = date(2024, 6, 30)
    delta_days = (end - start).days

    for album_id, price in album_rows:
        num_sales = random.randint(30, 200)
        for _ in range(num_sales):
            sale_date = start + timedelta(days=random.randint(0, delta_days))
            qty = random.randint(1, 5)
            total = round(qty * price, 2)
            DB.execute(
                "INSERT INTO sales (album_id, sale_date, quantity, total_amount) "
                "VALUES (%s, %s, %s, %s)",
                (album_id, sale_date, qty, total),
            )
            sale_count += 1
    print(f"Inserted {sale_count} sales records")

    DB.close()
    DB_CONNECTION.close()
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed()
