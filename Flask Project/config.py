class Config(object):
    # Base Config
    DEBUG = True

    SECRET_KEY = "BiGGiEsmaLLz555313555baCKaTiTaGaIN222"

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = "jsalemfinancial@gmail.com"
    MAIL_USERNAME = "jsalemfinancial@gmail.com"
    MAIL_PASSWORD = "wyippenjjvthffjg"

    DB_CONFIG = {"host": "flaskdb-001.cmtvzzpoedvj.us-east-2.rds.amazonaws.com", "port": "5050", "user": "flaskadmin", "password": "flasklover", "database": "flaskDB"}