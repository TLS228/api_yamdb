MAX_STR_LENGTH = 15
MAX_USERNAME_LENGTH = 150
MAX_EMAIL_LENGTH = 254
MAX_PASSWORD_LENGTH = 128
MAX_BIO_LENGTH = 256
MAX_NAME_LENGTH = 256
MAX_SLUG_LENGTH = 50
MAX_TEXT_LENGTH = 1000
MIN_SCORE = 1
MAX_SCORE = 10
CONFIRMATION_CODE_LENGTH = 6
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
CHOICES = (
    (USER, 'обычный'),
    (MODERATOR, 'модератор'),
    (ADMIN, 'администратор')
)
USERNAME_REGEX_ERROR_MESSAGE = 'Запрещено использовать это имя!'
USERNAME_ERROR_MESSAGE = 'Пользователь с таким именем уже существует.'
USERNAME_REGEX = r'^[\w.@+-]+\Z'
