from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(message='Обязательное поле'),
        Length(min=3, max=80, message='От 3 до 80 символов')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Обязательное поле'),
        Email(message='Введите корректный email')
    ])
    first_name = StringField('Имя', validators=[Optional()])
    last_name = StringField('Фамилия', validators=[Optional()])
    phone = StringField('Телефон', validators=[Optional()])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Обязательное поле'),
        Length(min=6, message='Минимум 6 символов')
    ])
    password2 = PasswordField('Подтвердите пароль', validators=[
        DataRequired(message='Обязательное поле'),
        EqualTo('password', message='Пароли не совпадают')
    ])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(message='Обязательное поле')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Обязательное поле')])
    submit = SubmitField('Войти')


class ProfileForm(FlaskForm):
    first_name = StringField('Имя', validators=[Optional()])
    last_name = StringField('Фамилия', validators=[Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[Optional()])
    address = StringField('Адрес доставки', validators=[Optional()])
    submit = SubmitField('Сохранить')


class OrderForm(FlaskForm):
    shipping_address = TextAreaField('Адрес доставки', validators=[
        DataRequired(message='Укажите адрес доставки')
    ])
    shipping_city = StringField('Город', validators=[DataRequired(message='Укажите город')])
    shipping_phone = StringField('Контактный телефон', validators=[DataRequired(message='Укажите телефон')])
    comment = TextAreaField('Комментарий к заказу', validators=[Optional()])
    submit = SubmitField('Оформить заказ')


class ReviewForm(FlaskForm):
    user_name = StringField('Ваше имя', validators=[DataRequired(message='Укажите имя')])
    rating = SelectField('Оценка', choices=[
        ('5', 'Отлично - 5'),
        ('4', 'Хорошо - 4'),
        ('3', 'Удовлетворительно - 3'),
        ('2', 'Плохо - 2'),
        ('1', 'Ужасно - 1')
    ], validators=[DataRequired()])
    text = TextAreaField('Отзыв', validators=[DataRequired(message='Напишите отзыв')])
    submit = SubmitField('Отправить отзыв')


class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    slug = StringField('URL-идентификатор', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[Optional()])
    price = FloatField('Цена', validators=[DataRequired(), NumberRange(min=0)])
    old_price = FloatField('Старая цена', validators=[Optional(), NumberRange(min=0)])
    stock = IntegerField('Количество на складе', validators=[DataRequired(), NumberRange(min=0)], default=0)
    material = StringField('Материал', validators=[Optional()])
    dimensions = StringField('Размеры', validators=[Optional()])
    color = StringField('Цвет', validators=[Optional()])
    weight = FloatField('Вес (кг)', validators=[Optional(), NumberRange(min=0)])
    category_id = SelectField('Категория', coerce=int, validators=[DataRequired()])
    is_featured = BooleanField('Рекомендуемый товар')
    is_active = BooleanField('Активен', default=True)
    submit = SubmitField('Сохранить')
