import os
import sqlite3
import json
import logging
import urllib.request
from datetime import datetime, timedelta

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DB_PATH = "football.db"

# Free, no-key football data source
OPENFOOTBALL_BASE = "https://raw.githubusercontent.com/openfootball/football.json/master"

LEAGUES = {
    "premier_league": {"name": "Premier League", "path": "2025-26/en.1.json"},
    "la_liga": {"name": "La Liga", "path": "2025-26/es.1.json"},
    "bundesliga": {"name": "Bundesliga", "path": "2025-26/de.1.json"},
    "serie_a": {"name": "Serie A", "path": "2025-26/it.1.json"},
    "ligue_1": {"name": "Ligue 1", "path": "2025-26/fr.1.json"},
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            league TEXT DEFAULT 'premier_league',
            subscribed_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS sent_matches (
            match_key TEXT PRIMARY KEY,
            sent_at TEXT
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


def fetch_league(league_key):
    """Fetch fixtures/results JSON from openfootball (no API key)."""
    info = LEAGUES.get(league_key)
    if not info:
        return None
    url = f"{OPENFOOTBALL_BASE}/{info['path']}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        logger.warning("Fetch failed for %s: %s", league_key, e)
        return None


def parse_matches(data):
    """Return list of matches with date, teams, score, status."""
    if not data or "matches" not in data:
        return []
    out = []
    for m in data["matches"]:
        date = m.get("date", "")
        team1 = m.get("team1", "?")
        team2 = m.get("team2", "?")
        score = m.get("score", {})
        ft = score.get("ft") if isinstance(score, dict) else None
        status = "finished" if ft else "scheduled"
        out.append({
            "date": date,
            "team1": team1,
            "team2": team2,
            "ft": ft,
            "status": status,
            "key": f"{date}_{team1}_{team2}",
        })
    return out


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_exec(
        "INSERT OR IGNORE INTO subscribers (user_id, username, league, subscribed_at) VALUES (?,?,?,?)",
        (user.id, user.username or "", "premier_league", datetime.utcnow().isoformat())
    )

    keyboard = [
        [InlineKeyboardButton("📅 Today's Fixtures", callback_data="today")],
        [InlineKeyboardButton("🏆 Standings", callback_data="standings")],
        [InlineKeyboardButton("⚽ Choose League", callback_data="choose_league")],
        [InlineKeyboardButton("🔔 My Subscription", callback_data="my_sub")],
    ]

    await update.message.reply_text(
        f"👋 Welcome to <b>Football Updates</b>, {user.first_name}!\n\n"
        "Get live match results, fixtures, and standings for major European leagues.\n\n"
        "No predictions. Just real football data.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


async def today_fixtures(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user_id = update.effective_user.id

    rows = db_exec("SELECT league FROM subscribers WHERE user_id=?", (user_id,))
    league = rows[0][0] if rows else "premier_league"

    data = fetch_league(league)
    matches = parse_matches(data)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    today_matches = [m for m in matches if m["date"] == today]

    if not today_matches:
        # Show upcoming 5 if none today
        upcoming = sorted([m for m in matches if m["date"] >= today], key=lambda x: x["date"])[:5]
        text = f"📅 <b>No matches today in {LEAGUES[league]['name']}.</b>\n\nUpcoming:\n"
        for m in upcoming:
            text += f"• {m['date']} — {m['team1']} vs {m['team2']}\n"
    else:
        text = f"📅 <b>Today's Matches — {LEAGUES[league]['name']}</b>\n\n"
        for m in today_matches:
            if m["ft"]:
                text += f"✅ {m['team1']} <b>{m['ft'][0]}-{m['ft'][1]}</b> {m['team2']}\n"
            else:
                text += f"⏳ {m['team1']} vs {m['team2']}\n"

    await q.edit_message_text(
        text, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])
    )


async def standings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    # Standings require computed data; for simplicity, show a note + link to bot content
    await q.edit_message_text(
        "🏆 <b>Standings</b>\n\n"
        "Standings are calculated from match results in the free openfootball dataset. "
        "Full standings display will be added in the next update.\n\n"
        "For now, use 'Today's Fixtures' to see live results.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])
    )


async def choose_league(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    keyboard = [
        [InlineKeyboardButton("🇬🇧 Premier League", callback_data="league_premier_league")],
        [InlineKeyboardButton("🇪🇸 La Liga", callback_data="league_la_liga")],
        [InlineKeyboardButton("🇩🇪 Bundesliga", callback_data="league_bundesliga")],
        [InlineKeyboardButton("🇮🇹 Serie A", callback_data="league_serie_a")],
        [InlineKeyboardButton("🇫🇷 Ligue 1", callback_data="league_ligue_1")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")],
    ]
    await q.edit_message_text("⚽ <b>Choose your league:</b>", parse_mode="HTML",
                              reply_markup=InlineKeyboardMarkup(keyboard))


async def set_league(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    league = q.data.replace("league_", "")
    if league not in LEAGUES:
        await q.edit_message_text("Unknown league.")
        return
    db_exec("UPDATE subscribers SET league=? WHERE user_id=?", (league, update.effective_user.id))
    await q.edit_message_text(
        f"✅ Your league is now <b>{LEAGUES[league]['name']}</b>.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])
    )


async def my_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    rows = db_exec("SELECT league FROM subscribers WHERE user_id=?", (update.effective_user.id,))
    league = rows[0][0] if rows else "premier_league"
    await q.edit_message_text(
        f"🔔 <b>Your Subscription</b>\n\nLeague: <b>{LEAGUES[league]['name']}</b>\n\n"
        "You will receive automatic result notifications for finished matches.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])
    )


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    keyboard = [
        [InlineKeyboardButton("📅 Today's Fixtures", callback_data="today")],
        [InlineKeyboardButton("🏆 Standings", callback_data="standings")],
        [InlineKeyboardButton("⚽ Choose League", callback_data="choose_league")],
        [InlineKeyboardButton("🔔 My Subscription", callback_data="my_sub")],
    ]
    await q.edit_message_text("Main menu:", reply_markup=InlineKeyboardMarkup(keyboard))


async def auto_notify(context: ContextTypes.DEFAULT_TYPE):
    """Check for newly finished matches and notify subscribers."""
    logger.info("Auto-notify check running...")
    for league_key in LEAGUES:
        data = fetch_league(league_key)
        matches = parse_matches(data)
        for m in matches:
            if m["status"] != "finished":
                continue
            if db_exec("SELECT 1 FROM sent_matches WHERE match_key=?", (m["key"],)):
                continue
            # Send to subscribers of this league
            subs = db_exec("SELECT user_id FROM subscribers WHERE league=?", (league_key,))
            text = (
                f"⚽ <b>Full Time</b> — {LEAGUES[league_key]['name']}\n\n"
                f"{m['team1']} <b>{m['ft'][0]}-{m['ft'][1]}</b> {m['team2']}\n"
                f"📅 {m['date']}"
            )
            for (uid,) in subs:
                try:
                    await context.bot.send_message(uid, text, parse_mode="HTML")
                except Exception:
                    pass
            db_exec("INSERT INTO sent_matches (match_key, sent_at) VALUES (?,?)",
                    (m["key"], datetime.utcnow().isoformat()))


async def post_init(app: Application):
    app.job_queue.run_repeating(auto_notify, interval=1800, first=10)  # every 30 min
    logger.info("Auto-notify scheduled.")


def main():
    if not BOT_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN required.")
    init_db()
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(today_fixtures, pattern="^today$"))
    app.add_handler(CallbackQueryHandler(standings, pattern="^standings$"))
    app.add_handler(CallbackQueryHandler(choose_league, pattern="^choose_league$"))
    app.add_handler(CallbackQueryHandler(set_league, pattern="^league_"))
    app.add_handler(CallbackQueryHandler(my_sub, pattern="^my_sub$"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))
    app.run_polling()


if __name__ == "__main__":
    main()
