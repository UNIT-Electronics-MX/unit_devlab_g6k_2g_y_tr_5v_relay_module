
import os
import re
import subprocess
import markdown2
import yaml
import shutil
import glob
from datetime import datetime
from zoneinfo import ZoneInfo


def markdown_table_to_latex(md_table):
    try:
        lines = [line.strip() for line in md_table.strip().splitlines() if '|' in line]
        header = lines[0].strip('|').split('|')
        rows = [line.strip('|').split('|') for line in lines[2:]]

        # Construir formato: 'c' para todas menos la última como 'X' (mejor distribución)
        col_formats = ["c"] * (len(header) - 1) + [">{\\RaggedRight\\arraybackslash}X"]

        latex = "\\rowcolors{2}{white}{rowalt}\n"
        latex += "\\begin{tabularx}{\\textwidth}{|" + "|".join(col_formats) + "|}\n\\hline\n"
        latex += "\\rowcolor{headergray}\n"
        latex += " & ".join(h.strip() for h in header) + r" \\" + "\n\\hline\n"

        for row in rows:
            row = [cell.strip() for cell in row]
            if len(row) != len(header):
                row += [''] * (len(header) - len(row))
            latex += " & ".join(row) + r" \\" + "\n"

        latex += "\\hline\n\\end{tabularx}\n"
        return latex

    except Exception as e:
        return f"\\textit{{Error parsing table: {str(e)}}}"


        
def markdown_links_to_latex_list(text):
    items = re.findall(r'- \[(.*?)\]\((.*?)\)', text)
    if not items:
        return ""  # <- evita entorno vacío
    return "\\begin{itemize}\n" + "\n".join([f"\\item \\href{{{url}}}{{{label}}}" for label, url in items]) + "\n\\end{itemize}"


def markdown_bullets_to_latex(text):
    lines = text.strip().splitlines()
    items = [
        line.strip()[2:].strip()
        for line in lines
        if line.strip().startswith('-') and len(line.strip()[2:].strip()) > 0
    ]
    if not items:
        return ""
    return "\\begin{itemize}\n" + "\n".join([f"\\item {item}" for item in items]) + "\n\\end{itemize}"


def fix_paragraphs(text):
    return text.replace('\n\n', '\n\n\\par\n\n')

def fix_linebreaks_for_lists(text):
    lines = text.splitlines()
    return "\n".join(line + r"\\ " if line.strip().startswith('-') else line for line in lines)

def extract_section(heading, content):
    pattern = rf'##+\s*{re.escape(heading)}\s+(.*?)(?=\n##|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extract_links_section(heading, content):
    section = extract_section(heading, content)
    return markdown_links_to_latex_list(section)


def extract_table(heading, content):
    pattern = rf'##+\s*{re.escape(heading)}\s*\n+((?:\|.*\n)+)'
    match = re.search(pattern, content, re.IGNORECASE)
    return markdown_table_to_latex(match.group(1)) if match else "No table."




def format_images_with_titles(content):
    pattern = r'##\s*(.*?)\s*\n\s*!\[.*?\]\((.*?)\)'
    matches = re.findall(pattern, content)
    code = ""
    for i, (title, path) in enumerate(matches):
        code += (
            "\\newpage\n"
            "\\vspace*{3em}\n"  # espacio antes del título
            f"\\section*{{{title}}}\n"
            "\\vspace{1em}\n"
            "\\begin{center}\n"
            f"\\includegraphics[width=0.75\\textwidth,keepaspectratio]{{{path}}}\n"
            "\\end{center}\n"
        )
    return code

def parse_readme_md(path):

        # Obtener fecha local en Ciudad de México
    cdmx_now = datetime.now(ZoneInfo("America/Mexico_City"))
    formatted_date = cdmx_now.strftime("%Y-%m-%d %H:%M")

    # Copiar archivos de esquemático a docs/
    print("🔄 Copiando archivos de esquemático...")
    copied_schematic_files = copy_schematic_to_docs()

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Actualizar enlaces de esquemático si se copiaron archivos
    if copied_schematic_files:
        print("🔄 Actualizando enlaces de esquemático...")
        content = update_schematic_links(content, copied_schematic_files)

    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    frontmatter_match = re.match(r'^---(.*?)---', content, re.DOTALL)
    frontmatter = yaml.safe_load(frontmatter_match.group(1)) if frontmatter_match else {}
    content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)


    image_matches = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
    image_product = next((path for alt, path in image_matches if "product" in alt.lower()), "")
    image_paths = [path for _, path in image_matches]
    if not image_product and image_paths:
        image_product = image_paths[0]
        if not os.path.exists(image_product):
            print(f"⚠️ Advertencia: La imagen principal no fue encontrada en la ruta: {image_product}")


    pin_table_match = re.search(r'## Pin.*?Layout\n((?:\|.*\n)+)', content)
    pin_table = markdown_table_to_latex(pin_table_match.group(1)) if pin_table_match else "No table."

    downloads = re.findall(r'- \[(.*?)\]\((.*?)\)', content)
    downloads_latex = "\\n".join([f"\\item \\href{{{link}}}{{{text}}}" for text, link in downloads])

    date_used = frontmatter.get("modified", formatted_date)

    data = {
        "LOGO": frontmatter.get("logo", "images/logo_unit.png"),
        "TITLE": frontmatter.get("title", "Untitled"),
        "VERSION": frontmatter.get("version", "v1.0"),
        "DATE": formatted_date,

        "SUBTITLE": frontmatter.get("subtitle", "Product Brief"),
        "INTRODUCTION": fix_paragraphs(extract_section("Introduction", content)),

        "FUNCTIONAL": fix_linebreaks_for_lists(extract_section("Functional Description", content)),
        "ELECTRICAL": fix_linebreaks_for_lists(extract_section("Electrical Characteristics & Signal Overview", content)),
        "FEATURES": fix_linebreaks_for_lists(extract_section("Features", content)),
        "APPLICATIONS": fix_linebreaks_for_lists(extract_section("Applications", content)),

        "PIN_TABLE": extract_table("Pin & Connector Layout", content),
        "R11_TABLE": extract_table(" Current", content),
        "R10_TABLE": extract_table(" Current Limit", content),

        "USAGE": markdown_bullets_to_latex(extract_section("Usage", content)),
        "DOWNLOADS": extract_links_section("Downloads", content),
        "PURCHASE": extract_links_section("Purchase", content),
        "IMAGES": format_images_with_titles(content),

        "IMAGE_PRODUCT": image_product,
        "OUTPUT_NAME": frontmatter.get("output", "generated_product_brief"),
    }
    

    # Agregar tablas personalizadas después de definir 'data'
    custom_tables = {
        "INTERFACE_TABLE": "Interface Overview",
        "SUPPORTS_TABLE": "Supports",
        "AVR_TABLE": "Firmware Modes: AVR Programmer",
        "CMSIS_TABLE": "Firmware Modes: CMSIS-DAP Debugger",
        "CPLD_TABLE": "Firmware Modes: CPLD Programmer"
    }

    for key, title in custom_tables.items():
        data[key] = extract_table(title, content)

    return data


def render_latex(template_path, output_path, replacements):
    with open(template_path, 'r', encoding='utf-8') as f:
        tex = f.read()
    for key, value in replacements.items():
        tex = tex.replace(f'<<{key}>>', value)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(tex)

        
def compile_pdf(tex_file):
    try:
        for _ in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory=build', tex_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'  # <- esta línea soluciona el problema
            )
            if result.returncode != 0:
                print("⚠️ LaTeX compiló con errores:")
                print(result.stdout)
                print(result.stderr)
                if not os.path.exists("build/" + os.path.splitext(os.path.basename(tex_file))[0] + ".pdf"):
                    raise subprocess.CalledProcessError(result.returncode, result.args)
    except subprocess.CalledProcessError as e:
        print(f"❌ LaTeX falló con código {e.returncode}")
        raise


def clean_aux_files(output_name):
    base = os.path.splitext(output_name)[0]
    exts = [".aux", ".log", ".out", ".toc"]
    for ext in exts:
        path = f"{base}{ext}"
        if os.path.exists(path):
            os.remove(path)


def copy_schematic_to_docs():
    """
    Copia automáticamente los archivos de esquemático desde hardware/ a docs/
    y actualiza los enlaces relativos para que funcionen desde el PDF generado.
    """
    # Buscar archivos de esquemático en la carpeta hardware
    hardware_path = "../../hardware/"
    docs_path = "docs/"  # Directorio local docs/
    
    # Crear la carpeta docs si no existe
    os.makedirs(docs_path, exist_ok=True)
    
    # Buscar archivos PDF de esquemático
    schematic_files = glob.glob(os.path.join(hardware_path, "*sch*.pdf"))
    
    copied_files = []
    for schematic_file in schematic_files:
        filename = os.path.basename(schematic_file)
        dest_path = os.path.join(docs_path, filename)
        
        try:
            shutil.copy2(schematic_file, dest_path)
            print(f"✅ Esquemático copiado: {filename} -> docs/")
            copied_files.append(filename)
        except Exception as e:
            print(f"⚠️ Error copiando {filename}: {e}")
    
    return copied_files


def update_schematic_links(content, copied_files):
    """
    Actualiza los enlaces de esquemático en el contenido para que apunten a docs/
    en lugar de hardware/
    """
    updated_content = content
    
    for filename in copied_files:
        # Actualizar enlaces relativos desde hardware/ a docs/
        hardware_pattern = rf'\[([^\]]*)\]\(\.\./\.\./hardware/{re.escape(filename)}\)'
        docs_replacement = rf'[\1](docs/{filename})'
        updated_content = re.sub(hardware_pattern, docs_replacement, updated_content)
        
        # También manejar rutas sin ../.. al inicio
        hardware_pattern2 = rf'\[([^\]]*)\]\(hardware/{re.escape(filename)}\)'
        docs_replacement2 = rf'[\1](docs/{filename})'
        updated_content = re.sub(hardware_pattern2, docs_replacement2, updated_content)
    
    return updated_content

if __name__ == "__main__":
    data = parse_readme_md("README.md")  # asegúrate de definir 'data' aquí
    output_name = data["OUTPUT_NAME"]    # luego la usas aquí

    output_tex = f"build/{output_name}.tex"
    os.makedirs("build", exist_ok=True)

    render_latex("product_brief_template.tex", output_tex, data)
    compile_pdf(output_tex)
    clean_aux_files(f"build/{output_name}")
    
    # Copiar el PDF generado a la carpeta docs con el nombre del product brief
    source_pdf = f"build/{output_name}.pdf"
    docs_pdf = "../../docs/unit_relay_module_g6k_2g_y_tr_dc5_product_brief.pdf"
    
    if os.path.exists(source_pdf):
        try:
            shutil.copy2(source_pdf, docs_pdf)
            print(f"✅ PDF copiado a docs: {docs_pdf}")
        except Exception as e:
            print(f"⚠️ Error copiando PDF a docs: {e}")
    
    print(f"🎉 Proceso completado. PDF disponible en:")
    print(f"   - build/{output_name}.pdf")
    print(f"   - ../../docs/unit_relay_module_g6k_2g_y_tr_dc5_product_brief.pdf")