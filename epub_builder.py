import os
import zipfile
import html
import uuid
from datetime import datetime
from typing import List, Dict, Optional

def create_epub(
    passages: List[Dict],
    output_path: str,
    book_title: str = "Arquímedes // Libro I: La Voluntad de las Cenizas",
    author: str = "Oscar Bueno",
    cover_image_path: Optional[str] = None,
    frontispiece_image_path: Optional[str] = None
) -> str:
    """
    Compila las escenas registradas en un libro EPUB 3 estándar,
    compatible con Apple Books, Moon+ Reader, Kindle, Kobo y cualquier lector.
    Incluye portada oficial, frontispicio y tabla de contenidos.
    """
    book_id = f"urn:uuid:{uuid.uuid4()}"
    now_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Autodetectar portadas si no se especifican
    base_assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "assets")
    if cover_image_path is None:
        cand = os.path.join(base_assets, "portada2.jpg")
        if os.path.exists(cand):
            cover_image_path = cand

    if frontispiece_image_path is None:
        cand2 = os.path.join(base_assets, "LaVoluntadDeLasCenizas.jpg")
        if os.path.exists(cand2):
            frontispiece_image_path = cand2

    # 1. Agrupar pasajes por capítulo
    capitulos: Dict[str, Dict] = {}
    for p in passages:
        c_num = p.get("chapter_number", 1)
        c_title = p.get("chapter_title") or f"Capítulo {c_num}"
        act_title = p.get("act_title") or "Acto I: La Academia"
        
        key = f"cap_{c_num}"
        if key not in capitulos:
            capitulos[key] = {
                "num": c_num,
                "title": c_title,
                "act": act_title,
                "paragraphs": []
            }
        
        # Separar párrafos
        raw_text = p.get("narrative", "")
        for block in raw_text.split("\n\n"):
            clean = block.strip()
            if clean:
                capitulos[key]["paragraphs"].append(clean)

    if not capitulos:
        # Fallback si todavía no hay escenas registradas
        capitulos["cap_1"] = {
            "num": 1,
            "title": "Capítulo 1: El Umbral de la Academia",
            "act": "Acto I: La Academia",
            "paragraphs": ["En el umbral de hierro y ceniza de la Academia, Oscar dio su primer paso..."]
        }

    # Ordenar capítulos numéricamente
    sorted_caps = sorted(capitulos.values(), key=lambda c: c["num"])

    # 2. Generar el archivo ZIP / EPUB
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as epub:
        # A. Archivo mimetype DEBE ser el primero y SIN compresión
        epub.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)

        # B. META-INF/container.xml
        container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
        epub.writestr("META-INF/container.xml", container_xml)

        # C. OEBPS/style.css
        style_css = """
body {
    font-family: "Georgia", "Merriweather", "Times New Roman", serif;
    font-size: 1.05em;
    line-height: 1.75;
    margin: 5% 8%;
    color: #1a1612;
    background-color: #fbf9f4;
}
.cover-page {
    margin: 0;
    padding: 0;
    text-align: center;
    background-color: #080808;
}
.cover-img {
    max-width: 100%;
    max-height: 100vh;
    height: auto;
}
.title-container {
    text-align: center;
    margin-top: 15%;
    margin-bottom: 20%;
}
.frontispiece-img {
    max-width: 82%;
    border-radius: 6px;
    margin-bottom: 2.5em;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.main-title {
    font-size: 2.3em;
    font-weight: bold;
    letter-spacing: 0.14em;
    margin-bottom: 0.25em;
    text-transform: uppercase;
    color: #111;
}
.sub-title {
    font-size: 1.2em;
    font-style: italic;
    color: #8c5b23;
    margin-bottom: 2em;
}
.author-name {
    font-size: 1em;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #444;
}
.epigraph-box {
    margin: 3em auto;
    padding: 1.5em;
    border-left: 2px solid #8c5b23;
    max-width: 75%;
    font-style: italic;
    color: #3b2f25;
}
.epigraph-author {
    text-align: right;
    font-size: 0.9em;
    letter-spacing: 0.08em;
    margin-top: 0.5em;
    color: #8c5b23;
}
.act-header {
    text-align: center;
    font-size: 0.85em;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: #8c5b23;
    margin-top: 3em;
    margin-bottom: 0.5em;
}
.chapter-title {
    text-align: center;
    font-size: 1.6em;
    font-weight: normal;
    letter-spacing: 0.05em;
    margin-bottom: 2em;
    color: #111;
}
p {
    text-indent: 1.5em;
    margin-top: 0;
    margin-bottom: 0.6em;
    text-align: justify;
}
p.first-p {
    text-indent: 0;
}
p.first-p::first-letter {
    font-size: 2.2em;
    float: left;
    line-height: 0.8;
    margin-right: 0.1em;
    font-weight: bold;
    color: #8c5b23;
}
.divider {
    text-align: center;
    margin: 2em auto;
    color: #aaa;
    font-size: 1.2em;
}
"""
        epub.writestr("OEBPS/style.css", style_css)

        manifest_items = [
            '<item id="style" href="style.css" media-type="text/css"/>',
            '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
            '<item id="titlepage" href="titlepage.xhtml" media-type="application/xhtml+xml"/>'
        ]
        spine_items = []
        meta_cover = ""

        # D. Portada Exterior (si existe)
        has_cover = False
        if cover_image_path and os.path.exists(cover_image_path):
            has_cover = True
            epub.write(cover_image_path, "OEBPS/images/cover.jpg")
            manifest_items.append('<item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>')
            manifest_items.append('<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="cover"/>')
            meta_cover = '<meta name="cover" content="cover-image"/>'

            cover_html = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es">
<head>
    <title>Portada</title>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body class="cover-page">
    <div>
        <img class="cover-img" src="images/cover.jpg" alt="Portada"/>
    </div>
</body>
</html>"""
            epub.writestr("OEBPS/cover.xhtml", cover_html)

        # E. Frontispicio Interior (si existe)
        frontispiece_img_html = ""
        if frontispiece_image_path and os.path.exists(frontispiece_image_path):
            epub.write(frontispiece_image_path, "OEBPS/images/frontispiece.jpg")
            manifest_items.append('<item id="frontispiece-image" href="images/frontispiece.jpg" media-type="image/jpeg"/>')
            frontispiece_img_html = '<img class="frontispiece-img" src="images/frontispiece.jpg" alt="Frontispicio"/>'

        # F. OEBPS/titlepage.xhtml
        titlepage_html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="es">
<head>
    <title>{html.escape(book_title)}</title>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <div class="title-container">
        {frontispiece_img_html}
        <h1 class="main-title">ARQUÍMEDES</h1>
        <p class="sub-title">Libro I: La Voluntad de las Cenizas</p>
        <p class="author-name">POR {html.escape(author.upper())}</p>
        
        <div class="epigraph-box">
            <p>«Dame un punto de apoyo y moveré el mundo.»</p>
            <p class="epigraph-author">— ARQUÍMEDES</p>
        </div>
        <div class="divider">✦ ✦ ✦</div>
    </div>
</body>
</html>"""
        epub.writestr("OEBPS/titlepage.xhtml", titlepage_html)
        spine_items.append('<itemref idref="titlepage"/>')

        # G. Capítulos individuales
        nav_points = []
        for idx, cap in enumerate(sorted_caps, start=1):
            file_name = f"chapter_{idx}.xhtml"
            item_id = f"chap_{idx}"

            manifest_items.append(f'<item id="{item_id}" href="{file_name}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{item_id}"/>')
            nav_points.append(f'<li><a href="{file_name}">{html.escape(cap["title"])}</a></li>')

            paragraphs_html = []
            for p_idx, para in enumerate(cap["paragraphs"]):
                p_class = ' class="first-p"' if p_idx == 0 else ""
                paragraphs_html.append(f'<p{p_class}>{html.escape(para)}</p>')

            chapter_content = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="es">
<head>
    <title>{html.escape(cap["title"])}</title>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <div class="act-header">{html.escape(cap["act"])}</div>
    <h2 class="chapter-title">{html.escape(cap["title"])}</h2>
    {"".join(paragraphs_html)}
</body>
</html>"""
            epub.writestr(f"OEBPS/{file_name}", chapter_content)

        # H. OEBPS/nav.xhtml (Navegación e Índice)
        nav_html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="es">
<head>
    <title>Índice</title>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <nav epub:type="toc" id="toc">
        <h1>ÍNDICE DE CAPÍTULOS</h1>
        <ol>
            {"".join(nav_points)}
        </ol>
    </nav>
</body>
</html>"""
        epub.writestr("OEBPS/nav.xhtml", nav_html)

        # I. OEBPS/content.opf (Paquete Maestro)
        content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:identifier id="BookId">{book_id}</dc:identifier>
        <dc:title>{html.escape(book_title)}</dc:title>
        <dc:language>es</dc:language>
        <dc:creator>{html.escape(author)}</dc:creator>
        <meta property="dcterms:modified">{now_iso}</meta>
        {meta_cover}
    </metadata>
    <manifest>
        {"".join(manifest_items)}
    </manifest>
    <spine>
        {"".join(spine_items)}
    </spine>
</package>"""
        epub.writestr("OEBPS/content.opf", content_opf)

    return output_path
