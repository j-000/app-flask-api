DEVELOPMENT = True
# # email credentials
MAIL_USERNAME =''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER =''

SQLALCHEMY_TRACK_MODIFICATIONS = False 
SECRET_KEY ='sdasiodaifqcXvLHzs6uAEfcFAEdzrwdaifqcXvLHzs6uAEfcFAEdzrwdjafqcXvLHzs6uAEfcFAEdzrwoidsj'
SECURITY_PASSWORD_SALT = 'cXvLHzs6uAEfcFAEdzrwdjafqcXvLHzs6uAcXvLHzs6uAEfcFAEdzrwdjafqcXvLHzs6uAcXv'
#################################################################
''' Database '''
##################################################################
URI = ''
PORT = ''
USER = ''
SECRET = ''
NAME = ''

if DEVELOPMENT:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
else:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'.format(
    user=USER, password=SECRET, host=URI, port=PORT, dbname=NAME)
