import os
import sqlite3
import logging
import random
from datetime import datetime

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

from data import LIGAS, PARTIDOS, FRASES_DIARIAS

# ---------- Configuración ----------
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DB_PATH = "futbol.db"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------- Base de datos ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS suscriptores (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            nombre TEXT,
            liga TEXT DEFAULT 'la_liga',
            registrado_en TEXT
        )
    """)
    conn.commit()
    conn.close()

def db_exec(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    r = c.fetchall()
    conn.close()
    return r

def agregar_suscriptor(user):
    db_exec(
        "INSERT OR IGNORE INTO suscriptores (user_id, username, nombre, liga, registrado_en) VALUES (?,?,?,?,?)",
        (user.id, user.username or "", user.first_name or "", "la_liga", datetime.utcnow().isoformat())
    )

# ---------- Menú principal ----------
def menu_principal():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Partidos de Hoy", callback_data="hoy")],
        [InlineKeyboardButton("🔜 Próximos Partidos", callback_data="proximos")],
        [InlineKeyboardButton("✅ Resultados Recientes", callback_data="resultados")],
        [InlineKeyboardButton("⚽ Elegir Liga", callback_data="elegir_liga")],
        [InlineKeyboardButton("🔔 Mi Suscripción", callback_data="mi_suscripcion")],
        [InlineKeyboardButton("ℹ️ Acerca de", callback_data="acerca")],
    ])

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    agregar_suscriptor(user)

    await update.message.reply_text(
        f"👋 ¡Bienvenido a <b>Accedo Gratis Fútbol</b>, {user.first_name}!\n\n"
        "Aquí recibirás información actualizada sobre fútbol: partidos, "
        "resultados y las principales ligas europeas.\n\n"
        "Sin pronósticos. Sin apuestas. Solo información real de fútbol.\n\n"
        "Usa el menú para comenzar.",
        reply_markup=menu_principal(),
        parse_mode="HTML"
    )

# ---------- Partidos de hoy ----------
async def hoy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    fecha_hoy = datetime.utcnow().strftime("%Y-%m-%d")
    partidos_hoy = [p for p in PARTIDOS if p["fecha"] == fecha_hoy]

    if not partidos_hoy:
        texto = (
            f"📅 <b>No hay partidos programados para hoy.</b>\n\n"
            f"Consulta los próximos partidos en el menú."
        )
    else:
        texto = "📅 <b>Partidos de Hoy</b>\n\n"
        for p in partidos_hoy:
            liga = LIGAS[p["liga"]]["nombre"]
            texto += f"🏆 {liga}\n"
            if p["marcador"]:
                texto += f"✅ {p['local']} <b>{p['marcador'][0]}-{p['marcador'][1]}</b> {p['visitante']}\n\n"
            else:
                texto += f"⏳ {p['local']} vs {p['visitante']}\n\n"

    await q.edit_message_text(
        texto, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data="volver")]])
    )

# ---------- Próximos partidos ----------
async def proximos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    fecha_hoy = datetime.utcnow().strftime("%Y-%m-%d")
    futuros = sorted([p for p in PARTIDOS if p["fecha"] > fecha_hoy], key=lambda x: x["fecha"])[:8]

    if not futuros:
        texto = "🔜 No hay próximos partidos registrados por ahora."
    else:
        texto = "🔜 <b>Próximos Partidos</b>\n\n"
        for p in futuros:
            liga = LIGAS[p["liga"]]["nombre"]
            texto += f"📆 {p['fecha']} — {liga}\n"
            texto += f"⚽ {p['local']} vs {p['visitante']}\n\n"

    await q.edit_message_text(
        texto, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data="volver")]])
    )

# ---------- Resultados recientes ----------
async def resultados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    terminados = [p for p in PARTIDOS if p["marcador"]]

    if not terminados:
        texto = "✅ No hay resultados recientes disponibles."
    else:
        texto = "✅ <b>Resultados Recientes</b>\n\n"
        for p in terminados[-8:]:
            liga = LIGAS[p["liga"]]["nombre"]
            texto += f"🏆 {liga}\n"
            texto += f"✅ {p['local']} <b>{p['marcador'][0]}-{p['marcador'][1]}</b> {p['visitante']}\n"
            texto += f"📆 {p['fecha']}\n\n"

    await q.edit_message_text(
        texto, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data="volver")]])
    )

# ---------- Elegir liga ----------
async def elegir_liga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    botones = []
    for key, info in LIGAS.items():
        botones.append([InlineKeyboardButton(f"⚽ {info['nombre']}", callback_data=f"liga_{key}")])
    botones.append([InlineKeyboardButton("🔙 Volver", callback_data="volver")])

    await q.edit_message_text(
        "⚽ <b>Elige tu liga favorita:</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(botones)
    )

# ---------- Establecer liga ----------
async def set_liga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    liga_key = q.data.replace("liga_", "")
    if liga_key not in LIGAS:
        await q.edit_message_text("Liga no encontrada.")
        return

    db_exec("UPDATE suscriptores SET liga=? WHERE user_id=?", (liga_key, update.effective_user.id))

    await q.edit_message_text(
        f"✅ Tu liga ahora es <b>{LIGAS[liga_key]['nombre']}</b>.\n\n"
        f"Recibirás actualizaciones automáticas de esta liga.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data="volver")]])
    )

# ---------- Mi suscripción ----------
async def mi_suscripcion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    user_id = update.effective_user.id
    filas = db_exec("SELECT liga FROM suscriptores WHERE user_id=?", (user_id,))
    liga_key = filas[0][0] if filas else "la_liga"

    total = db_exec("SELECT COUNT(*) FROM suscriptores")[0][0]

    await q.edit_message_text(
        f"🔔 <b>Mi Suscripción</b>\n\n"
        f"Liga actual: <b>{LIGAS[liga_key]['nombre']}</b>\n\n"
        f"Recibirás notificaciones automáticas cuando haya nuevos resultados.\n\n"
        f"👥 Total de suscriptores: {total}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data="volver")]])
    )

# ---------- Acerca de ----------
async def acerca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    await q.edit_message_text(
        "ℹ️ <b>Acerca de Accedo Gratis Fútbol</b>\n\n"
        "Este bot entrega información actualizada sobre fútbol: partidos, "
        "resultados y las principales ligas europeas.\n\n"
        "Elige tu liga favorita y recibe novedades directamente en tu Telegram.\n\n"
        "Sin pronósticos. Sin apuestas. Solo información real de fútbol.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data="volver")]])
    )

# ---------- Volver ----------
async def volver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "Menú principal — elige una opción:",
        reply_markup=menu_principal()
    )

# ---------- Notificación automática ----------
async def notificar_resultados(context: ContextTypes.DEFAULT_TYPE):
    """Envía resultados recientes a los suscriptores automáticamente."""
    logger.info("Verificando resultados para notificar...")

    terminados = [p for p in PARTIDOS if p["marcador"]]
    if not terminados:
        return

    frase = random.choice(FRASES_DIARIAS)
    ultimos = terminados[-3:]

    texto = f"⚽ <b>Actualización de Fútbol</b>\n\n{frase}\n\n"
    for p in ultimos:
        liga = LIGAS[p["liga"]]["nombre"]
        texto += f"🏆 {liga}\n"
        texto += f"✅ {p['local']} <b>{p['marcador'][0]}-{p['marcador'][1]}</b> {p['visitante']}\n\n"

    suscriptores = db_exec("SELECT user_id FROM suscriptores")
    enviados = 0
    for (uid,) in suscriptores:
        try:
            await context.bot.send_message(uid, texto, parse_mode="HTML")
            enviados += 1
        except Exception:
            pass

    logger.info("Notificación enviada a %d suscriptores.", enviados)

async def post_init(app: Application):
    # Enviar actualizaciones cada 6 horas
    app.job_queue.run_repeating(notificar_resultados, interval=21600, first=60)
    logger.info("Notificaciones automáticas programadas cada 6 horas.")

# ---------- Main ----------
def main():
    if not BOT_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN es obligatorio.")

    init_db()

    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(hoy, pattern="^hoy$"))
    app.add_handler(CallbackQueryHandler(proximos, pattern="^proximos$"))
    app.add_handler(CallbackQueryHandler(resultados, pattern="^resultados$"))
    app.add_handler(CallbackQueryHandler(elegir_liga, pattern="^elegir_liga$"))
    app.add_handler(CallbackQueryHandler(set_liga, pattern="^liga_"))
    app.add_handler(CallbackQueryHandler(mi_suscripcion, pattern="^mi_suscripcion$"))
    app.add_handler(CallbackQueryHandler(acerca, pattern="^acerca$"))
    app.add_handler(CallbackQueryHandler(volver, pattern="^volver$"))

    logger.info("Bot de fútbol en español iniciando...")
    app.run_polling()

if __name__ == "__main__":
    main()
