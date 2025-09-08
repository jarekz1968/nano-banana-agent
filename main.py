import os, shutil, json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

# Wczytaj konfigurację
config_path = os.getenv("CONFIG_PATH", "config.json")
config = json.load(open(config_path))

# Ścieżki folderów
PENDING = "pending"
APPROVED = "approved"
PUBLISHED = "published"

# Utwórz foldery jeśli nie istnieją
for folder in [PENDING, APPROVED, PUBLISHED]:
    os.makedirs(folder, exist_ok=True)

# Inicjalizacja aplikacji
app = FastAPI()
templates = Environment(loader=FileSystemLoader("templates"))

@app.get("/", response_class=HTMLResponse)
def index():
    html = templates.get_template("index.html").render(
        pending=os.listdir(PENDING),
        approved=os.listdir(APPROVED),
        published=os.listdir(PUBLISHED)
    )
    return HTMLResponse(html)

@app.post("/generate")
def generate_bundle():
    # Symulacja generowania zestawu
    bundle_id = f"bundle_{len(os.listdir(PENDING)) + 1}"
    bundle_dir = os.path.join(PENDING, bundle_id)
    os.makedirs(bundle_dir)
    # Tworzenie plików testowych
    for i in range(1, 6):
        with open(os.path.join(bundle_dir, f"graphic{i}.png"), "w") as f:
            f.write("PNG_DATA")
    with open(os.path.join(bundle_dir, "mockup.jpg"), "w") as f:
        f.write("MOCKUP")
    with open(os.path.join(bundle_dir, "promo.mp4"), "w") as f:
        f.write("VIDEO")
    return {"status": "generated", "bundle": bundle_id}

@app.post("/approve")
def approve(bundle: str = Form(...)):
    src = os.path.join(PENDING, bundle)
    dst = os.path.join(APPROVED, bundle)
    shutil.move(src, dst)
    return {"status": "approved", "bundle": bundle}

@app.post("/publish")
def publish(bundle: str = Form(...)):
    src = os.path.join(APPROVED, bundle)
    dst = os.path.join(PUBLISHED, bundle)
    shutil.move(src, dst)
    # Tu można dodać integrację z Etsy API i Buffer
    return {"status": "published", "bundle": bundle}
