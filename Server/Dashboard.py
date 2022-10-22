from flask import Flask
import KeySearch
import NewsTable

app = Flask(__name__)


@app.route("/dashboard")
# 主畫面
def Dashboard():
    return {
        "KeySearch": KeySearch.KeySearch(),
        "NewsTable": NewsTable.NewsTable()
    }


if __name__ == "__main__":
    app.run(debug=True)
