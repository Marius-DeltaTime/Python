import requests
import sqlite3
import time

def FetchAndStoreData():
    # Start timing
    start_time = time.time()

    # Retrieve data
    url = "https://deckofcardsapi.com/api/deck/new/draw/?count=52"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return

    # Create db and connect
    conn = sqlite3.connect('cards.db')
    cursor = conn.cursor()

    # Table to hold card data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY,
        deck_id TEXT,
        code TEXT,
        image TEXT,
        svg TEXT,
        png TEXT,
        value TEXT,
        suit TEXT
    )
    ''')

    # Insert into table
    deck_id = data['deck_id']
    cards = data['cards']

    for card in cards:
        cursor.execute('''
        INSERT INTO cards (deck_id, code, image, svg, png, value, suit)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (deck_id, card['code'], card['image'], card['images']['svg'], card['images']['png'], card['value'], card['suit']))

    # Commit
    conn.commit()

    # Close connection
    conn.close()

    # End timing
    end_time = time.time()
    duration = end_time - start_time
    print(f"Data has been successfully imported into the SQLite database in {duration:.2f} seconds.")

if __name__ == "__main__":
    FetchAndStoreData()
