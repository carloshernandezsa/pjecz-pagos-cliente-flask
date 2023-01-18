"""
Resultados, vistas
"""
from flask import abort, Blueprint, render_template, request, redirect, url_for
import requests

from config.settings import API_BASE_URL, API_TIMEOUT

resultados = Blueprint("resultados", __name__, template_folder="templates")


@resultados.route("/resultado", methods=["GET", "POST"])
def procesar_lo_que_viene_del_banco():
    """Procesar lo que viene del banco"""
    # pendiente

    # Si no viene el payload del banco por POST
    if not request.form:
        abort(400, "No se ha proporcionado el payload del banco.")
    if request.form["strResponse"] == "":
        abort(400, "No se ha proporcionado el payload del banco.")

    # Preparar el cuerpo a enviar a la API "/pag_pagos/resultado"
    request_body = {
        "xml_encriptado": request.form["strResponse"],
    }

    # Enviar al API, donde se actualizará el pago
    try:
        respuesta = requests.post(
            f"{API_BASE_URL}/pag_pagos/resultado",
            json=request_body,
            timeout=API_TIMEOUT,
        )
    except requests.exceptions.ConnectionError as error:
        abort(500, "No se pudo conectar con la API de pagos. " + str(error))
    except requests.exceptions.Timeout as error:
        abort(500, "Tiempo de espera agotado al conectar con la API de pagos. " + str(error))
    except requests.exceptions.RequestException as error:
        abort(500, "Error desconocido con la API de pagos. " + str(error))
    datos = respuesta.json()
    if "estado" not in datos or "folio" not in datos:
        abort(500, "No se pudo terminar el proceso de pago.")

    # Redirigir a la página de resultado PAGADO
    if datos["estado"] == "PAGADO":
        return redirect(url_for("resultados.resultado_pagado"))

    # De lo contrario, el reultado es FALLIDO
    return redirect(url_for("resultados.resultado_fallido"))


@resultados.route("/resultado/pagado", methods=["GET", "POST"])
def resultado_pagado():
    """Resultado pagado"""

    # Entregar
    return render_template("resultados/pagado.jinja2")


@resultados.route("/resultado/fallido", methods=["GET", "POST"])
def resultado_fallido():
    """Resultado fallido"""

    # Entregar
    return render_template("resultados/fallido.jinja2")
