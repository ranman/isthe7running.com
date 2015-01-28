from flask import Flask
from flask import render_template
from xml.etree import ElementTree
from xml.sax import saxutils
import requests
import requests_cache
requests_cache.install_cache('mta_cache', expire_after=120)

data_url = "http://web.mta.info/status/serviceStatus.txt"
application = Flask(__name__)


@application.route('/')
def index():
    resp = requests.get(data_url)
    tree = ElementTree.fromstring(resp.content)
    line = tree.find("./subway/line[name='7']")
    status = line.find('status').text
    if status == "GOOD SERVICE":
        return render_template('index.html', status="Yes")
    else:
        status_text = "Nope."
        text = saxutils.unescape(line.find('text').text)
        if status == "SERVICE CHANGE":
            status_text = "Maybe?"
        return render_template('index.html', status=status_text, text=text)

if __name__ == "__main__":
    application.run(debug=True)
