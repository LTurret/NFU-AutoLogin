import easyocr

from login import login

reader = easyocr.Reader(["en"], gpu=True)

while True:
    try:
        login(reader)
        break
    except:
        pass
