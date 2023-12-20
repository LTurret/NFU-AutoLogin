# NFU-AutoLogin

A Python script designed for user authentication on [identity.nfu.edu.tw](https://ulearn.nfu.edu.tw/) without solving captcha

## Directory Structure

```plain
.env
model.pkl
src/
├── model.py
└── main.py
```

## Requirements

### Packages

Install packages via
`pip install -r requirements.txt`

### Secrets

Create a `.env` to keep your secrets

```.env
nfu_username=
nfu_password=
```

### Model

To use OCR for detect captcha, you need to run `./src/model.py` to generate the `model.pkl`

## Running

```shell
python3 -B ./src/main.py
```

## License

Licensed under [MIT](LICENSE)
