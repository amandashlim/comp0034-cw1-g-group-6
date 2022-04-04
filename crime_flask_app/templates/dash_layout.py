import codecs
from pathlib import Path

filepath = Path(__file__).parent.joinpath("dashboard.html" )
f = codecs.open(filepath,"r")

html_layout = f.read()