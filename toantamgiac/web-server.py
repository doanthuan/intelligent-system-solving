from flask import Flask, render_template
from suydien.tgsdt_caitien import *

app = Flask(__name__, template_folder="templates", static_folder='static', static_url_path='')


@app.route("/")
def index():
    inDangThuc = TapDangThuc_latex
    inGiaThiet = GiaThuyet_latex
    inKetLuan_ = KetLuan_latex

    inBuocGiai_ = buocGiai_latex
    inGiaThiet_new = giaThuyet_new_latex
    return render_template("index.html", dtlatex=inDangThuc, gtlatex=inGiaThiet, kllatex=inKetLuan_,
                           bglatex=inBuocGiai_, gtnlatex=inGiaThiet_new)


app.run(debug=True)
