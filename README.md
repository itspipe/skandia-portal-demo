# ✦ Skandia Portal CX — Demo Hackathon

Aplicación Streamlit completa para demo del portal de clientes Skandia con agente IA, técnico en tiempo real y sistema de escalamiento.

## Estructura

```
skandia/
├── app.py                        # Entrypoint principal
├── requirements.txt
├── config/
│   └── brand.py                  # Colores y CSS marca Skandia
├── data/
│   └── base_conocimiento.py      # Errores, clientes y agentes demo
├── modules/
│   ├── session_manager.py        # Gestión de estado global
│   ├── nlp_categorizer.py        # Clasificación NLP de comentarios
│   ├── chatbot.py                # Agente IA conversacional
│   ├── tecnico.py                # Interfaz técnico en tiempo real
│   └── report_generator.py      # Generación de informes y tickets
└── pages/
    ├── login.py                  # Login + OTP + errores de acceso
    ├── inicio.py                 # Dashboard personal del cliente
    ├── retiros.py                # Flujo de retiros en 3 pasos
    ├── cuentas.py                # Inscripción de cuentas bancarias
    ├── otras_paginas.py          # Portafolio, Documentos, Mis Datos
    ├── nps.py                    # Encuesta NPS post-experiencia
    ├── dashboard.py              # Analítica Big Data
    └── control_tower.py          # Panel de CX en tiempo real
```

## Instalación y ejecución

```bash
# 1. Clonar o descomprimir el proyecto
cd skandia

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
streamlit run app.py
```

La app abre en: **http://localhost:8501**

## Credenciales demo

| Cliente | Documento | Contraseña | Escenario |
|---|---|---|---|
| Carlos Mendoza | `1020456789` | `skandia123` | A — IA resuelve |
| María López | `1032789456` | `skandia123` | B — Técnico resuelve |
| Roberto Sánchez | `79854123` | `skandia123` | C — Escalamiento |
| Lucía Ramírez | `1015678234` | `skandia123` | Libre |

**Código OTP:** `123456` (en todos los flujos)

## Escenarios de demo

### 🟢 Escenario A — IA resuelve exitosamente
1. Login con Carlos Mendoza
2. Ir a Retiros → intentar procesar → ERR001 (cuenta bancaria)
3. Chatbot IA activa y guía al módulo de cuentas
4. Se inscribe la cuenta → retiro procesado exitosamente

### 🟡 Escenario B — IA falla, técnico resuelve
1. Login con María López
2. Ir a Cuentas Bancarias → intentar inscribir → ERR009 (SARLAFT)
3. Chatbot IA activa, pasos no resuelven
4. Cliente pide técnico → vista dual cliente/técnico
5. Técnico valida y resuelve → notificaciones enviadas

### 🔴 Escenario C — Escalado a mesa de ayuda
1. Login con Roberto Sánchez
2. Ir a Portafolio → cambiar perfil → ERR011 (firma electrónica)
3. Chatbot IA no resuelve → técnico tampoco
4. Técnico escala → ticket generado → correos simulados

## Datos opcionales
Si tienes el archivo `Portal Clientes 2026.xlsx - Sheet0.csv`, ubícalo en la raíz del proyecto. De lo contrario, el dashboard usa datos sintéticos automáticamente.
