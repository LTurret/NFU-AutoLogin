# NFU-AutoLogin

A Python script designed for user authentication on [identity.nfu.edu.tw](https://ulearn.nfu.edu.tw/) without solving captcha

## Limitation

> [!IMPORTANT]  
> The current online OCR token is complimentary and directly integrated into the program. However, due to the daily limit of 500 uses imposed by this free API, there may be instances when the token is exhausted. Rest assured, you can replace the token yourself without any issues.

## Directory Structure

```plain
.env
src/
└── main.py
```

## Build

### Requirements

Install packages via
`pip install -r requirements.txt`

### Confidentials

Create a `.env` to keep your secrets

```.env
nfu_username=
nfu_password=
```

### Running

```shell
python3 -B main.py
```

## License

Licensed under [MIT](LICENSE)
