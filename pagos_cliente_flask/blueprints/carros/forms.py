"""
Carros, formularios
"""
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import BooleanField, EmailField, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class IngresarForm(FlaskForm):
    """Formulario para ingresar datos personales"""

    cantidad = HiddenField("Cantidad")
    pag_tramite_servicio_clave = HiddenField("Clave del trámite o servicio")
    autoridad_clave = HiddenField("Clave de la autoridad")
    nombres = StringField(
        "Nombres",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    apellido_primero = StringField(
        "Primer apellido",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    apellido_segundo = StringField(
        "Segundo apellido",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    curp = StringField(
        "CURP",
        validators=[DataRequired(), Length(min=18, max=18)],
        render_kw={"placeholder": "18 caracteres"},
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Length(min=3, max=128)],
    )
    telefono = StringField(
        "Telefono celular",
        validators=[DataRequired(), Length(min=10, max=10)],
        render_kw={"placeholder": "10 dígitos sin espacios ni guiones"},
    )
    recaptcha = RecaptchaField()
    aceptar = BooleanField(
        "He leído y acepto el <a href='/aviso' class='nav-link link-aviso'>Aviso de Privacidad</a>",
        validators=[DataRequired()],
    )
    continuar = SubmitField("Continuar")
