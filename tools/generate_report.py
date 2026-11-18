import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


REPO_URL = "https://github.com/Gabriel-XDDDD/prj_withdrawal"
ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "output" / "pdf" / "Informe_Entrega_3_actualizado.pdf"

INK = colors.HexColor("#173C34")
ACCENT = colors.HexColor("#2F7564")
PALE = colors.HexColor("#E8F1ED")
MUTED = colors.HexColor("#5A6B65")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("TitleE3", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=24, leading=29, textColor=INK, spaceAfter=7 * mm))
styles.add(ParagraphStyle("SubtitleE3", parent=styles["Normal"], fontName="Helvetica", fontSize=12, leading=17, textColor=MUTED, spaceAfter=7 * mm))
styles.add(ParagraphStyle("H1E3", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=INK, spaceBefore=4 * mm, spaceAfter=3 * mm))
styles.add(ParagraphStyle("H2E3", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=ACCENT, spaceBefore=3 * mm, spaceAfter=2 * mm))
styles.add(ParagraphStyle("BodyE3", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=colors.HexColor("#26332F"), spaceAfter=2.5 * mm))
styles.add(ParagraphStyle("SmallE3", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED))
styles.add(ParagraphStyle("CodeE3", parent=styles["Code"], fontName="Courier", fontSize=8, leading=11, borderColor=colors.HexColor("#CAD8D3"), borderWidth=0.6, borderPadding=4 * mm, backColor=colors.HexColor("#F5F8F6"), spaceBefore=2 * mm, spaceAfter=3 * mm))


def p(text, style="BodyE3"):
    return Paragraph(text, styles[style])


def header_footer(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.rect(0, height - 18 * mm, width, 18 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(18 * mm, height - 11.5 * mm, "ENTREGA 3  |  prj_withdrawal")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(width - 18 * mm, height - 11.5 * mm, "Aplicación web - Go - BDD")
    canvas.setStrokeColor(colors.HexColor("#CEDBD6"))
    canvas.line(18 * mm, 15 * mm, width - 18 * mm, 15 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(18 * mm, 9.5 * mm, "Universidad Nacional de Ingeniería - Ingeniería de Software")
    canvas.drawRightString(width - 18 * mm, 9.5 * mm, f"Página {doc.page}")
    canvas.restoreState()


def table(rows, widths, header=INK):
    result = Table(rows, colWidths=widths, repeatRows=1)
    result.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D7D2")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return result


def build(ci_status):
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=25 * mm, bottomMargin=20 * mm,
        title="Informe Entrega 3 - prj_withdrawal",
        author="Gabriel Eustaquio",
        subject="Aplicación web de retiro, abono e integridad JSON",
    )

    story = [
        Spacer(1, 7 * mm),
        p("Refactorización de la aplicación", "TitleE3"),
        p("Entrega 3: aplicación web de retiro, abono e integridad del historial JSON", "SubtitleE3"),
        table([
            [p("PROYECTO", "SmallE3"), p("prj_withdrawal")],
            [p("AUTOR", "SmallE3"), p("Gabriel Eustaquio")],
            [p("REPOSITORIO", "SmallE3"), p(f'<link href="{REPO_URL}" color="#2F7564">{REPO_URL}</link>')],
        ], [35 * mm, 135 * mm], ACCENT),
        Spacer(1, 5 * mm),
        p("I. Objetivo", "H1E3"),
        p("Transformar la aplicación de consola en una aplicación web local sin duplicar reglas de negocio. El servidor Go reutiliza el cálculo monetario y el almacenamiento JSON de las iteraciones anteriores."),
        p("II. Evolución incremental", "H1E3"),
        table([
            [p("Entrega", "SmallE3"), p("Resultado", "SmallE3")],
            [p("1"), p("Retiro y abono desde consola.")],
            [p("2"), p("Persistencia del saldo e historial de éxito, fallo y error.")],
            [p("3"), p("Formulario web, tabla de movimientos, pruebas HTTP y publicación en GitHub.")],
        ], [30 * mm, 140 * mm]),
        p("III. Criterios de aceptación", "H1E3"),
        p("1. GET / muestra el saldo persistido y el historial."),
        p("2. POST /movimiento permite retirar o abonar y responde con redirección HTTP 303."),
        p("3. Un movimiento válido actualiza el saldo una sola vez."),
        p("4. Un monto inválido o un retiro sin fondos conserva el saldo y queda registrado."),
        p("5. Al reiniciar el servidor se recupera y valida cuenta.json."),
        p("IV. Organización", "H1E3"),
        p("account.go: reglas monetarias en céntimos.<br/>store.go: validación y escritura atómica.<br/>web.go e index.html: rutas y presentación.<br/>features/: especificaciones Gherkin.<br/>.github/workflows/tests.yml: integración continua."),
        PageBreak(),
        p("Flujo web e integridad", "TitleE3"),
        p("Del formulario al saldo persistido y al historial verificable", "SubtitleE3"),
        p("V. Interacción desde el navegador", "H1E3"),
        table([
            [p("Paso", "SmallE3"), p("Comportamiento", "SmallE3")],
            [p("1"), p("El navegador consulta GET / y recibe la vista actual.")],
            [p("2"), p("El usuario ingresa el monto y pulsa Abonar o Retirar.")],
            [p("3"), p("POST /movimiento llama a Store.move con la operación recibida.")],
            [p("4"), p("El estado se guarda y el servidor redirige nuevamente a GET /.")],
        ], [25 * mm, 145 * mm]),
        p("VI. Conservación de los datos", "H1E3"),
        p("Store serializa el acceso con un mutex. Para cada intento vuelve a calcular el evento esperado, actualiza saldo e historial en memoria y escribe ambos en un archivo temporal. Tras sincronizarlo, lo renombra como cuenta.json."),
        p("Al reabrir se comprueban la secuencia de identificadores, los eventos recalculados, el saldo final, la presencia de fechas UTC y su orden cronológico. Un archivo inconsistente se rechaza sin sobrescribirlo."),
        p("VII. Estados registrados", "H1E3"),
        table([
            [p("Estado", "SmallE3"), p("Ejemplo", "SmallE3"), p("Efecto", "SmallE3")],
            [p("éxito"), p("Retiro 200 desde 234.56"), p("Saldo 34.56")],
            [p("fallo"), p("Retiro 200 desde 34.56"), p("Saldo intacto")],
            [p("error"), p("Abono 0 o negativo"), p("Saldo intacto")],
        ], [30 * mm, 85 * mm, 55 * mm]),
        p("VIII. Alcance", "H1E3"),
        p("La entrega administra una cuenta académica local. No modela autenticación de clientes, inventario físico de billetes ni despliegue de producción. El README delimita este alcance y explica cómo reiniciar la demostración."),
        PageBreak(),
        p("Verificación y publicación", "TitleE3"),
        p("Pruebas automatizadas, ejecución local y repositorio GitHub", "SubtitleE3"),
        p("IX. Pruebas ejecutadas", "H1E3"),
        table([
            [p("Comprobación", "SmallE3"), p("Resultado", "SmallE3")],
            [p("go test -race -count=1 -cover ./..."), p("Aprobado; cobertura 51.3%")],
            [p("go vet ./..."), p("Sin observaciones")],
            [p("Behave"), p("7 escenarios y 21 pasos aprobados")],
            [p("Formulario web"), p("Retiro, abono, error, fondos insuficientes y reinicio verificados")],
            [p("Integración continua"), p(ci_status)],
        ], [82 * mm, 88 * mm], ACCENT),
        p("X. Repositorio GitHub", "H1E3"),
        p("El código, las pruebas, el workflow de CI, la documentación y este informe se publican en:"),
        p(f'<link href="{REPO_URL}" color="#2F7564"><b>{REPO_URL}</b></link>', "H2E3"),
        p("El README presenta la evolución de las tres entregas, la arquitectura, las reglas de negocio, los comandos de macOS y el enlace directo al informe."),
        p("XI. Ejecución reproducible", "H1E3"),
        p("git clone https://github.com/Gabriel-XDDDD/prj_withdrawal.git<br/>cd prj_withdrawal<br/>go test -v ./...<br/>go run .", "CodeE3"),
        p("Abra http://localhost:8080. Para Gherkin, cree un entorno Python, instale behave==1.3.3 y ejecute python -m behave."),
        p("XII. Conclusión", "H1E3"),
        p("La aplicación web conserva las reglas y la integridad de las iteraciones anteriores, ofrece una demostración reproducible y publica evidencia verificable mediante GitHub Actions. El repositorio queda preparado como entrega académica autocontenida."),
        p("Referencia", "H2E3"),
        p("J. Medianero Acosta, codeLAB Semana 7c, Gherkin, BDD y Cucumber; consigna del proyecto prj_withdrawal, acápite 4."),
    ]

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUTPUT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ci-status", default="Workflow configurado; verificación local aprobada")
    args = parser.parse_args()
    build(args.ci_status)
