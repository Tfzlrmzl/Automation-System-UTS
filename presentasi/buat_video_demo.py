#!/usr/bin/env python3
"""Create a short, captioned MP4 walkthrough from the current project outputs."""

import csv
import os
import subprocess
import tempfile
import textwrap
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "Video_Demo_UTS_Automation_Systems.mp4"
WIDTH, HEIGHT, FPS = 1280, 720, 24
BG_TOP = (11, 17, 32)
BG_BOTTOM = (18, 30, 48)
PANEL = (21, 31, 50)
PANEL_ALT = (27, 40, 63)
GOLD = (230, 189, 119)
WHITE = (243, 246, 251)
MUTED = (158, 171, 192)
GREEN = (151, 206, 174)
LINE = (54, 68, 91)


def font(size, bold=False, mono=False):
    windows = Path(os.environ.get("WINDIR", r"C:\Windows"))
    if mono:
        candidates = [windows / "Fonts" / "CascadiaMono.ttf", windows / "Fonts" / "consola.ttf"]
    else:
        candidates = [
            windows / "Fonts" / ("segoeuib.ttf" if bold else "segoeui.ttf"),
            windows / "Fonts" / ("arialbd.ttf" if bold else "arial.ttf"),
        ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


FONTS = {
    "small": font(15),
    "body": font(20),
    "body_bold": font(20, bold=True),
    "subtitle": font(25),
    "heading": font(36, bold=True),
    "title": font(54, bold=True),
    "mono": font(16, mono=True),
    "mono_bold": font(16, bold=True, mono=True),
}


def rounded(draw, box, fill, outline=None, radius=18, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, font_name="body", fill=WHITE, anchor=None):
    draw.text(xy, value, font=FONTS[font_name], fill=fill, anchor=anchor)


def wrapped(draw, xy, value, max_chars=45, font_name="body", fill=MUTED, spacing=8):
    x, y = xy
    for line in textwrap.wrap(value, width=max_chars):
        draw.text((x, y), line, font=FONTS[font_name], fill=fill)
        y += FONTS[font_name].size + spacing
    return y


def background(section, stamp):
    image = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = image.load()
    for y in range(HEIGHT):
        fraction = y / (HEIGHT - 1)
        color = tuple(int(BG_TOP[i] * (1 - fraction) + BG_BOTTOM[i] * fraction) for i in range(3))
        for x in range(WIDTH):
            pixels[x, y] = color
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 8, HEIGHT), fill=GOLD)
    text(draw, (48, 25), "BOOKFOLIO  /  AUTOMATION SYSTEMS", "small", MUTED)
    text(draw, (1230, 25), section.upper(), "small", GOLD, anchor="ra")
    draw.line((50, 674, 1230, 674), fill=LINE, width=1)
    text(draw, (52, 687), "Muhammad Tafzil Rimzal  ·  312310529", "small", MUTED)
    text(draw, (1228, 687), stamp, "small", GOLD, anchor="ra")
    return image


def heading(draw, eyebrow, title, subtitle=None):
    text(draw, (58, 91), eyebrow.upper(), "small", GOLD)
    text(draw, (58, 124), title, "heading", WHITE)
    if subtitle:
        text(draw, (60, 176), subtitle, "body", MUTED)


def make_web_capture():
    browser_paths = [
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Google/Chrome/Application/chrome.exe",
    ]
    browser = next((path for path in browser_paths if path.is_file()), None)
    if browser is None:
        raise FileNotFoundError("Microsoft Edge or Google Chrome is required to capture the catalog.")
    catalog = ROOT / "output" / "index.html"
    if not catalog.is_file():
        raise FileNotFoundError(f"Catalog page not found: {catalog}")
    url = catalog.as_uri()
    with tempfile.TemporaryDirectory(prefix="bookfolio-demo-") as directory:
        directory = Path(directory)
        shot = directory / "catalog.png"
        profile = directory / "browser-profile"
        command = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-first-run",
            f"--user-data-dir={profile}",
            "--window-size=1440,1100",
            f"--screenshot={shot}",
            url,
        ]
        result = subprocess.run(command, capture_output=True, timeout=45, check=False)
        if result.returncode or not shot.is_file():
            detail = result.stderr.decode(errors="replace")[-1200:]
            raise RuntimeError(f"Browser could not capture the catalog page: {detail}")
        return Image.open(shot).convert("RGB")


def run_scraper():
    python = ROOT / ".venv" / "Scripts" / "python.exe"
    if not python.is_file():
        raise FileNotFoundError(f"Project virtual environment Python not found: {python}")
    command = [str(python), "main.py", "--limit", "30", "--backup"]
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        check=False,
    )
    output = result.stdout + ("\n" + result.stderr if result.stderr else "")
    if result.returncode:
        raise RuntimeError(f"Scraper failed with exit code {result.returncode}:\n{output}")
    return output


def title_scene(stamp):
    image = background("Video Demonstrasi", stamp)
    draw = ImageDraw.Draw(image)
    rounded(draw, (850, 102, 1198, 590), PANEL, LINE)
    text(draw, (1024, 176), "01", "title", GOLD, anchor="mm")
    draw.line((930, 236, 1118, 236), fill=LINE, width=2)
    text(draw, (1024, 287), "AUTOMATION", "subtitle", WHITE, anchor="mm")
    text(draw, (1024, 326), "SYSTEMS", "subtitle", WHITE, anchor="mm")
    text(draw, (62, 126), "DEMO PROYEK UTS  ·  2025/2026", "small", GOLD)
    text(draw, (60, 190), "Online Book", "title", WHITE)
    text(draw, (60, 250), "Catalog Organizer", "title", WHITE)
    wrapped(draw, (64, 345), "Mengumpulkan, membersihkan, menyimpan, dan menampilkan katalog buku secara otomatis.", 42, "subtitle", MUTED, 10)
    text(draw, (64, 505), "Muhammad Tafzil Rimzal  ·  NIM 312310529", "body_bold", WHITE)
    text(draw, (64, 547), "Kelompok individu — telah dikonfirmasi dosen", "small", MUTED)
    text(draw, (64, 624), "SCRAPING  ·  REGEX  ·  FILE I/O  ·  BACKUP ZIP", "small", GOLD)
    return image


def workflow_scene(stamp):
    image = background("Tujuan & Alur", stamp)
    draw = ImageDraw.Draw(image)
    heading(draw, "01  /  Tujuan", "Dari situs katalog ke data terorganisasi", "Sumber latihan publik: Books to Scrape")
    stages = [
        ("01", "Ambil", "requests"),
        ("02", "Parse", "BeautifulSoup"),
        ("03", "Bersihkan", "Regex"),
        ("04", "Simpan", "CSV / TXT / HTML"),
        ("05", "Backup", "ZIP"),
    ]
    start, width, gap = 58, 217, 20
    for i, (num, name, tech) in enumerate(stages):
        x = start + i * (width + gap)
        rounded(draw, (x, 278, x + width, 436), PANEL, LINE)
        text(draw, (x + 20, 302), num, "small", GOLD)
        text(draw, (x + 20, 346), name, "body_bold", WHITE)
        text(draw, (x + 20, 392), tech, "small", MUTED)
        if i < len(stages) - 1:
            text(draw, (x + width + 3, 340), "›", "heading", GOLD)
    rounded(draw, (58, 476, 1220, 574), PANEL_ALT)
    text(draw, (82, 498), "TARGET", "small", GOLD)
    text(draw, (82, 534), "30 record  ·  keyword opsional  ·  hasil dapat dibuka kembali", "body_bold", WHITE)
    return image


def terminal_scene(stamp, log):
    image = background("Demo CLI", stamp)
    draw = ImageDraw.Draw(image)
    heading(draw, "02  /  Eksekusi", "Scraping dijalankan lewat CLI")
    rounded(draw, (57, 214, 1220, 588), (13, 20, 33), LINE)
    rounded(draw, (57, 214, 1220, 258), PANEL_ALT, LINE, radius=18)
    for i, color in enumerate(((242, 106, 106), (242, 189, 93), (98, 197, 130))):
        draw.ellipse((78 + i * 26, 229, 91 + i * 26, 242), fill=color)
    text(draw, (172, 228), "PowerShell  ·  project root", "small", MUTED)
    command = r".\.venv\Scripts\python.exe main.py --limit 30 --backup"
    text(draw, (83, 282), "> " + command, "mono_bold", GREEN)
    lines = [line.strip() for line in log.splitlines() if line.strip()]
    y = 331
    for line in lines[:7]:
        if len(line) > 106:
            line = line[:103] + "..."
        text(draw, (83, y), line, "mono", WHITE if "[+]" in line else MUTED)
        y += 33
    if not lines:
        text(draw, (83, y), "Scraping berjalan dan hasil tersimpan ke folder proyek.", "mono", WHITE)
    return image


def catalog_scene(stamp, screenshot):
    image = background("Hasil Web", stamp)
    draw = ImageDraw.Draw(image)
    heading(draw, "03  /  Katalog Web", "Hasil scraping tampil sebagai katalog")
    text(draw, (61, 226), "30 BUKU", "body_bold", GOLD)
    text(draw, (61, 273), "Sampul sesuai judul", "body", WHITE)
    text(draw, (61, 313), "Harga dalam rupiah", "body", WHITE)
    text(draw, (61, 353), "Pencarian & filter", "body", WHITE)
    text(draw, (61, 393), "Sortir harga", "body", WHITE)
    text(draw, (61, 468), "Buka file:", "small", MUTED)
    text(draw, (61, 496), "output\\index.html", "mono", GREEN)
    preview = screenshot.copy()
    preview.thumbnail((820, 530), Image.Resampling.LANCZOS)
    x = 420 + (790 - preview.width) // 2
    y = 205 + (448 - preview.height) // 2
    rounded(draw, (404, 191, 1220, 654), PANEL, LINE)
    image.paste(preview, (x, y))
    return image


def results_scene(stamp, records):
    image = background("Dataset & Backup", stamp)
    draw = ImageDraw.Draw(image)
    heading(draw, "04  /  Hasil", "30 record berhasil dikumpulkan")
    premium = sum(row["category"] == "Premium" for row in records)
    standard = len(records) - premium
    values = [
        (str(len(records)), "TOTAL BUKU"),
        (str(premium), "PREMIUM*"),
        (str(standard), "STANDARD*"),
        ("£37.21", "RATA-RATA GBP"),
    ]
    for i, (value, label) in enumerate(values):
        x = 58 + i * 294
        rounded(draw, (x, 221, x + 267, 331), PANEL, LINE)
        text(draw, (x + 134, 250), value, "heading", GOLD, anchor="mm")
        text(draw, (x + 134, 300), label, "small", MUTED, anchor="mm")
    rounded(draw, (58, 362, 1220, 594), PANEL_ALT)
    text(draw, (84, 384), "BERKAS HASIL", "small", GOLD)
    items = [
        ("output\\hasil_scraping.csv", "30 baris · judul · harga GBP · tautan · sampul"),
        ("output\\laporan.txt", "Ringkasan pengambilan"),
        ("backup\\backup_data.zip", "CSV · index.html · laporan.txt · raw_data.txt"),
    ]
    y = 425
    for path, description in items:
        text(draw, (84, y), path, "mono_bold", WHITE)
        text(draw, (570, y + 2), description, "small", MUTED)
        y += 48
    text(draw, (61, 619), "*Premium jika harga > £30; Standard jika ≤ £30 — klasifikasi harga, bukan genre.", "small", MUTED)
    return image


def closing_scene(stamp):
    image = background("Tanya Jawab", stamp)
    draw = ImageDraw.Draw(image)
    text(draw, (61, 144), "RINGKASAN", "small", GOLD)
    text(draw, (59, 202), "Ambil.", "title", WHITE)
    text(draw, (59, 266), "Bersihkan.", "title", WHITE)
    text(draw, (59, 330), "Organisasikan.", "title", WHITE)
    text(draw, (62, 421), "Web scraping  ·  Regex  ·  CSV/TXT  ·  Backup ZIP", "body", MUTED)
    rounded(draw, (745, 185, 1218, 505), PANEL, LINE)
    text(draw, (981, 241), "TERIMA KASIH", "subtitle", GOLD, anchor="mm")
    text(draw, (981, 326), "Tanya", "title", WHITE, anchor="mm")
    text(draw, (981, 386), "jawab", "title", WHITE, anchor="mm")
    text(draw, (62, 548), "Muhammad Tafzil Rimzal  ·  312310529", "body_bold", WHITE)
    text(draw, (62, 588), "Demo ringkas tanpa narasi audio  ·  bahan tanya jawab tersedia di naskah demo", "small", MUTED)
    return image


def encode(scenes):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    command = [
        ffmpeg,
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        f"{WIDTH}x{HEIGHT}",
        "-pix_fmt",
        "rgb24",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "22",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(OUT),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    total_frames = sum(int(duration * FPS) for _, duration in scenes)
    frame_number = 0
    try:
        assert process.stdin is not None
        for scene, duration in scenes:
            base = scene.convert("RGB")
            count = int(duration * FPS)
            for frame_index in range(count):
                frame = base.copy()
                draw = ImageDraw.Draw(frame)
                progress = frame_number / max(1, total_frames - 1)
                draw.rectangle((0, 670, int(WIDTH * progress), 674), fill=GOLD)
                pulse_x = 56 + int((WIDTH - 112) * (frame_index / max(1, count - 1)))
                draw.ellipse((pulse_x, 660, pulse_x + 8, 668), fill=GOLD)
                process.stdin.write(frame.tobytes())
                frame_number += 1
        process.stdin.close()
        stderr = process.stderr.read() if process.stderr else b""
        code = process.wait(timeout=120)
        if code:
            raise RuntimeError(stderr.decode(errors="replace")[-3000:])
    except Exception:
        process.kill()
        raise


def main():
    log = run_scraper()
    csv_path = ROOT / "output" / "hasil_scraping.csv"
    with csv_path.open(encoding="utf-8-sig", newline="") as source:
        records = list(csv.DictReader(source))
    if len(records) != 30:
        raise ValueError(f"Expected 30 scraped records for demo, got {len(records)}.")
    screenshot = make_web_capture()
    scenes = [
        (title_scene("00:00  /  00:46"), 5),
        (workflow_scene("00:05  /  00:46"), 7),
        (terminal_scene("00:12  /  00:46", log), 9),
        (catalog_scene("00:21  /  00:46", screenshot), 11),
        (results_scene("00:32  /  00:46", records), 8),
        (closing_scene("00:40  /  00:46"), 6),
    ]
    encode(scenes)
    print(f"Video demonstrasi dibuat: {OUT}")
    print("Durasi: 46 detik · 1280×720 · MP4/H.264 · teks/caption, tanpa audio.")
    print(f"Ukuran file: {OUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
