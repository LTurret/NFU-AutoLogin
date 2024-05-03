# NFU-AutoLogin

A Python script designed for user authentication on [identity.nfu.edu.tw](https://ulearn.nfu.edu.tw/) without solving captcha

## Directory Structure

```plain
.env
src/
├── fetch_util.py
├── main.py
├── model.py
└── validator.py
```

## Requirements

### Packages

Install packages via requirements.txt

#### Windows

```shell
pip install -r requirements.txt
```

#### macOS

```shell
pip install -r requirements_intel-macos.txt
```

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
