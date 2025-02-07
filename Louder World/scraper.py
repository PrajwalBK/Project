import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_events():
    url = "https://example.com/events/sydney"  # Replace with actual event website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    events = []
    for event in soup.find_all('div', class_='event'):
        title = event.find('h2').text
        date = event.find('span', class_='date').text
        link = event.find('a')['href']
        events.append((title, date, link))

    # Store events in SQLite database
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS events (title TEXT, date TEXT, link TEXT)')
    c.execute('DELETE FROM events')  # Clear old events
    c.executemany('INSERT INTO events VALUES (?, ?, ?)', events)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    scrape_events()