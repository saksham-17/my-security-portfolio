from flask import Flask, render_template, jsonify
from flask_cors import CORS
import feedparser
import time

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# --- CONFIGURATION ---
# We use RSS feeds because they are reliable and don't require complex API keys for a starter project.
RSS_FEEDS = {
    "news": "https://feeds.feedburner.com/TheHackersNews",
    "cisa": "https://www.cisa.gov/uscert/ncas/alerts.xml" # Official US Cert Alerts
}

def parse_feed(url, source_name):
    """Fetches and parses an RSS feed."""
    try:
        feed = feedparser.parse(url)
        data = []
        # Get the top 5 entries
        for entry in feed.entries[:5]:
            data.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", "N/A"),
                "source": source_name
            })
        return data
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")
        return []

@app.route('/')
def home():
    """Serves the dashboard HTML page."""
    return render_template('dashboard.html')

@app.route('/api/updates')
def get_updates():
    """API Endpoint: Returns combined data from all sources."""
    news_data = parse_feed(RSS_FEEDS["news"], "The Hacker News")
    threat_data = parse_feed(RSS_FEEDS["cisa"], "CISA Alerts")
    
    return jsonify({
        "news": news_data,
        "threats": threat_data,
        "timestamp": time.strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    print(">> SOC Dashboard is running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)