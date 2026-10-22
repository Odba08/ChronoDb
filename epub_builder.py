import os
import zipfile
import html
import uuid
from datetime import datetime
from typing import List, Dict

def create_epub(
    passages: List[Dict],
    output_path: str,
    book_title: str = "Arquímedes: La Voluntad de las Cenizas",
    author: str = "Oscar Bueno"
) -> str:
    """
    Compila las escenas registradas en un libro EPUB 3 estándar,
    compatible con Apple Books, Kindle, Kobo y cualquier lector.
    """
    book_id = f"urn:uuid:{uuid.uuid4()}"
    now_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # 1. Agrupar pasajes por capítulo
    capitulos: Dict[str, Dict] = {}
    for p in passages:
        c_num = p.get("chapter_number", 1)
        c_title = p.get("chapter_title") or f"Capítulo {c_num}"
        act_title = p.get("act_title") or "Acto I: La Puerta de Hierro y Ceniza"
        
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
            "act": "Acto I: La Puerta de Hierro y Ceniza",
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
    line-height: 1.7;
    margin: 5% 8%;
    color: #1a1a1a;
}
.cover-container {
    text-align: center;
    margin-top: 25%;
}
.main-title {
    font-size: 2.4em;
    font-weight: bold;
    letter-spacing: 0.12em;
    margin-bottom: 0.2em;
    text-transform: uppercase;
}
.sub-title {
    font-size: 1.3em;
    font-style: italic;
    color: #555;
    margin-bottom: 2.5em;
}
.author-name {
    font-size: 1.1em;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #333;
}
.act-header {
    text-align: center;
    font-size: 0.85em;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: #777;
    margin-top: 3em;
    margin-bottom: 0.5em;
}
.chapter-title {
    text-align: center;
    font-size: 1.6em;
    font-weight: normal;
    letter-spacing: 0.05em;
    margin-bottom: 2em;
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
}
.divider {
    text-align: center;
    margin: 2em auto;
    color: #aaa;
    font-size: 1.2em;
}
"""
        epub.writestr("OEBPS/style.css", style_css)

        # D. OEBPS/titlepage.xhtml
        titlepage_html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="es">
<head>
    <title>{html.escape(book_title)}</title>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <div class="cover-container">
        <h1 class="main-title">ARQUÍMEDES</h1>
        <p class="sub-title">La Voluntad de las Cenizas</p>
        <p class="author-name">POR {html.escape(author.upper())}</p>
        <div class="divider">✦ ✦ ✦</div>
    </div>
</body>
</html>"""
        epub.writestr("OEBPS/titlepage.xhtml", titlepage_html)

        # E. Capítulos individuales
        manifest_items = [
            '<item id="style" href="style.css" media-type="text/css"/>',
            '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
            '<item id="titlepage" href="titlepage.xhtml" media-type="application/xhtml+xml"/>'
        ]
        spine_items = [
            '<itemref idref="titlepage"/>'
        ]
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

        # F. OEBPS/nav.xhtml (Navegación e Índice)
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

        # G. OEBPS/content.opf (Paquete Maestro)
        content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:identifier id="BookId">{book_id}</dc:identifier>
        <dc:title>{html.escape(book_title)}</dc:title>
        <dc:language>es</dc:language>
        <dc:creator>{html.escape(author)}</dc:creator>
        <meta property="dcterms:modified">{now_iso}</meta>
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
