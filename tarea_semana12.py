from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Image, KeepTogether, ListFlowable, ListItem,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Registrar Liberation Sans (idéntica a Arial en métricas) ─────────────
BASE = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Arial",           BASE + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold",      BASE + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic",    BASE + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Arial-BoldItalic",BASE + "LiberationSans-BoldItalic.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Arial",
    normal="Arial", bold="Arial-Bold",
    italic="Arial-Italic", boldItalic="Arial-BoldItalic")

OUTPUT = "/home/user/Fincontrol/Tarea_Semana12_ConcentracionSolar.pdf"
FOTOS  = "/home/user/Fincontrol/fotos"

BLUE   = colors.HexColor("#2255aa")
DARK   = colors.HexColor("#1a1a1a")
GRAY   = colors.HexColor("#666666")

doc = SimpleDocTemplate(
    OUTPUT, pagesize=letter,
    rightMargin=2.5*cm, leftMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

# ── Estilos ───────────────────────────────────────────────────────────────
titulo = ParagraphStyle("titulo",
    fontName="Arial-Bold", fontSize=20,
    textColor=DARK, spaceAfter=6, leading=26)

meta = ParagraphStyle("meta",
    fontName="Arial-Bold", fontSize=12,
    textColor=DARK, spaceAfter=3, leading=16)

heading = ParagraphStyle("heading",
    fontName="Arial-Bold", fontSize=14,
    textColor=DARK, spaceBefore=14, spaceAfter=6, leading=18)

body = ParagraphStyle("body",
    fontName="Arial", fontSize=12,
    textColor=DARK, spaceAfter=6, leading=17,
    alignment=TA_JUSTIFY)

formula_c = ParagraphStyle("formula",
    fontName="Arial-Italic", fontSize=12,
    textColor=DARK, alignment=TA_CENTER,
    spaceAfter=8, leading=17)

bullet_item = ParagraphStyle("bullet",
    fontName="Arial", fontSize=12,
    textColor=DARK, leading=17,
    leftIndent=16, spaceAfter=4,
    alignment=TA_JUSTIFY)

caption = ParagraphStyle("cap",
    fontName="Arial-Italic", fontSize=9,
    textColor=GRAY, alignment=TA_CENTER,
    spaceAfter=8, leading=13)

footer = ParagraphStyle("footer",
    fontName="Arial-Italic", fontSize=10,
    textColor=GRAY, alignment=TA_CENTER,
    spaceBefore=20)

def foto(nombre, w=12*cm, h=7*cm):
    return Image(f"{FOTOS}/{nombre}", width=w, height=h)

def bullet(bold_part, rest):
    return Paragraph(f"• <b>{bold_part}</b> {rest}", bullet_item)

story = []

# ── Encabezado ────────────────────────────────────────────────────────────
story.append(Paragraph("Tarea Semana 12: Límites físicos de concentración solar", titulo))
story.append(HRFlowable(width="100%", thickness=1.2, color=DARK, spaceAfter=8))
story.append(Paragraph("<b>Estudiante:</b> Emerson Elias Segura Vargas", meta))
story.append(Paragraph("<b>Curso:</b> Óptica Geométrica para Energía Solar", meta))
story.append(Spacer(1, 0.3*cm))

# ── 1 ────────────────────────────────────────────────────────────────────
story.append(Paragraph("1. Fórmulas del factor de concentración", heading))
story.append(Paragraph(
    "El factor de concentración (<i>C</i>) es básicamente la relación entre qué tan grande es la "
    "entrada de luz comparada con el área donde finalmente se concentra.", body))
story.append(bullet("En 2D (Sistemas lineales):", "Comparamos anchos: C = a<sub>entrada</sub> / a<sub>salida</sub>."))
story.append(bullet("En 3D (Sistemas puntuales):", "Comparamos áreas: C = A<sub>entrada</sub> / A<sub>salida</sub>."))

# ── 2 ────────────────────────────────────────────────────────────────────
story.append(Paragraph("2. Límite para sistemas 3D", heading))
story.append(Paragraph(
    "Considerando el ángulo por el que llega la luz del sol (θ<sub>s</sub> ≈ <b>4.65 mrad</b>) "
    "y la conservación de <i>étendue</i>, el máximo teórico en aire es:", body))
story.append(Paragraph("<i>C<sub>3D,max</sub> = 1 / sin²(θ<sub>s</sub>) ≈ 46,200</i>", formula_c))

# ── 3 ────────────────────────────────────────────────────────────────────
story.append(Paragraph("3. Límite para sistemas 2D", heading))
story.append(Paragraph(
    "Como la concentración ocurre en una sola dimensión, el límite es más sencillo:", body))
story.append(Paragraph("<i>C<sub>2D,max</sub> = 1 / sin(θ<sub>s</sub>) ≈ 215</i>", formula_c))

# ── 4 ────────────────────────────────────────────────────────────────────
story.append(Paragraph("4. El índice de refracción (n)", heading))
story.append(Paragraph(
    "Si colocamos el receptor en un material como el vidrio (<b><i>n</i> ≈ 1.5</b>), podemos "
    "aumentar el límite. Las fórmulas se ajustan a:", body))
story.append(Paragraph(
    "<i>C<sub>3D</sub> = n² / sin²(θ<sub>s</sub>)   y   C<sub>2D</sub> = n / sin(θ<sub>s</sub>)</i>",
    formula_c))
story.append(Paragraph(
    "Es una estrategia física eficiente para mejorar el rendimiento sin romper leyes termodinámicas.",
    body))

# ── 5 ────────────────────────────────────────────────────────────────────
story.append(Paragraph("5. Aceptancia menor al ángulo solar", heading))
story.append(Paragraph(
    "No es recomendable. Aunque los valores teóricos de <i>C</i> aumenten, en la práctica perdemos "
    "luz que queda fuera del ángulo de aceptancia. Además, exige un sistema de seguimiento mucho "
    "más costoso y preciso.", body))

# ── 6 ────────────────────────────────────────────────────────────────────
story.append(Paragraph("6. Tres ejemplos de sistemas 2D", heading))

# 6a
story.append(bullet("Canal Parabólico (CCP):",
    "Espejo curvo que enfoca la luz en un tubo receptor. Muy común en plantas termosolares."))
story.append(KeepTogether([
    foto("2d_canal_parabolico.png"),
    Paragraph("Fig. 1 — Colector de Canal Parabólico: los rayos se reflejan hacia el tubo en el foco.", caption),
]))

# 6b
story.append(bullet("Fresnel Lineal (LFC):",
    "Filas de espejos planos que reflejan a un receptor superior. Más económico que el CCP, aunque menos eficiente."))
story.append(KeepTogether([
    foto("2d_fresnel_lineal.png"),
    Paragraph("Fig. 2 — Fresnel Lineal: cada espejo plano refleja la radiación hacia el receptor fijo superior.", caption),
]))

# 6c
story.append(bullet("CPC (Winston):",
    "Utiliza dos parábolas unidas para atrapar la luz. Su ventaja es que puede funcionar con menor precisión de seguimiento."))
story.append(KeepTogether([
    foto("2d_cpc_winston.png", w=10*cm, h=9*cm),
    Paragraph("Fig. 3 — CPC de Winston: las dos parábolas captan toda la radiación dentro del ángulo de aceptancia.", caption),
]))

# ── 7 ────────────────────────────────────────────────────────────────────
story.append(Paragraph("7. Tres ejemplos de sistemas 3D", heading))

# 7a
story.append(bullet("Disco Parabólico:",
    "Forma de plato que concentra todo en un punto, logrando factores de hasta 3,000."))
story.append(KeepTogether([
    foto("3d_disco_parabolico.png"),
    Paragraph("Fig. 4 — Disco Parabólico: paraboloide de revolución que enfoca la luz en un punto focal.", caption),
]))

# 7b
story.append(bullet("Torre Solar:",
    "Un campo de espejos (heliostatos) que apuntan a un receptor en una torre."))
story.append(KeepTogether([
    foto("3d_torre_solar.png"),
    Paragraph("Fig. 5 — Torre Solar con campo de heliostatos reflejando hacia el receptor en la torre.", caption),
]))

# 7c
story.append(bullet("Lente de Fresnel Circular:",
    "Lente delgada y plana usada en sistemas fotovoltaicos concentrados (CPV)."))
story.append(KeepTogether([
    foto("3d_fresnel_circular.png"),
    Paragraph("Fig. 6 — Lente de Fresnel Circular: perfil escalonado que refracta los rayos hacia un punto focal.", caption),
]))

# ── 8 ────────────────────────────────────────────────────────────────────
story.append(Paragraph("8. Concentrador de Winston (CPC)", heading))
story.append(Paragraph(
    "Es un concentrador no formador de imagen que alcanza el límite termodinámico para un ángulo "
    "dado. No es solo 2D: al rotar su perfil, obtenemos una versión 3D en forma de trompeta que "
    "alcanza <i>C<sub>3D,max</sub> = 1 / sin²(θ<sub>a</sub>)</i>.", body))

# ── Pie ───────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("Tarea entregada como parte de la evaluación de la semana 12.", footer))

doc.build(story)
print(f"PDF generado: {OUTPUT}")
