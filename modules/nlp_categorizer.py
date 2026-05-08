"""Módulo de categorización NLP — clasifica comentarios y detecta errores probables."""

from data.base_conocimiento import KNOWLEDGE_BASE

CATEGORIAS_KEYWORDS = {
    "Consulte mi saldo": ["saldo", "balance", "cuánto tengo", "valor cuenta", "cuanto tengo", "ver saldo"],
    "Solicité un retiro": ["retiro", "retirar", "sacar dinero", "desembolso", "solicite retiro", "hacer retiro"],
    "Realicé un aporte": ["aporte", "consignar", "depositar", "inversión", "inversion", "cotización", "cotizacion"],
    "Gestioné mi portafolio": ["portafolio", "fondos", "cambio de fondo", "reasignación", "reasignacion", "portafolio de inversión"],
    "Consulté mi información": ["información", "informacion", "datos", "contrato", "estado cuenta", "mi perfil"],
    "Consulté documentos/certificados": ["certificado", "extracto", "documento", "constancia", "certificacion"],
    "Actualicé mis datos": ["actualizar", "cambiar datos", "teléfono", "telefono", "dirección", "direccion", "correo", "actualice"],
    "Certifiqué mis aportes": ["certificación", "certificacion", "certificar", "retención en la fuente", "retencion"],
    "Registros de cuentas bancarias": ["cuenta", "banco", "inscribir", "registrar cuenta", "cuenta bancaria", "inscripcion"],
}

ERROR_KEYWORDS = {
    "ERR001": ["cuenta activa", "ya inscrita", "cuenta registrada", "no puedo inscribir cuenta"],
    "ERR002": ["fondos insuficientes", "no tengo saldo", "saldo insuficiente", "no alcanza"],
    "ERR003": ["perfil", "portafolio bloqueado", "perfil vencido", "actualizar perfil"],
    "ERR004": ["no puedo actualizar", "datos no cambian", "actualización rechazada"],
    "ERR005": ["no carga", "error al descargar", "certificado no descarga", "timeout", "se cayó"],
    "ERR006": ["límite diario", "limite diario", "no acepta aporte", "monto máximo"],
    "ERR007": ["saldo no actualiza", "saldo desactualizado", "no refresca"],
    "ERR008": ["sesión expirada", "sesion expirada", "cerró sesión", "volvió a pedir contraseña"],
    "ERR009": ["bloqueado", "no puedo inscribir", "cuenta rechazada", "sarlaft"],
    "ERR010": ["periodo", "no disponible", "plazo fijo", "bloqueo de fondo"],
    "ERR011": ["firma", "firma electrónica", "firma electronica", "cambio de perfil no guarda"],
    "ERR012": ["certificado no disponible", "año en curso", "periodo fiscal"],
    "ERR013": ["contraseña incorrecta", "bloqueado portal", "no puedo ingresar", "olvidé contraseña"],
    "ERR014": ["fraude", "acceso extraño", "dispositivo desconocido", "alerta seguridad"],
    "ERR015": ["error 500", "portal no carga", "pantalla blanca", "fallo técnico"],
    "ERR016": ["documento no encontrado", "usuario no existe", "no me reconoce"],
    "ERR017": ["código no llega", "otp no llega", "no recibo código", "código de verificación"],
}


def clasificar_transaccion(comentario: str) -> str:
    """Clasifica un comentario en una categoría de transacción oficial."""
    texto = comentario.lower()
    scores = {}
    for categoria, keywords in CATEGORIAS_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in texto)
        if score > 0:
            scores[categoria] = score
    if scores:
        return max(scores, key=scores.get)
    return "Otras"


def detectar_error_probable(comentario: str, categoria: str = "") -> dict:
    """Detecta el error más probable dado un comentario y categoría."""
    texto = (comentario + " " + categoria).lower()
    scores = {}
    for err_id, keywords in ERROR_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in texto)
        if score > 0:
            scores[err_id] = score
    if scores:
        best = max(scores, key=scores.get)
        total = sum(scores.values())
        confianza = round(scores[best] / max(total, 1), 2)
        return {"error_id": best, "confianza": min(confianza + 0.6, 0.97), "datos": KNOWLEDGE_BASE.get(best, {})}
    return {"error_id": None, "confianza": 0, "datos": {}}


def analizar_sentimiento_tono(comentario: str) -> dict:
    """Analiza el tono emocional del comentario."""
    texto = comentario.lower()
    frustracion_kw = ["no funciona", "no puedo", "llevo días", "imposible", "pésimo", "terrible", "error", "problema", "bloqueado"]
    urgencia_kw = ["urgente", "necesito ya", "inmediatamente", "hoy", "ahora", "rápido"]
    positivo_kw = ["gracias", "excelente", "muy bien", "perfecto", "rápido", "fácil", "satisfecho"]

    frst = sum(1 for kw in frustracion_kw if kw in texto)
    urg = sum(1 for kw in urgencia_kw if kw in texto)
    pos = sum(1 for kw in positivo_kw if kw in texto)

    if pos > frst:
        tono = "Positivo 😊"
        color = "green"
    elif frst >= 2 or urg >= 1:
        tono = "Frustrado / Urgente 😤"
        color = "red"
    elif frst == 1:
        tono = "Insatisfecho 😕"
        color = "orange"
    else:
        tono = "Neutro 😐"
        color = "gray"

    return {"tono": tono, "color": color, "frustracion": frst, "urgencia": urg}
