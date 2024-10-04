CONFIRMATION_CODE_LENGTH = 6
MAX_BIO_LENGTH = 256
MAX_EMAIL_LENGTH = 254
MAX_NAME_LENGTH = 256
MAX_SLUG_LENGTH = 50
MAX_STR_LENGTH = 15
MAX_TEXT_LENGTH = 1000
MAX_USERNAME_LENGTH = 150
MIN_SCORE = 1
MAX_SCORE = 10

USERNAME_REGEX = r'^[\w.@+-]+\Z'
USERNAMES_BLACKLIST = ['me']

USERNAME_REGEX_ERROR_MESSAGE = 'Запрещено использовать это имя!'
USERNAME_ERROR_MESSAGE = 'Такой пользователь уже зарегистрирован!'
USER_ALREADY_REVIEWED_MESSAGE = 'Вы уже оставляли отзыв к этому произведению!'
TOKEN_ERROR_MESSAGE = {'confirmation_code': 'Неверный код подтверждения!'}

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
CHOICES = (
    (USER, 'обычный'),
    (MODERATOR, 'модератор'),
    (ADMIN, 'администратор')
)

SUBJECT = 'Код подтверждения'
FROM_EMAIL = 'example@ex.ru'
