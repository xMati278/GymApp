import environ

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'default-secret-key'),
    ENV=(str, 'dev'),
    DB=(str, 'sqlite'),
)
