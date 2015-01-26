from flask import Flask
from flask import render_template
from xml.etree import ElementTree
from xml.sax import saxutils
import requests

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
        text = saxutils.unescape(line.find('text').text)
        return render_template('index.html', status="Nope", text=text)

if __name__ == "__main__":
    application.run(debug=True)
