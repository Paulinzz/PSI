from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp

from models.user import User


class RegistrationForm(FlaskForm):
    userename = StringField('Nome de usuário', 
            validators=[
                DataRequired(message="O nome de usuário é obrigatório."),
                Length(min=3, max=25, message="O nome de usuário deve ter entre 3 e 25 caracteres."),
                Regexp(r'^[\w ]+$', message="O nome de usuário só pode conter letras, números e sublinhados.")
            ],

        render_kw={"placeholder": "Nome de usuário"}
    )

    email = StringField('Email',
            validators=[
                DataRequired(message="O email é obrigatório."),
                Email(message="Endereço de email inválido."),
                Length(max=50, message="O email deve ter no máximo 120 caracteres.")
            ],

        render_kw={"placeholder": "Email"}
    )

    password = PasswordField('Senha',
            validators=[
                DataRequired(message="A senha é obrigatória."),
                Length(min=6, message="A senha deve ter no mínimo 6 caracteres.")
            ],

            render_kw={"placeholder": "Senha"}
    )

    confirm_password = PasswordField('Confirme a Senha',
            validators=[
                DataRequired(message="A confirmação de senha é obrigatória."),
                EqualTo('password', message="As senhas devem corresponder.")
            ],

            render_kw={"placeholder": "Confirme a Senha"}
    )

    submit = SubmitField('Registrar')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')
        
    
class LoginForm(FlaskForm):
    username = StringField('Nome de usuário',
            validators=[DataRequired(message="O nome de usuário é obrigatório.")],

            render_kw={"placeholder": "Nome de usuário"}
    )


    password = PasswordField('Senha',
            validators=[DataRequired(message="A senha é obrigatória.")],

            render_kw={"placeholder": "Senha"}
    )

    remember = BooleanField('Lembrar de mim')

    submit = SubmitField('Entrar')
