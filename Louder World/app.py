from flask import Flask, render_template, request, redirect
import sqlite3
from scraper import scrape_events  # Import the scraping function
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Call the scraping function to initialize the database
scrape_events()

# Schedule the scraping function to run every 24 hours
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_events, 'interval', hours=24)
scheduler.start()

@app.route('/')
def index():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events')
    events = c.fetchall()
    conn.close()
    return render_template('index.html', events=events)  # Ensure this is 'index.html'

@app.route('/get-ticket', methods=['POST'])
def get_tickets():
    email = request.form['email']
    event_link = request.form['event_link']
    # Here you can add email opt-in logic
    # Redirect to the original event link
    return redirect(event_link)

if __name__ == "__main__":
    app.run(debug=True)