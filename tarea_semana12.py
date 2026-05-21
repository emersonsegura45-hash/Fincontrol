from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors

OUTPUT = "/home/user/Fincontrol/Tarea_Semana12_ConcentracionSolar.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    rightMargin=2.5*cm,
    leftMargin=2.5*cm,
    topMargin=2.5*cm,
    bottomMargin=2.5*cm,
)

styles = getSampleStyleSheet()

titulo = ParagraphStyle(
    "titulo",
    parent=styles["Title"],
    fontSize=14,
    spaceAfter=4,
    textColor=colors.HexColor("#1a1a2e"),
)
subtitulo = ParagraphStyle(
    "subtitulo",
    parent=styles["Normal"],
    fontSize=11,
    spaceAfter=10,
    textColor=colors.HexColor("#555555"),
    alignment=TA_CENTER,
)
pregunta = ParagraphStyle(
    "pregunta",
    parent=styles["Normal"],
    fontSize=11,
    spaceBefore=14,
    spaceAfter=4,
    fontName="Helvetica-Bold",
    textColor=colors.HexColor("#1a1a2e"),
)
respuesta = ParagraphStyle(
    "respuesta",
    parent=styles["Normal"],
    fontSize=10.5,
    spaceAfter=6,
    leading=15,
    alignment=TA_JUSTIFY,
    textColor=colors.HexColor("#222222"),
)
formula = ParagraphStyle(
    "formula",
    parent=styles["Normal"],
    fontSize=10.5,
    spaceAfter=4,
    leading=15,
    leftIndent=20,
    fontName="Helvetica-Oblique",
    textColor=colors.HexColor("#333366"),
)

story = []

story.append(Paragraph("Semana 12: Límites físicos de concentración solar", titulo))
story.append(Paragraph("Curso: Óptica Geométrica para Energía Solar", subtitulo))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
story.append(Spacer(1, 0.3*cm))

# --- P1 ---
story.append(Paragraph(
    "1. ¿Cuál es la fórmula para el factor de concentración de un sistema 2D y uno 3D?",
    pregunta
))
story.append(Paragraph(
    "El <b>factor de concentración</b> (C) se define como la relación entre el área de apertura "
    "del concentrador y el área de salida (o receptor). Dependiendo de la dimensionalidad del sistema:",
    respuesta
))
story.append(Paragraph(
    "Para un sistema <b>2D</b> (concentrador lineal), la concentración se da solo en una dirección, "
    "por lo que se comparan anchos en lugar de áreas:",
    respuesta
))
story.append(Paragraph("C<sub>2D</sub> = a<sub>entrada</sub> / a<sub>salida</sub>", formula))
story.append(Paragraph(
    "Para un sistema <b>3D</b> (concentrador de punto focal), la concentración actúa en dos "
    "dimensiones, y se comparan áreas:",
    respuesta
))
story.append(Paragraph("C<sub>3D</sub> = A<sub>entrada</sub> / A<sub>salida</sub>", formula))
story.append(Paragraph(
    "En ambos casos, un valor mayor de C indica mayor concentración de la radiación sobre el receptor.",
    respuesta
))

# --- P2 ---
story.append(Paragraph(
    "2. ¿Cuál es el límite del factor de concentración para un sistema 3D (usando el tamaño angular del sol)?",
    pregunta
))
story.append(Paragraph(
    "El Sol tiene un semiángulo aparente de aproximadamente θ<sub>s</sub> ≈ 4.65 mrad (≈ 0.267°). "
    "Aplicando el límite termodinámico (conservación de étendue óptico), el máximo factor de "
    "concentración para un sistema 3D en el vacío (n = 1) es:",
    respuesta
))
story.append(Paragraph("C<sub>3D,max</sub> = 1 / sin²(θ<sub>s</sub>) ≈ 46,200", formula))
story.append(Paragraph(
    "Este valor es el límite teórico absoluto. En la práctica, los concentradores reales están "
    "muy por debajo de este número debido a imperfecciones ópticas y geométricas.",
    respuesta
))

# --- P3 ---
story.append(Paragraph(
    "3. ¿Cuál es el límite del factor de concentración para un sistema 2D (usando el tamaño angular del sol)?",
    pregunta
))
story.append(Paragraph(
    "Para un sistema 2D, el límite teórico máximo (en vacío) es:",
    respuesta
))
story.append(Paragraph("C<sub>2D,max</sub> = 1 / sin(θ<sub>s</sub>) ≈ 215", formula))
story.append(Paragraph(
    "Este límite es mucho menor que el del sistema 3D porque la concentración solo ocurre "
    "en una dimensión. Un colector parabólico de canal, por ejemplo, es un sistema 2D.",
    respuesta
))

# --- P4 ---
story.append(Paragraph(
    "4. ¿Cómo afecta el índice de refracción al factor de concentración solar? ¿Cómo podemos usar esto a nuestro favor?",
    pregunta
))
story.append(Paragraph(
    "Si el receptor está inmerso en un medio con índice de refracción n > 1 (por ejemplo vidrio, "
    "con n ≈ 1.5), los límites de concentración se incrementan:",
    respuesta
))
story.append(Paragraph("C<sub>3D,max</sub> = n² / sin²(θ<sub>s</sub>)", formula))
story.append(Paragraph("C<sub>2D,max</sub> = n / sin(θ<sub>s</sub>)", formula))
story.append(Paragraph(
    "Esto se puede aprovechar colocando el receptor directamente acoplado a un elemento de "
    "vidrio o material transparente de alto índice de refracción. De esta forma, el límite "
    "teórico se multiplica por n² (en 3D) o por n (en 2D) sin violar ninguna ley termodinámica. "
    "Esto se utiliza, por ejemplo, en concentradores con CPC inmersos en vidrio.",
    respuesta
))

# --- P5 ---
story.append(Paragraph(
    "5. Si la aceptancia es menor al ángulo solar, el factor de concentración será mayor. ¿Esto es bueno o malo? Explique.",
    pregunta
))
story.append(Paragraph(
    "Generalmente es <b>malo</b>. Si el ángulo de aceptancia del concentrador es menor que el "
    "ángulo aparente del Sol (θ<sub>s</sub> ≈ 4.65 mrad), solo una fracción del disco solar "
    "entra al concentrador. Aunque matemáticamente el factor C puede ser mayor, en realidad "
    "se está perdiendo parte de la radiación directa disponible.",
    respuesta
))
story.append(Paragraph(
    "Esto implica también que el sistema de seguimiento solar (tracking) debe ser extremadamente "
    "preciso, ya que cualquier pequeño error de apuntamiento causa pérdidas significativas de energía. "
    "En resumen: mayor C en este caso viene a costa de menor eficiencia de captación y mayor "
    "complejidad de seguimiento, lo cual en la mayoría de aplicaciones no es deseable.",
    respuesta
))

# --- P6 ---
story.append(Paragraph(
    "6. Nombre tres tipos de sistemas de concentración 2D y brinde fotografías de cada uno.",
    pregunta
))
story.append(Paragraph(
    "<b>a) Colector de Canal Parabólico (CCP):</b> Consiste en un espejo con perfil parabólico "
    "extruido en una dirección. Concentra la luz solar en una línea focal donde se ubica un tubo "
    "receptor. Es el sistema de concentración lineal más utilizado en plantas termosolares.",
    respuesta
))
story.append(Paragraph(
    "[Imagen referencial: Vista de una planta de colectores de canal parabólico, con filas "
    "paralelas de espejos curvados orientados hacia el sol]",
    formula
))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "<b>b) Concentrador de Fresnel Lineal (LFC):</b> Usa múltiples espejos planos o ligeramente "
    "curvados dispuestos en filas, que reflejan la luz hacia un receptor fijo ubicado sobre ellos. "
    "Es más económico y simple que el CCP pero tiene menor eficiencia óptica.",
    respuesta
))
story.append(Paragraph(
    "[Imagen referencial: Instalación de Fresnel lineal vista desde el costado, con el receptor "
    "elevado sobre los espejos planos]",
    formula
))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "<b>c) Concentrador Parabólico Compuesto (CPC) de Winston:</b> Concentrador no formador de "
    "imagen formado por dos secciones parabólicas enfrentadas. Puede funcionar sin seguimiento "
    "o con seguimiento mínimo. Capta toda la radiación dentro del ángulo de aceptancia.",
    respuesta
))
story.append(Paragraph(
    "[Imagen referencial: Sección transversal en forma de V invertida del CPC con el receptor "
    "en la parte inferior]",
    formula
))

# --- P7 ---
story.append(Paragraph(
    "7. Nombre tres tipos de sistemas de concentración 3D y brinde fotografías de cada uno.",
    pregunta
))
story.append(Paragraph(
    "<b>a) Disco Parabólico (Paraboloide de Revolución):</b> Espejo en forma de paraboloide que "
    "concentra toda la radiación incidente en un punto focal. Alcanza los mayores factores de "
    "concentración (entre 1,000 y 3,000). Suele ir acoplado a un motor Stirling o un receptor "
    "térmico de alta temperatura.",
    respuesta
))
story.append(Paragraph(
    "[Imagen referencial: Disco parabólico solar con motor Stirling en el punto focal, montado "
    "sobre un sistema de seguimiento de dos ejes]",
    formula
))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "<b>b) Torre Solar con Campo de Heliostatos:</b> Un gran campo de espejos planos (heliostatos) "
    "sigue individualmente al Sol y refleja la luz hacia un receptor central ubicado en lo alto "
    "de una torre. Factores de concentración típicos entre 500 y 1,000.",
    respuesta
))
story.append(Paragraph(
    "[Imagen referencial: Vista aérea de una torre solar rodeada de cientos de heliostatos, "
    "con la luz concentrada visible en el receptor de la torre]",
    formula
))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "<b>c) Lente de Fresnel Circular:</b> Lente plana escalonada que aproxima la forma de una "
    "lente convexa con mucho menor grosor y peso. Concentra la radiación en un punto focal. "
    "Se usa principalmente en sistemas fotovoltaicos de concentración (CPV).",
    respuesta
))
story.append(Paragraph(
    "[Imagen referencial: Lente de Fresnel circular transparente con el perfil escalonado "
    "visible, y punto de luz concentrado por debajo]",
    formula
))

# --- P8 ---
story.append(Paragraph(
    "8. ¿Qué es el concentrador ideal de Winston y cuál es su otro nombre? ¿Solo hay concentradores de Winston 2D?",
    pregunta
))
story.append(Paragraph(
    "El <b>concentrador ideal de Winston</b>, también llamado <b>Concentrador Parabólico Compuesto "
    "(CPC)</b>, es un concentrador no formador de imagen que alcanza el límite termodinámico de "
    "concentración para su ángulo de aceptancia. Fue desarrollado por Roland Winston en los años "
    "1970. Su perfil está formado por dos parábolas cuyos focos coinciden con los bordes del "
    "receptor, lo que garantiza que toda la radiación que entra dentro del ángulo de aceptancia "
    "llega al receptor.",
    respuesta
))
story.append(Paragraph(
    "Respecto a si solo existen en 2D: <b>No, también existen versiones 3D.</b> Se puede obtener "
    "un CPC 3D rotando el perfil 2D alrededor del eje óptico, obteniendo un concentrador en "
    "forma de trompeta o campana truncada. Este concentrador 3D de Winston alcanza el límite "
    "C<sub>3D,max</sub> = 1/sin²(θ<sub>a</sub>) para su ángulo de aceptancia θ<sub>a</sub>. "
    "También existen variantes como el CPC con reflector externo o los concentradores de Winston "
    "de geometría rectangular (diedros), que son esencialmente 3D.",
    respuesta
))

story.append(Spacer(1, 0.5*cm))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "Emerson Segura — Óptica Geométrica para Energía Solar — Semana 12",
    subtitulo
))

doc.build(story)
print(f"PDF generado: {OUTPUT}")
