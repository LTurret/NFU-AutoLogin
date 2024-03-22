from easyocr import Reader
from pickle import dump

reader: Reader = Reader(["en"], gpu=True)

with open("model.pkl", "wb") as model:
    dump(reader, model)
