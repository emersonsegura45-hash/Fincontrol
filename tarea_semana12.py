from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Image, KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors

OUTPUT = "/home/user/Fincontrol/Tarea_Semana12_ConcentracionSolar.pdf"
FOTOS  = "/home/user/Fincontrol/fotos"

doc = SimpleDocTemplate(
    OUTPUT, pagesize=letter,
    rightMargin=2.5*cm, leftMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

styles = getSampleStyleSheet()

titulo = ParagraphStyle("titulo", parent=styles["Title"],
    fontSize=13, spaceAfter=3, textColor=colors.HexColor("#1a1a2e"))
subtitulo = ParagraphStyle("sub", parent=styles["Normal"],
    fontSize=10, spaceAfter=10, textColor=colors.HexColor("#555555"),
    alignment=TA_CENTER)
pregunta = ParagraphStyle("preg", parent=styles["Normal"],
    fontSize=10.5, spaceBefore=12, spaceAfter=3,
    fontName="Helvetica-Bold", textColor=colors.HexColor("#1a1a2e"))
resp = ParagraphStyle("resp", parent=styles["Normal"],
    fontSize=10, spaceAfter=5, leading=14,
    alignment=TA_JUSTIFY, textColor=colors.HexColor("#222222"))
formula_st = ParagraphStyle("frm", parent=styles["Normal"],
    fontSize=10, leftIndent=20, fontName="Helvetica-Oblique",
    textColor=colors.HexColor("#333366"), spaceAfter=5)
caption = ParagraphStyle("cap", parent=styles["Normal"],
    fontSize=8.5, alignment=TA_CENTER, spaceAfter=6,
    textColor=colors.HexColor("#666666"), fontName="Helvetica-Oblique")


def foto(nombre, w=12*cm, h=7*cm):
    return Image(f"{FOTOS}/{nombre}", width=w, height=h)


story = []

story.append(Paragraph("Semana 12: Límites físicos de concentración solar", titulo))
story.append(Paragraph("Curso: Óptica Geométrica para Energía Solar", subtitulo))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
story.append(Spacer(1, 0.3*cm))

# ── 1 ──────────────────────────────────────────────────────────────────
story.append(Paragraph(
    "1. ¿Cuál es la fórmula del factor de concentración para un sistema 2D y uno 3D?", pregunta))
story.append(Paragraph(
    "El factor de concentración C es la relación entre el área de apertura y el área del receptor. "
    "Para un sistema <b>2D</b> se comparan anchos: C = a<sub>entrada</sub> / a<sub>salida</sub>. "
    "Para un sistema <b>3D</b> se comparan áreas: C = A<sub>entrada</sub> / A<sub>salida</sub>.", resp))

# ── 2 ──────────────────────────────────────────────────────────────────
story.append(Paragraph(
    "2. ¿Cuál es el límite del factor de concentración para un sistema 3D?", pregunta))
story.append(Paragraph(
    "Usando el semiángulo solar θ<sub>s</sub> ≈ 4.65 mrad y el principio de conservación de étendue, "
    "el máximo teórico para un sistema 3D (en aire, n = 1) es:", resp))
story.append(Paragraph("C<sub>3D,max</sub> = 1 / sin²(θ<sub>s</sub>) ≈ 46,200", formula_st))

# ── 3 ──────────────────────────────────────────────────────────────────
story.append(Paragraph(
    "3. ¿Cuál es el límite del factor de concentración para un sistema 2D?", pregunta))
story.append(Paragraph(
    "Para un sistema 2D el límite es menor porque la concentración solo ocurre en una dimensión:", resp))
story.append(Paragraph("C<sub>2D,max</sub> = 1 / sin(θ<sub>s</sub>) ≈ 215", formula_st))

# ── 4 ──────────────────────────────────────────────────────────────────
story.append(Paragraph(
    "4. ¿Cómo afecta el índice de refracción al factor de concentración? ¿Cómo usarlo a nuestro favor?",
    pregunta))
story.append(Paragraph(
    "Si el receptor está en un medio con índice n > 1, el límite sube a C<sub>3D</sub> = n²/sin²(θ<sub>s</sub>) "
    "y C<sub>2D</sub> = n/sin(θ<sub>s</sub>). Esto se puede aprovechar acoplando el receptor a un bloque "
    "de vidrio (n ≈ 1.5), lo que aumenta el límite teórico sin violar ninguna ley termodinámica.", resp))

# ── 5 ──────────────────────────────────────────────────────────────────
story.append(Paragraph(
    "5. Si la aceptancia es menor al ángulo solar el factor C es mayor, ¿esto es bueno o malo?", pregunta))
story.append(Paragraph(
    "Es malo. Aunque C matemáticamente sube, en la práctica parte de la radiación solar queda fuera "
    "del ángulo de aceptancia y se pierde. Además el sistema de seguimiento debe ser más preciso, "
    "lo que aumenta los costos y la complejidad.", resp))

# ── 6 ──────────────────────────────────────────────────────────────────
story.append(Paragraph(
    "6. Nombre tres tipos de sistemas de concentración 2D y brinde fotografías de cada uno.", pregunta))

story.append(Paragraph(
    "<b>a) Colector de Canal Parabólico (CCP):</b> Espejo con perfil parabólico que concentra la luz "
    "en un tubo receptor a lo largo de la línea focal. Es el más utilizado en plantas termosolares.", resp))
story.append(KeepTogether([
    foto("2d_canal_parabolico.png"),
    Paragraph("Fig. 1 — Colector de Canal Parabólico. Los rayos paralelos se reflejan hacia el tubo receptor en el foco.", caption),
]))

story.append(Paragraph(
    "<b>b) Concentrador de Fresnel Lineal (LFC):</b> Filas de espejos planos o curvados que reflejan "
    "la luz hacia un receptor fijo ubicado arriba. Más barato que el CCP aunque con menor eficiencia óptica.", resp))
story.append(KeepTogether([
    foto("2d_fresnel_lineal.png"),
    Paragraph("Fig. 2 — Fresnel Lineal. Cada espejo plano refleja la radiación hacia el receptor central fijo.", caption),
]))

story.append(Paragraph(
    "<b>c) Concentrador Parabólico Compuesto — CPC (Winston):</b> Formado por dos secciones parabólicas "
    "que dirigen toda la luz del ángulo de aceptancia hacia el receptor. Puede funcionar sin seguimiento.", resp))
story.append(KeepTogether([
    foto("2d_cpc_winston.png", w=10*cm, h=9*cm),
    Paragraph("Fig. 3 — CPC de Winston. Las dos parábolas captan toda la radiación dentro del ángulo de aceptancia.", caption),
]))

# ── 7 ──────────────────────────────────────────────────────────────────
story.append(Paragraph(
    "7. Nombre tres tipos de sistemas de concentración 3D y brinde fotografías de cada uno.", pregunta))

story.append(Paragraph(
    "<b>a) Disco Parabólico:</b> Espejo en forma de paraboloide de revolución que concentra la luz en "
    "un punto focal. Alcanza los mayores factores C (hasta ~3,000), generalmente acoplado a un motor Stirling.", resp))
story.append(KeepTogether([
    foto("3d_disco_parabolico.png"),
    Paragraph("Fig. 4 — Disco Parabólico. Toda la superficie refleja hacia el receptor en el punto focal.", caption),
]))

story.append(Paragraph(
    "<b>b) Torre Solar con Heliostatos:</b> Campo de espejos planos (heliostatos) que reflejan individualmente "
    "la luz hacia un receptor en lo alto de una torre central. Factor de concentración típico entre 500 y 1,000.", resp))
story.append(KeepTogether([
    foto("3d_torre_solar.png"),
    Paragraph("Fig. 5 — Torre Solar. Cada heliostato sigue al sol de forma independiente y refleja la luz hacia la torre.", caption),
]))

story.append(Paragraph(
    "<b>c) Lente de Fresnel Circular:</b> Lente plana escalonada que aproxima una lente convexa con menor "
    "grosor y peso. Concentra la luz en un punto focal y se usa en sistemas fotovoltaicos de concentración (CPV).", resp))
story.append(KeepTogether([
    foto("3d_fresnel_circular.png"),
    Paragraph("Fig. 6 — Lente de Fresnel Circular. El perfil escalonado refracta los rayos hacia un único punto focal.", caption),
]))

# ── 8 ──────────────────────────────────────────────────────────────────
story.append(Paragraph(
    "8. ¿Qué es el concentrador ideal de Winston y cuál es su otro nombre? ¿Solo hay versiones 2D?",
    pregunta))
story.append(Paragraph(
    "El concentrador de Winston también se llama <b>CPC (Concentrador Parabólico Compuesto)</b>. "
    "Es el concentrador no formador de imagen que alcanza el límite termodinámico para su ángulo "
    "de aceptancia. No solo existe en 2D: rotando el perfil alrededor del eje óptico se obtiene "
    "una versión 3D en forma de trompeta, que alcanza C<sub>3D,max</sub> = 1/sin²(θ<sub>a</sub>).", resp))

story.append(Spacer(1, 0.6*cm))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("Emerson Segura — Óptica Geométrica para Energía Solar — Semana 12", subtitulo))

doc.build(story)
print(f"PDF generado: {OUTPUT}")
