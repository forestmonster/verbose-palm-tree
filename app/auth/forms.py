from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, numbers, dots or underscores.",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Passwords must match."),
        ],
    )
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("E-mail already registered.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")


class PasswordUpdateForm(FlaskForm):
    """Allow user to update their password."""

    old_password = PasswordField("Current password", validators=[DataRequired()])
    new_password = PasswordField("New password", validators=[DataRequired()])
    new_password2 = PasswordField(
        "Retype new password to confirm",
        validators=[
            DataRequired(),
            EqualTo("new_password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Confirm password change")


class PasswordResetRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField("Reset Password")


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Passwords must match"),
        ],
    )
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Reset Password")


class ChangeEmailForm(FlaskForm):
    email = StringField(
        "New E-mail", validators=[DataRequired(), Length(1, 64), Email()]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Update E-mail Address")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("E-mail already registered.")
