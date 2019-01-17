import os
from flask import Flask, render_template
from CloudFlare import CloudFlare

PREFIX = '.novell.mause.me'

cf = CloudFlare(
    'me@mause.me',
    os.environ.get('CF_KEY')
)
zone = next(
    zone['id']
    for zone in cf.zones.get()
    if zone['name'] == 'mause.me'
)
app = Flask(__name__)


@app.route('/')
def index():
    records = cf.zones.dns_records.get(zone)
    records = [record['name'] for record in records]
    records = {
        record.replace(PREFIX, ''): record
        for record in records
        if record.endswith(PREFIX)
    }
    return render_template('index.html', records=records)


if __name__ == '__main__':
    app.run(debug=True)

