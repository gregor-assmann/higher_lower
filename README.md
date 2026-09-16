# Higher Lower

## Lokaler Entwicklungsserver

Voraussetzungen:

- Python 3.10 oder neuer
- die vom Projekt bereitgestellte `.env`
- installierte Pakete aus `requirements.txt`

Einmalig einrichten:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Die `.env` enthält die Verbindung zu der für dieses Projekt festgelegten MongoDB, einen zufälligen `FLASK_SECRET_KEY` und die Zeitzone. Der Entwicklungsserver wird aus dem `server`-Verzeichnis gestartet:

```sh
cd server
python3 main.py
```

Die Anwendung ist anschließend unter `http://localhost:8000` erreichbar.

Der Scraper kann separat gestartet werden. Er verwendet die Kategorien und XPath-Ausdrücke aus `scraper/scraper_config.yaml`; fehlt die Datei, wird automatisch die Template-Datei verwendet:

```sh
cd scraper
python3 scraper.py
```

## Docker

Docker verwendet ein Image mit zwei Containern:

- `web`: Flask-Anwendung mit Gunicorn
- `scraper`: Selenium-Scraper mit täglichem Lauf um 06:00 Uhr

Beide Container verwenden dieselbe externe MongoDB. Zum Starten:

```sh
docker compose up -d --build
```

Die Anwendung ist anschließend unter `http://localhost:8000` erreichbar. Logs können so angezeigt werden:

```sh
docker compose logs -f web
docker compose logs -f scraper
```

Die Zeitzone für den täglichen Scraper-Lauf wird über `TZ` in `.env` festgelegt.
