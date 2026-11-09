#!/usr/bin/env python3
"""Generate a concise, presentation-ready UTS slide deck."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent / "Presentasi_UTS_Automation_Systems_Final.pptx"

NAVY = RGBColor(11, 17, 32)
PANEL = RGBColor(21, 31, 50)
PANEL_LIGHT = RGBColor(27, 40, 63)
GOLD = RGBColor(230, 189, 119)
WHITE = RGBColor(243, 246, 251)
MUTED = RGBColor(158, 171, 192)
GREEN = RGBColor(151, 206, 174)
LINE = RGBColor(54, 68, 91)
FONT = "Aptos"


def add_box(slide, x, y, w, h, fill, rounded=True, line=None):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line or fill
    if rounded:
        shape.adjustments[0] = 0.12
    return shape


def add_text(
    slide,
    text,
    x,
    y,
    w,
    h,
    size=18,
    color=WHITE,
    bold=False,
    font=FONT,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.MIDDLE,
    margin=0,
):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    frame.vertical_anchor = valign
    for index, line in enumerate(text.split("\n")):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.alignment = align
        paragraph.space_after = Pt(0)
        paragraph.space_before = Pt(0)
        run = paragraph.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
    return shape


def add_background(slide, number, section):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = NAVY
    add_box(slide, 0, 0, 0.09, 7.5, GOLD, rounded=False)
    add_text(slide, "BOOKFOLIO  /  AUTOMATION SYSTEMS", 0.55, 0.26, 6, 0.24, 9, MUTED, True)
    add_text(slide, section.upper(), 9.0, 0.26, 3.75, 0.24, 9, GOLD, True, align=PP_ALIGN.RIGHT)
    add_box(slide, 0.55, 7.08, 12.25, 0.012, LINE, rounded=False)
    add_text(slide, "Muhammad Tafzil Rimzal  ·  312310529", 0.58, 7.15, 8, 0.18, 8, MUTED)
    add_text(slide, f"{number:02d}", 12.17, 7.13, 0.55, 0.22, 9, GOLD, True, align=PP_ALIGN.RIGHT)


def add_title(slide, eyebrow, title, subtitle=None):
    add_text(slide, eyebrow.upper(), 0.7, 0.78, 11.9, 0.25, 10, GOLD, True)
    add_text(slide, title, 0.7, 1.12, 11.9, 0.62, 28, WHITE, True)
    if subtitle:
        add_text(slide, subtitle, 0.72, 1.79, 11.8, 0.42, 14, MUTED)


def add_card(slide, x, y, w, h, title, body, number=None, accent=GOLD):
    add_box(slide, x, y, w, h, PANEL, line=LINE)
    if number is not None:
        add_text(slide, number, x + 0.22, y + 0.19, 0.48, 0.32, 13, accent, True)
        title_x = x + 0.78
    else:
        title_x = x + 0.24
    add_text(slide, title, title_x, y + 0.16, w - (title_x - x) - 0.2, 0.4, 16, WHITE, True)
    add_text(
        slide,
        body,
        x + 0.24,
        y + 0.67,
        w - 0.48,
        h - 0.82,
        12,
        MUTED,
        valign=MSO_ANCHOR.TOP,
    )


def make_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # 1. Cover
    slide = prs.slides.add_slide(blank)
    add_background(slide, 1, "Presentasi UTS")
    add_box(slide, 9.25, 1.2, 3.0, 4.9, PANEL, line=LINE)
    add_text(slide, "01", 9.65, 1.7, 2.2, 1.25, 66, GOLD, True, align=PP_ALIGN.CENTER)
    add_box(slide, 9.82, 3.14, 1.84, 0.025, LINE, rounded=False)
    add_text(slide, "AUTOMATION\nSYSTEMS", 9.55, 3.52, 2.4, 0.85, 17, WHITE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "UNIVERSITAS PELITA BANGSA  ·  2025/2026", 0.8, 1.4, 7.6, 0.3, 11, GOLD, True)
    add_text(slide, "Online Book\nCatalog Organizer", 0.78, 2.0, 7.8, 1.65, 37, WHITE, True)
    add_text(
        slide,
        "Otomatisasi pengumpulan, pembersihan,\ndan pengorganisasian katalog buku",
        0.82,
        3.88,
        7.2,
        0.82,
        18,
        MUTED,
    )
    add_text(slide, "Muhammad Tafzil Rimzal", 0.82, 5.25, 6, 0.34, 17, WHITE, True)
    add_text(slide, "NIM 312310529  ·  Kelompok 01 (individu, disetujui dosen)", 0.82, 5.65, 7.2, 0.3, 12, MUTED)
    add_text(slide, "15 MENIT   ·   5 PENJELASAN  /  7 DEMO  /  3 TANYA JAWAB", 0.82, 6.42, 8.4, 0.26, 10, GOLD, True)

    # 2. Problem and goal
    slide = prs.slides.add_slide(blank)
    add_background(slide, 2, "Masalah")
    add_title(slide, "01  /  Konteks", "Dari katalog publik ke data yang siap ditata", "Tujuan: mengurangi pengambilan dan pencatatan buku secara manual.")
    add_card(slide, 0.72, 2.55, 3.82, 2.15, "Masalah", "Judul dan harga tersebar di halaman katalog; pencarian dan pencatatan manual menyita waktu.", "A")
    add_card(slide, 4.76, 2.55, 3.82, 2.15, "Sumber", "Books to Scrape — situs latihan publik untuk demonstrasi web scraping.", "B", GREEN)
    add_card(slide, 8.8, 2.55, 3.82, 2.15, "Target", "Ambil minimal 30 buku, saring judul, simpan terstruktur, dan siapkan backup.", "C")
    add_box(slide, 0.72, 5.12, 11.9, 0.9, PANEL_LIGHT)
    add_text(slide, "HASIL YANG DIHARAPKAN", 1.0, 5.28, 2.65, 0.2, 9, GOLD, True)
    add_text(slide, "Dataset rapi  ·  katalog mudah dicari  ·  proses dapat dijalankan ulang", 1.0, 5.58, 10.8, 0.26, 16, WHITE, True)

    # 3. Workflow
    slide = prs.slides.add_slide(blank)
    add_background(slide, 3, "Alur Solusi")
    add_title(slide, "02  /  Alur", "Satu proses dari halaman web sampai backup", "Pengambilan data berlanjut ke halaman berikutnya sampai target tercapai.")
    stages = [
        ("01", "Ambil halaman", "requests"),
        ("02", "Parse katalog", "BeautifulSoup"),
        ("03", "Bersihkan & filter", "Regex"),
        ("04", "Simpan hasil", "CSV / TXT / HTML"),
        ("05", "Arsipkan", "ZIP"),
    ]
    x0, width, gap = 0.72, 2.25, 0.2
    for idx, (num, title, caption) in enumerate(stages):
        x = x0 + idx * (width + gap)
        add_box(slide, x, 3.0, width, 1.8, PANEL, line=LINE)
        add_text(slide, num, x + 0.2, 3.2, 0.55, 0.32, 14, GOLD, True)
        add_text(slide, title, x + 0.2, 3.68, width - 0.4, 0.45, 16, WHITE, True)
        add_text(slide, caption, x + 0.2, 4.2, width - 0.4, 0.28, 11, MUTED)
        if idx < len(stages) - 1:
            add_text(slide, "›", x + width + 0.02, 3.62, 0.18, 0.42, 24, GOLD, True, align=PP_ALIGN.CENTER)
    add_text(slide, "OUTPUT", 0.86, 5.42, 0.8, 0.2, 9, GOLD, True)
    add_text(slide, "data/raw_data.txt    ·    output/hasil_scraping.csv    ·    output/laporan.txt    ·    output/index.html    ·    backup/backup_data.zip", 0.86, 5.75, 11.7, 0.42, 13, WHITE)

    # 4. Required course topics
    slide = prs.slides.add_slide(blank)
    add_background(slide, 4, "Materi Wajib")
    add_title(slide, "03  /  Integrasi Materi", "Lima materi wajib diterapkan di satu aplikasi")
    topics = [
        ("CH 09", "Regular Expressions", "Ekstraksi angka harga\nFilter keyword judul"),
        ("CH 10", "File I/O", "Baca dan tulis\nCSV serta TXT"),
        ("CH 11", "Organisasi File", "Folder otomatis\nBackup ZIP"),
        ("CH 12", "CLI", "--url · --keyword\n--limit · --backup"),
        ("CH 13", "Web Scraping", "requests + BeautifulSoup\nPaginasi katalog"),
    ]
    for idx, (chapter, title, body) in enumerate(topics):
        col, row = idx % 3, idx // 3
        x = 0.72 + col * 4.04
        y = 2.35 + row * 1.8
        if idx == 3:
            x = 2.72
        elif idx == 4:
            x = 6.76
        add_box(slide, x, y, 3.78, 1.48, PANEL, line=LINE)
        add_text(slide, chapter, x + 0.22, y + 0.17, 0.8, 0.22, 10, GOLD, True)
        add_text(slide, title, x + 0.22, y + 0.5, 3.35, 0.32, 16, WHITE, True)
        add_text(slide, body, x + 0.22, y + 0.91, 3.35, 0.44, 11, MUTED)

    # 5. Results
    slide = prs.slides.add_slide(blank)
    add_background(slide, 5, "Hasil Scraping")
    add_title(slide, "04  /  Hasil", "30 buku berhasil dikumpulkan", "Pengambilan terakhir dari Books to Scrape · harga sumber tetap tersimpan dalam GBP.")
    metrics = [("30", "RECORD"), ("20", "PREMIUM*"), ("10", "STANDARD*"), ("£37.21", "RATA-RATA")]
    for idx, (value, label) in enumerate(metrics):
        x = 0.72 + idx * 3.04
        add_box(slide, x, 2.52, 2.78, 1.42, PANEL, line=LINE)
        add_text(slide, value, x + 0.15, 2.72, 2.48, 0.56, 27, GOLD, True, align=PP_ALIGN.CENTER)
        add_text(slide, label, x + 0.15, 3.38, 2.48, 0.25, 9, MUTED, True, align=PP_ALIGN.CENTER)
    add_box(slide, 0.72, 4.33, 11.9, 1.35, PANEL_LIGHT)
    add_text(slide, "Setiap record", 1.0, 4.53, 1.7, 0.28, 13, GOLD, True)
    add_text(slide, "Judul  ·  harga  ·  kategori harga  ·  URL buku  ·  URL sampul", 2.85, 4.51, 8.9, 0.3, 15, WHITE, True)
    add_text(slide, "*Premium jika harga > £30; Standard jika ≤ £30. Kategori harga, bukan genre.", 1.0, 5.08, 10.8, 0.25, 11, MUTED)
    add_text(slide, "Katalog web: konversi IDR memakai kurs acuan tetap, dengan tanggal kurs ditampilkan.", 0.75, 6.05, 11.8, 0.3, 12, MUTED)

    # 6. Live demo handoff
    slide = prs.slides.add_slide(blank)
    add_background(slide, 6, "Demo Langsung · 7 Menit")
    add_title(slide, "05  /  Demonstrasi", "Berikutnya: jalankan dan periksa hasil")
    add_box(slide, 0.74, 2.2, 11.85, 0.95, RGBColor(18, 28, 44), line=LINE)
    add_text(slide, r".\.venv\Scripts\python.exe main.py --limit 30 --backup", 1.02, 2.48, 11.3, 0.32, 18, GREEN, True, font="Cascadia Code")
    demo = [
        ("01:30", "CLI & hasil terminal"),
        ("01:45", "Katalog: sampul, harga IDR"),
        ("01:00", "Cari, filter, urutkan"),
        ("01:00", "CSV & laporan ringkas"),
        ("01:00", "Data mentah & backup ZIP"),
        ("00:45", "Validasi & penanganan error"),
    ]
    for idx, (time, text) in enumerate(demo):
        col, row = idx % 3, idx // 3
        x, y = 0.74 + col * 4.02, 3.62 + row * 1.04
        add_text(slide, time, x, y, 0.75, 0.25, 11, GOLD, True)
        add_text(slide, text, x + 0.83, y, 2.98, 0.38, 13, WHITE, True)
    add_text(slide, "Semua file demo tersedia lewat pintasan pada folder dokumentasi/presentasi.", 0.78, 6.15, 11.5, 0.28, 12, MUTED)

    # 7. Q&A
    slide = prs.slides.add_slide(blank)
    add_background(slide, 7, "Tanya Jawab · 3 Menit")
    add_title(slide, "06  /  Penutup", "Terima kasih", "Saya siap menjawab pertanyaan.")
    add_text(slide, "Q&A", 0.78, 2.35, 4.0, 1.05, 55, GOLD, True)
    add_text(slide, "TOPIK YANG SIAP DIBAHAS", 0.82, 3.72, 4.5, 0.25, 10, MUTED, True)
    qas = [
        "Regex & validasi data",
        "Paginasi dan batas scraping",
        "CSV, folder, dan backup ZIP",
        "Kategori harga & kurs IDR",
        "Batasan data dan pengembangan",
    ]
    for idx, item in enumerate(qas):
        y = 2.5 + idx * 0.62
        add_box(slide, 5.25, y, 6.95, 0.46, PANEL, line=LINE)
        add_text(slide, f"0{idx + 1}", 5.5, y + 0.06, 0.42, 0.22, 10, GOLD, True)
        add_text(slide, item, 6.05, y + 0.06, 5.8, 0.25, 13, WHITE, True)
    add_text(slide, "Catatan jujur: belum ada penulis pada data kartu; Premium/Standard adalah klasifikasi harga.", 0.82, 5.5, 11.5, 0.45, 13, MUTED)
    add_text(slide, "Muhammad Tafzil Rimzal  ·  312310529", 0.82, 6.35, 7.2, 0.3, 13, WHITE, True)

    prs.core_properties.title = "Online Book Catalog Organizer - UTS Automation Systems"
    prs.core_properties.subject = "Presentasi UTS 15 menit: 5 menit penjelasan, 7 menit demo, 3 menit tanya jawab"
    prs.core_properties.author = "Muhammad Tafzil Rimzal"
    prs.core_properties.keywords = "Automation Systems, web scraping, Books to Scrape"
    prs.save(OUTPUT)
    print(f"PowerPoint dibuat: {OUTPUT}")


if __name__ == "__main__":
    make_deck()
