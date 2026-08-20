STOCKFISH_URLS = {
    "Windows": "...",
    "Linux": "...",
    "Darwin": "...",
}

BIN_DIR = "bin"  # renamed from "engine"

def setup():
    system = platform.system()
    url = STOCKFISH_URLS.get(system)
    if not url:
        raise RuntimeError(f"No prebuilt Stockfish for {system}")

    os.makedirs(BIN_DIR, exist_ok=True)
    archive_path = os.path.join(BIN_DIR, f"stockfish_download{os.path.splitext(url)[1]}")
    urllib.request.urlretrieve(url, archive_path)