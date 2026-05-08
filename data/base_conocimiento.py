"""Base de conocimiento de errores recurrentes y datos demo para Skandia."""

# ── BASE DE CONOCIMIENTO ────────────────────────────────────────────────────
KNOWLEDGE_BASE = {
    "ERR001": {
        "titulo": "No se puede inscribir cuenta bancaria activa",
        "categoria": "Cuentas bancarias",
        "descripcion": "El cliente intenta inscribir una cuenta que ya está registrada en otro contrato.",
        "solucion_ia": [
            "Ve a Mi Perfil → Cuentas registradas y verifica si ya tienes esta cuenta inscrita.",
            "Si la cuenta aparece como activa en otro contrato, debes desvincularla primero en Configuración → Cuentas.",
            "Espera 5 minutos y vuelve a intentar la inscripción.",
            "Regresa al módulo de Retiros e intenta el proceso nuevamente."
        ],
        "modulo_destino": "Cuentas Bancarias",
        "icono": "🏦"
    },
    "ERR002": {
        "titulo": "Retiro no procesado por fondos insuficientes",
        "categoria": "Retiros",
        "descripcion": "El monto solicitado supera el saldo disponible para retiro.",
        "solucion_ia": [
            "Verifica tu saldo disponible actual en la pantalla de retiros (no es el saldo total).",
            "El saldo disponible puede diferir del saldo total por inversiones en plazos fijos.",
            "Ajusta el monto del retiro a un valor menor o igual al saldo disponible mostrado.",
            "Si requieres el total, selecciona la opción 'Retiro total' en lugar de monto específico."
        ],
        "modulo_destino": "Retiros",
        "icono": "💰"
    },
    "ERR003": {
        "titulo": "Retiro bloqueado por perfil de inversión no actualizado",
        "categoria": "Retiros",
        "descripcion": "El perfil de riesgo del cliente está vencido y bloquea transacciones.",
        "solucion_ia": [
            "Tu perfil de inversión requiere actualización anual — el tuyo está vencido.",
            "Ve a Mi Portafolio → Actualizar perfil de inversión.",
            "Completa el cuestionario de perfil de riesgo (tarda aproximadamente 5 minutos).",
            "Una vez actualizado, regresa a Retiros para continuar con tu solicitud."
        ],
        "modulo_destino": "Mi Portafolio",
        "icono": "📊"
    },
    "ERR004": {
        "titulo": "No se pueden actualizar datos personales — documento en proceso",
        "categoria": "Actualización de datos",
        "descripcion": "Existe una solicitud de actualización pendiente de validación.",
        "solucion_ia": [
            "Tienes una solicitud de actualización de datos en proceso de validación.",
            "El proceso de validación puede tardar hasta 24 horas hábiles.",
            "Recibirás una notificación por correo cuando esté completada.",
            "Si es urgente, comunícate con tu Financial Planner para agilizar el proceso."
        ],
        "modulo_destino": "Mis Datos",
        "icono": "👤"
    },
    "ERR005": {
        "titulo": "Error al cargar extracto — timeout del servidor",
        "categoria": "Documentos",
        "descripcion": "El servidor tardó demasiado en generar el documento solicitado.",
        "solucion_ia": [
            "El servidor de documentos está experimentando alta demanda en este momento.",
            "Espera 2-3 minutos e intenta descargar el documento nuevamente.",
            "Si el error persiste, intenta en un navegador diferente o modo incógnito.",
            "Como alternativa, solicita el envío del documento a tu correo registrado."
        ],
        "modulo_destino": "Documentos",
        "icono": "📄"
    },
    "ERR006": {
        "titulo": "Aporte rechazado por límite diario superado",
        "categoria": "Aportes",
        "descripcion": "El monto del aporte supera el límite diario permitido.",
        "solucion_ia": [
            "Has alcanzado el límite diario de aportes permitido por regulación ($50.000.000 COP).",
            "Puedes realizar aportes adicionales a partir de las 12:01 a.m. del día siguiente.",
            "Si necesitas un límite mayor, comunícate con tu Financial Planner para solicitar una excepción.",
            "También puedes dividir el aporte en múltiples transacciones en días distintos."
        ],
        "modulo_destino": "Aportes",
        "icono": "⬆️"
    },
    "ERR007": {
        "titulo": "Portafolio no muestra saldo actualizado — caché del sistema",
        "categoria": "Mi Portafolio",
        "descripcion": "Los saldos mostrados corresponden a una versión anterior cacheada.",
        "solucion_ia": [
            "Los saldos se actualizan cada 15 minutos durante el horario de mercado.",
            "Limpia la caché de tu navegador con Ctrl+Shift+Delete y recarga la página.",
            "Si el problema persiste después de 30 minutos, cierra sesión y vuelve a ingresar.",
            "Los saldos reales se reflejan al cierre del día hábil (después de las 6:00 p.m.)."
        ],
        "modulo_destino": "Mi Portafolio",
        "icono": "🔄"
    },
    "ERR008": {
        "titulo": "Error de autenticación — sesión expirada",
        "categoria": "Acceso al portal",
        "descripcion": "La sesión del cliente expiró por inactividad.",
        "solucion_ia": [
            "Tu sesión expiró por seguridad después de 15 minutos de inactividad.",
            "Haz clic en 'Ingresar' e ingresa tus credenciales nuevamente.",
            "Para evitar esto, activa la opción 'Recordar mi sesión' al iniciar.",
            "Si olvidaste tu contraseña, usa el link '¿Olvidaste tu contraseña?' en el login."
        ],
        "modulo_destino": "Login",
        "icono": "🔐"
    },
    "ERR009": {
        "titulo": "Cuenta bancaria en lista de restricción SARLAFT",
        "categoria": "Cuentas bancarias",
        "descripcion": "La cuenta bancaria está marcada en el sistema de prevención de lavado de activos.",
        "solucion_ia": [
            "La cuenta que intentas inscribir tiene una restricción en nuestro sistema de seguridad.",
            "Esta situación requiere validación manual por parte de nuestro equipo de cumplimiento.",
            "Debes contactar a tu Financial Planner con los documentos de la cuenta bancaria.",
            "El proceso de validación tarda entre 2 y 5 días hábiles."
        ],
        "modulo_destino": "Cuentas Bancarias",
        "icono": "🚫",
        "es_critico": True
    },
    "ERR010": {
        "titulo": "Retiro no disponible — periodo de bloqueo del fondo",
        "categoria": "Retiros",
        "descripcion": "El fondo tiene un periodo mínimo de permanencia que aún no se ha cumplido.",
        "solucion_ia": [
            "El fondo seleccionado tiene un periodo mínimo de permanencia de 30 días.",
            "Tu inversión en este fondo fue realizada hace menos de 30 días.",
            "Puedes realizar retiros de otros fondos sin restricción de tiempo.",
            "La fecha disponible para retiro se muestra en el detalle del fondo."
        ],
        "modulo_destino": "Retiros",
        "icono": "⏳"
    },
    "ERR011": {
        "titulo": "Actualización de perfil de riesgo — pendiente de firma electrónica",
        "categoria": "Mi Portafolio",
        "descripcion": "El cambio de perfil requiere firma electrónica que no ha sido completada.",
        "solucion_ia": [
            "Tu solicitud de cambio de perfil está pendiente de firma electrónica.",
            "Revisa tu correo — te enviamos un enlace de firma hace unos momentos.",
            "El enlace de firma vence en 24 horas. Si venció, genera uno nuevo desde el portal.",
            "Si no puedes completar la firma digital, tu FP puede gestionar el cambio de forma presencial."
        ],
        "modulo_destino": "Mi Portafolio",
        "icono": "✍️"
    },
    "ERR012": {
        "titulo": "Certificado de aportes no generado — periodo fiscal no cerrado",
        "categoria": "Documentos",
        "descripcion": "El certificado del año en curso no está disponible hasta el cierre fiscal.",
        "solucion_ia": [
            "Los certificados del año en curso solo están disponibles después del cierre fiscal (enero del año siguiente).",
            "Para el año vigente, puedes descargar un extracto de movimientos como soporte temporal.",
            "Los certificados de años anteriores están disponibles de inmediato en la sección Documentos.",
            "Si necesitas el certificado urgente para declaración, contacta a tu Financial Planner."
        ],
        "modulo_destino": "Documentos",
        "icono": "📋"
    },
    "ERR013": {
        "titulo": "Contraseña incorrecta — bloqueo por múltiples intentos",
        "categoria": "Acceso al portal",
        "descripcion": "El portal fue bloqueado tras 3 intentos fallidos de contraseña.",
        "solucion_ia": [
            "Tu portal fue bloqueado temporalmente por seguridad tras múltiples intentos fallidos.",
            "Haz clic en '¿Olvidaste tu contraseña?' en la pantalla de login.",
            "Recibirás un correo con el enlace de restablecimiento en los próximos 2 minutos.",
            "Si no recibes el correo, revisa la carpeta de spam o correo no deseado.",
            "Una vez restablecida, intenta ingresar nuevamente con la nueva contraseña."
        ],
        "modulo_destino": "Login",
        "icono": "🔒"
    },
    "ERR014": {
        "titulo": "Portal bloqueado por actividad sospechosa — posible fraude",
        "categoria": "Seguridad",
        "descripcion": "Acceso desde dispositivo o ubicación inusual detectado.",
        "solucion_ia": [
            "⚠️ ALERTA DE SEGURIDAD: Detectamos acceso desde un dispositivo no reconocido.",
            "Por tu seguridad, hemos bloqueado el acceso temporalmente.",
            "Recibirás una alerta inmediata a tu correo y celular registrado.",
            "Si NO reconoces este intento, comunícate INMEDIATAMENTE con la línea de fraudes.",
            "NUNCA compartas tu contraseña ni códigos OTP con nadie, incluyendo asesores de Skandia."
        ],
        "modulo_destino": "Login",
        "icono": "🚨",
        "es_critico": True
    },
    "ERR015": {
        "titulo": "Fallo técnico en acceso al portal — error 500",
        "categoria": "Acceso al portal",
        "descripcion": "El portal no carga o presenta error técnico al intentar ingresar.",
        "solucion_ia": [
            "Limpia la caché y cookies de tu navegador (Ctrl+Shift+Delete → borrar todo).",
            "Intenta en modo incógnito (Ctrl+Shift+N en Chrome) o en un navegador diferente.",
            "Verifica tu conexión a internet o cambia a datos móviles.",
            "Si el problema persiste, el portal puede estar en mantenimiento programado.",
            "Intenta nuevamente en 10-15 minutos."
        ],
        "modulo_destino": "Login",
        "icono": "⚠️"
    },
    "ERR016": {
        "titulo": "Usuario no encontrado — documento no registrado",
        "categoria": "Acceso al portal",
        "descripcion": "El número de documento ingresado no tiene usuario activo.",
        "solucion_ia": [
            "Verifica que estás ingresando el número de cédula sin puntos, comas ni espacios.",
            "Si eres cliente nuevo, primero debes registrarte en la opción 'Crear cuenta'.",
            "Confirma que usas el mismo documento con el que firmaste tu contrato con Skandia.",
            "Si el problema persiste, contacta a tu Financial Planner asignado."
        ],
        "modulo_destino": "Login",
        "icono": "👤"
    },
    "ERR017": {
        "titulo": "Código OTP no llega al celular o correo",
        "categoria": "Verificación de seguridad",
        "descripcion": "El cliente no recibe el código de verificación de doble factor.",
        "solucion_ia": [
            "Espera hasta 2 minutos — los SMS pueden tener demora según el operador.",
            "Verifica que el número de celular en tu perfil sea el correcto.",
            "Revisa la carpeta de spam si esperas el código por correo electrónico.",
            "Presiona 'Reenviar código' solo UNA VEZ — múltiples reenvíos generan bloqueo.",
            "Selecciona la opción alternativa (correo vs. SMS) para recibirlo por otro canal."
        ],
        "modulo_destino": "Verificación",
        "icono": "📱"
    },
}

# ── CLIENTES DEMO ────────────────────────────────────────────────────────────
CLIENTES_DEMO = [
    {
        "id": "CLI001",
        "nombre": "Carlos Mendoza",
        "documento": "1020456789",
        "contrato": "SKD-2024-001",
        "contrato_num": "100006674636",
        "email": "carlos.mendoza@email.com",
        "telefono": "300-111-2233",
        "fp_id": "FP001",
        "saldo_ahorro": 1414977.14,
        "saldo_pension": 77675843.93,
        "perfil_riesgo": "Moderado",
        "cuentas": [
            {"banco": "Banco Davivienda", "tipo": "Ahorros", "numero": "12345678991", "estado": "Activa"}
        ],
        "historial": [
            {"fecha": "2026-04-15", "tipo": "Retiro parcial", "monto": 500000, "estado": "Procesado"},
            {"fecha": "2026-03-02", "tipo": "Aporte", "monto": 2000000, "estado": "Procesado"},
            {"fecha": "2026-02-10", "tipo": "Retiro parcial", "monto": 300000, "estado": "Procesado"},
        ],
        "escenario": "A"
    },
    {
        "id": "CLI002",
        "nombre": "María López",
        "documento": "1032789456",
        "contrato": "SKD-2023-087",
        "contrato_num": "100006874521",
        "email": "maria.lopez@email.com",
        "telefono": "311-222-3344",
        "fp_id": "FP001",
        "saldo_ahorro": 8750000.00,
        "saldo_pension": 45230000.00,
        "perfil_riesgo": "Conservador",
        "cuentas": [],
        "historial": [
            {"fecha": "2026-03-20", "tipo": "Retiro total", "monto": 1200000, "estado": "Rechazado"},
            {"fecha": "2026-01-15", "tipo": "Aporte", "monto": 500000, "estado": "Procesado"},
        ],
        "escenario": "B"
    },
    {
        "id": "CLI003",
        "nombre": "Roberto Sánchez",
        "documento": "79854123",
        "contrato": "SKD-2022-154",
        "contrato_num": "100005423187",
        "email": "roberto.sanchez@email.com",
        "telefono": "315-444-5566",
        "fp_id": "FP002",
        "saldo_ahorro": 32400000.00,
        "saldo_pension": 120500000.00,
        "perfil_riesgo": "Agresivo",
        "cuentas": [
            {"banco": "Bancolombia", "tipo": "Corriente", "numero": "78945612300", "estado": "Activa"}
        ],
        "historial": [
            {"fecha": "2026-04-01", "tipo": "Cambio portafolio", "monto": 0, "estado": "En trámite"},
            {"fecha": "2026-02-28", "tipo": "Retiro parcial", "monto": 5000000, "estado": "Procesado"},
        ],
        "escenario": "C"
    },
    {
        "id": "CLI004",
        "nombre": "Lucía Ramírez",
        "documento": "1015678234",
        "contrato": "SKD-2025-012",
        "contrato_num": "100007123456",
        "email": "lucia.ramirez@email.com",
        "telefono": "302-888-9900",
        "fp_id": "FP002",
        "saldo_ahorro": 560000.00,
        "saldo_pension": 0,
        "perfil_riesgo": "Moderado",
        "cuentas": [],
        "historial": [],
        "escenario": "libre"
    },
]

# ── AGENTES Y FINANCIAL PLANNERS ─────────────────────────────────────────────
AGENTES_DEMO = {
    "FP001": {
        "id": "FP001",
        "nombre": "Ana García",
        "email": "ana.garcia@skandia.com",
        "telefono": "601-744-0000 ext. 1201",
        "rol": "Financial Planner",
        "avatar": "👩‍💼"
    },
    "FP002": {
        "id": "FP002",
        "nombre": "Julián Torres",
        "email": "julian.torres@skandia.com",
        "telefono": "601-744-0000 ext. 1205",
        "rol": "Financial Planner",
        "avatar": "👨‍💼"
    },
    "AGT001": {
        "id": "AGT001",
        "nombre": "Luis Herrera",
        "email": "luis.herrera@skandia.com",
        "telefono": "601-744-0000 ext. 2301",
        "rol": "Agente Técnico",
        "avatar": "👨‍💻"
    },
    "AGT002": {
        "id": "AGT002",
        "nombre": "Sandra Morales",
        "email": "sandra.morales@skandia.com",
        "telefono": "601-744-0000 ext. 2302",
        "rol": "Agente Técnico",
        "avatar": "👩‍💻"
    },
}

# ── MAPEO DE ERRORES POR ESCENARIO ───────────────────────────────────────────
ESCENARIOS_ERROR = {
    "A": "ERR001",   # Carlos: cuenta bancaria
    "B": "ERR009",   # María: SARLAFT
    "C": "ERR011",   # Roberto: firma electrónica
    "libre": "ERR002",
}

# ── DATOS NPS SINTÉTICOS ─────────────────────────────────────────────────────
import random, datetime

def generar_nps_sintetico(n: int = 120) -> list:
    categorias = [
        "Solicité un retiro",
        "Consulte mi saldo",
        "Realicé un aporte",
        "Gestioné mi portafolio",
        "Registros de cuentas bancarias",
        "Consulté documentos/certificados",
        "Actualicé mis datos",
        "Otras",
    ]
    comentarios_detractores = [
        "No pude inscribir mi cuenta bancaria, el sistema no me dejó",
        "Llevo 3 días intentando hacer el retiro y no funciona",
        "La página se cayó justo cuando iba a confirmar",
        "No entiendo por qué me bloquean el acceso",
        "Mi saldo no se actualiza hace dos semanas",
        "El certificado no se descarga, error permanente",
        "Tuve que llamar 3 veces para resolver algo sencillo",
    ]
    comentarios_promotores = [
        "Excelente plataforma, muy fácil de usar",
        "Proceso rápido y seguro, muy satisfecho",
        "Me encanta poder ver todo en un solo lugar",
        "El asesor fue muy amable y resolvió todo",
        "Muy buena experiencia en general",
    ]
    registros = []
    base_date = datetime.date(2026, 1, 1)
    for i in range(n):
        score = random.choices(
            list(range(11)),
            weights=[3,3,4,4,5,5,8,8,15,20,25]
        )[0]
        cat = random.choice(categorias)
        if score <= 6:
            comentario = random.choice(comentarios_detractores)
        else:
            comentario = random.choice(comentarios_promotores)
        fecha = base_date + datetime.timedelta(days=random.randint(0, 127))
        registros.append({
            "NPS": score,
            "Segmento_NPS": "Detractor" if score <= 6 else ("Pasivo" if score <= 8 else "Promotor"),
            "Transaccion": cat,
            "Comentario": comentario,
            "Fecha": str(fecha),
        })
    return registros
