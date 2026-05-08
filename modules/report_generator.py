"""Generador de informes técnicos y tickets de escalamiento."""

import datetime
import streamlit as st


def generar_informe_tecnico(ss) -> str:
    """Genera el informe técnico completo del caso."""
    cliente = ss.get("cliente_activo", {})
    error = ss.get("error_activo", {})
    log = ss.get("chatbot_log", [])
    pasos = ss.get("chatbot_pasos_completados", [])
    modulo = ss.get("modulo_origen", "Desconocido")
    ts = ss.get("timestamp_inicio", datetime.datetime.now())

    lineas_log = "\n".join([f"  [{e['hora']}] {e['accion']}" for e in log])
    lineas_pasos = ""
    if error and "datos" in error and "solucion_ia" in error.get("datos", {}):
        for i, paso in enumerate(error["datos"]["solucion_ia"]):
            estado = "✓ Completado" if i in pasos else "✗ No resuelto"
            lineas_pasos += f"  [{estado}] Paso {i+1}: {paso}\n"

    informe = f"""
╔══════════════════════════════════════════════════════════════╗
║           INFORME TÉCNICO DE CASO — SKANDIA PORTAL           ║
╠══════════════════════════════════════════════════════════════╣

DATOS DEL EVENTO
─────────────────
Fecha y hora del evento : {ts.strftime('%d/%m/%Y %H:%M:%S')}
Módulo donde ocurrió    : {modulo}
Error identificado      : {error.get('error_id','N/A')} — {error.get('datos',{}).get('titulo','N/A')}
Categoría               : {error.get('datos',{}).get('categoria','N/A')}

DATOS DEL CLIENTE
─────────────────
Nombre        : {cliente.get('nombre','N/A')}
Documento     : {cliente.get('documento','N/A')}
Contrato      : {cliente.get('contrato','N/A')}
Email         : {cliente.get('email','N/A')}
Teléfono      : {cliente.get('telefono','N/A')}
FP Asignado   : {cliente.get('fp_id','N/A')}

ACCIONES REALIZADAS POR AGENTE IA
──────────────────────────────────
{lineas_pasos if lineas_pasos else '  Sin acciones registradas'}

LOG DETALLADO DE EXPERIENCIA
─────────────────────────────
{lineas_log if lineas_log else '  Sin log disponible'}

ESTADO ACTUAL
─────────────
{"Escalado a técnico — Pendiente resolución" if ss.get('tecnico_conectado') else "En proceso con Agente IA"}

══════════════════════════════════════════════════════════════
Generado automáticamente por el Sistema de Soporte Skandia
{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
══════════════════════════════════════════════════════════════
"""
    return informe


def generar_ticket_escalamiento(ss, acciones_tecnico: list = None) -> dict:
    """Genera el ticket de escalamiento a mesa de ayuda."""
    import random
    ticket_num = f"TICK-2026-{random.randint(1000, 9999)}"
    cliente = ss.get("cliente_activo", {})
    error = ss.get("error_activo", {})

    acciones_txt = ""
    if acciones_tecnico:
        for a in acciones_tecnico:
            acciones_txt += f"  [{a.get('hora','--:--')}] {a.get('accion','')}\n"

    ticket = {
        "numero": ticket_num,
        "fecha_creacion": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "cliente_nombre": cliente.get("nombre", "N/A"),
        "cliente_contrato": cliente.get("contrato", "N/A"),
        "cliente_email": cliente.get("email", "N/A"),
        "error_id": error.get("error_id", "N/A"),
        "error_titulo": error.get("datos", {}).get("titulo", "N/A"),
        "modulo": ss.get("modulo_origen", "N/A"),
        "estado": "ESCALADO — PENDIENTE MESA DE AYUDA",
        "sla": "4 horas hábiles",
        "informe_completo": generar_informe_tecnico(ss),
        "acciones_tecnico": acciones_txt,
    }
    return ticket


def simular_correos(ticket: dict, fp_info: dict, agente_info: dict) -> list:
    """Genera los correos simulados que se enviarían."""
    correos = [
        {
            "destinatario": ticket["cliente_email"],
            "asunto": f"Caso escalado — Ticket {ticket['numero']} | Skandia",
            "cuerpo": f"""Estimado/a {ticket['cliente_nombre']},

Tu caso ha sido escalado a nuestra Mesa de Ayuda Especializada con el número de ticket {ticket['numero']}.

📋 Detalle del caso:
• Módulo: {ticket['modulo']}
• Inconveniente: {ticket['error_titulo']}
• Fecha: {ticket['fecha_creacion']}

⏱ Recibirás respuesta en un máximo de {ticket['sla']}.
Tu Financial Planner también fue notificado y hará seguimiento de tu caso.

Gracias por tu paciencia.
Equipo Skandia""",
        },
        {
            "destinatario": fp_info.get("email", "fp@skandia.com"),
            "asunto": f"[FP] Caso escalado — Cliente {ticket['cliente_nombre']} | {ticket['numero']}",
            "cuerpo": f"""Hola {fp_info.get('nombre','')},

Te notificamos que el caso de tu cliente fue escalado a la Mesa de Ayuda.

👤 Cliente: {ticket['cliente_nombre']} | Contrato: {ticket['cliente_contrato']}
🔴 Error: {ticket['error_titulo']}
🎫 Ticket: {ticket['numero']}

Por favor realiza seguimiento con el cliente y con la mesa de ayuda.

Sistema de Soporte Skandia""",
        },
        {
            "destinatario": "mesadeayuda@skandia.com",
            "asunto": f"[ESCALAMIENTO] {ticket['numero']} — {ticket['error_titulo']}",
            "cuerpo": f"""TICKET DE ESCALAMIENTO AUTOMÁTICO

Número: {ticket['numero']}
Prioridad: {"ALTA" if ticket.get('es_critico') else "MEDIA"}
Fecha: {ticket['fecha_creacion']}
SLA: {ticket['sla']}

Cliente: {ticket['cliente_nombre']}
Contrato: {ticket['cliente_contrato']}
Error: {ticket['error_id']} — {ticket['error_titulo']}

ACCIONES YA REALIZADAS:
{ticket['informe_completo']}

Por favor gestionar a la brevedad posible.
Sistema automatizado Skandia""",
        },
    ]
    return correos
