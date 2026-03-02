from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Registrarse")

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar Sesión")

class PostForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired()])
    content = TextAreaField("Contenido", validators=[DataRequired()])
    image = FileField("Imagen")
    submit = SubmitField("Publicar")

class CommentForm(FlaskForm):
    content = TextAreaField("Comentario", validators=[DataRequired()])
    submit = SubmitField("Comentar")