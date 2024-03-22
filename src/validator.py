from os import path


def validator(secrets: tuple, model: str) -> bool:
    if not path.isfile(model):
        raise FileNotFoundError('"src/model.pkl" is not found!')

    if any(map(lambda credentials: credentials is None, secrets)):
        raise ValueError(
            'The provided secrets do not meet the required criteria. Please check your ".env" file and ensure it follows the correct format. For example, SECRET_KEY="YourSecretKey".'
        )

    secrets = None

    return True
