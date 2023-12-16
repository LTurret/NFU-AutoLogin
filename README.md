# NFU-AutoLogin

A Python script designed for user authentication on [identity.nfu.edu.tw](https://ulearn.nfu.edu.tw/) without solving captcha

## Directory Structure

```plain
src/
├── .env
├── login.py
└── main.py
```

## Build

### Requirements

Install packages via
`pip install -r requirements.txt`

### .env

Create a enviornment variables for keep your secrets

```.env
username=
password=
```

### Running

```shell
python3 -B main.py
```

## License

Licensed under [MIT](LICENSE)
