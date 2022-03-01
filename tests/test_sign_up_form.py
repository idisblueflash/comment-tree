from hamcrest import *

from app.api.forms import SignUpForm, CommentForm


class TestSignUpForm:
    USERNAME = 'flash1978'
    PASSWORD = 'Flash&password123'
    EMAIL = 'flash@email.com'

    CORRECT_DATA = {
        'username': USERNAME,
        'password': PASSWORD,
        'email': EMAIL
    }

    MISSING_USERNAME_DATA = {'password': PASSWORD, 'email': EMAIL}
    MISSING_PASSWORD_DATA = {'username': USERNAME, 'email': EMAIL}

    def validate_form_with_data(self, app, data):
        with app.app_context():
            form = SignUpForm(**data, meta={'csrf': False})
            return form.validate(), form.errors

    def test_username_exist(self, app):
        data = self.CORRECT_DATA
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(errors, equal_to({}))
        assert_that(flag, equal_to(True))

    def test_username_missing_with_message(self, app):
        flag, errors = self.validate_form_with_data(app, self.MISSING_USERNAME_DATA)
        assert_that(errors, equal_to({'username': ['This field is required.']}))

    def test_username_mix_length(self, app):
        data = {**self.MISSING_USERNAME_DATA,
                'username': '123a'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(errors.get('username'), equal_to(['Field must be between 5 and 20 characters long.']))

    def test_username_max_length(self, app):
        data = {**self.MISSING_USERNAME_DATA,
                'username': '12345678901234567890a'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(errors.get('username'), equal_to(['Field must be between 5 and 20 characters long.']))

    def test_username_alphabet_only(self, app):
        data = {**self.MISSING_USERNAME_DATA,
                'username': '12-4a'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(errors.get('username'),
                    equal_to(['Username must contain LowerCase, UpperCase alphabets or numbers']))

    def test_password_missing(self, app):
        data = self.MISSING_PASSWORD_DATA
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(flag, equal_to(False))

    def test_password_min_length(self, app):
        data = {**self.MISSING_PASSWORD_DATA,
                'password': '1234567'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(flag, equal_to(False))

    def test_password_max_length(self, app):
        data = {**self.MISSING_PASSWORD_DATA,
                'password': '12345678901234567890a'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(flag, equal_to(False))

    def test_password_without_upper_case(self, app):
        data = {**self.MISSING_PASSWORD_DATA,
                'password': '1234567890'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(flag, equal_to(False))

    def test_password_without_lower_case(self, app):
        data = {**self.MISSING_PASSWORD_DATA,
                'password': '1234567890'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(flag, equal_to(False))

    def test_password_without_number(self, app):
        data = {**self.MISSING_PASSWORD_DATA,
                'password': 'abcdEFGH'}
        flag, errors = self.validate_form_with_data(app, data)
        print(f'DEBUG: errors={errors}')
        assert_that(flag, equal_to(False))

    def test_password_without_special_char(self, app):
        data = {**self.MISSING_PASSWORD_DATA,
                'password': 'abcdEFGH'}
        flag, errors = self.validate_form_with_data(app, data)
        print(f'DEBUG: errors={errors}')
        assert_that(flag, equal_to(False))

    def test_email_missing(self, app):
        data = {'username': 'flash', 'password': 'flash-password'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(flag, equal_to(False))

    def tests_wrong_email(self, app):
        data = {'username': 'flash', 'password': 'flash-password',
                'email': 'flash.com'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(flag, equal_to(False))


class TestCommentForm:
    def validate_form_with_data(self, app, data=None):
        if data is None:
            data = {}
        with app.app_context():
            form = CommentForm(**data, meta={'csrf': False})
            flag = form.validate()
            errors = form.errors
            app.logger.error(f'errors={errors}, validate={flag}')
            return flag, errors

    def test_message_min_length(self, app):
        data = {'message': '12'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(errors['message'], equal_to(['Field must be between 3 and 200 characters long.']))

    def test_message_max_length(self, app):
        data = {'message': 'Third-most populous as and much flare that many statues were '
                           'painted in a counterclockwise and much flare that many statues were '
                           'painted in a counterclockwise populous as and much flare that many foxes'}
        print(f'DEBUG: len={len(data["message"])}')
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(errors['message'], equal_to(['Field must be between 3 and 200 characters long.']))

    def test_message_mix_length_cn(self, app):
        data = {'message': '國力'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(errors['message'], equal_to(['Field must be between 3 and 200 characters long.']))

    def test_message_max_length_cn(self, app):
        data = {'message': '國力鄉來去設家充表無香母多任辦錢正巴多然灣教陽，思突了的他你這，金子里意改出國當課，'
                           '界一運花已東後注接點但是推綠都民港比，話非地了下族就國小爭千的說細使學流物，'
                           '名唱臺達漸小家值局車在備要比影上來基容方是家學。事部決人校票，力量明表小國化果取會智為天冷多，'
                           '銷合氣大一民以養臺代公國教位的學合以物親說名語這是方是，布著一操界時成，'
                           '究機可知原念傳此社經設念級陽論爸許。母叫什，文市的，就多願是主回人地和世，登數差為不去參想；'}
        flag, errors = self.validate_form_with_data(app, data)
        assert_that(errors['message'], equal_to(['Field must be between 3 and 200 characters long.']))

    def test_user_id(self, app):
        flag, errors = self.validate_form_with_data(app)
        assert_that(errors['user_id'], equal_to(['This field is required.']))

    def test_timestamp(self, app):
        flag, errors = self.validate_form_with_data(app)
        assert_that(errors['timestamp'], equal_to(['This field is required.']))
