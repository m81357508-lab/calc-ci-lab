import os
import socket
from datetime import datetime
import psycopg
from flask import Flask

app = Flask(__name__)
DB_DSN = (
	f"host={os.getenv('DB_HOST', 'db')} "
	f"port={os.getenv('DB_PORT', '5432')} "
	f"dbname={os.getenv('DB_NAME')} "
	f"user={os.getenv('DB_USER')} "
	f"password={os.getenv('DB_PASSWORD')}"
)

def init_db():
	with psycopg.connect(DB_DSN) as conn:
		conn.execute(
			"CREATE TABLE IF NOT EXISTS visits ("
			"id SERIAL PRIMARY KEY, "
			"visited_at TIMESTAMP NOT NULL, "
			"host TEXT NOT NULL)"
		)

@app.route("/")
def index():
	with psycopg.connect(DB_DSN) as conn:
		conn.execute(
			"INSERT INTO visits (visited_at, host) VALUES (%s, %s)",
			(datetime.now(), socket.gethostname()),
		)
		total = conn.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
	return (
		f"<h1>Docker Compose: web + db</h1>"
		f"<p>Всего визитов: <b>{total}</b></p>"
		f"<p>Обработал контейнер: {socket.gethostname()}</p>"
		f"<p>Приложение: {os.getenv('APP_TITLE', 'без названия')}</p>"
	)

@app.route("/health")
def health():
	return {"status": "ok"}

if __name__ == "__main__":
	init_db()
	app.run(host="0.0.0.0", port=5000)
