from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_BREAK
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'Informe_pruebas_y_resultados_ABP_Midely.docx'


def set_cell_shading(cell, fill):
    props = cell._tc.get_or_add_tcPr()
    shading = props.find(qn('w:shd'))
    if shading is None:
        shading = OxmlElement('w:shd')
        props.append(shading)
    shading.set(qn('w:fill'), fill)


def set_cell_borders(cell, color='D9D9D9', size='6'):
    props = cell._tc.get_or_add_tcPr()
    borders = props.first_child_found_in('w:tcBorders')
    if borders is None:
        borders = OxmlElement('w:tcBorders')
        props.append(borders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        tag = 'w:' + edge
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn('w:val'), 'single')
        element.set(qn('w:sz'), size)
        element.set(qn('w:space'), '0')
        element.set(qn('w:color'), color)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120):
    props = cell._tc.get_or_add_tcPr()
    margins = props.first_child_found_in('w:tcMar')
    if margins is None:
        margins = OxmlElement('w:tcMar')
        props.append(margins)
    for name, value in [('top', top), ('start', start), ('bottom', bottom), ('end', end)]:
        node = margins.find(qn('w:' + name))
        if node is None:
            node = OxmlElement('w:' + name)
            margins.append(node)
        node.set(qn('w:w'), str(value))
        node.set(qn('w:type'), 'dxa')


def set_repeat_table_header(row):
    tr_props = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement('w:tblHeader')
    tbl_header.set(qn('w:val'), 'true')
    tr_props.append(tbl_header)


def add_page_number(paragraph):
    run = paragraph.add_run()
    field_begin = OxmlElement('w:fldChar')
    field_begin.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = 'PAGE'
    field_end = OxmlElement('w:fldChar')
    field_end.set(qn('w:fldCharType'), 'end')
    run._r.append(field_begin)
    run._r.append(instr)
    run._r.append(field_end)


def set_run_font(run, name='Aptos', size=11, color='1F2937', bold=False, italic=False):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn('w:ascii'), name)
    run._element.get_or_add_rPr().rFonts.set(qn('w:hAnsi'), name)
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(color)
    run.bold = bold
    run.italic = italic


def style_document(doc):
    section = doc.sections[0]
    section.top_margin = Inches(0.78)
    section.bottom_margin = Inches(0.72)
    section.left_margin = Inches(0.82)
    section.right_margin = Inches(0.82)

    normal = doc.styles['Normal']
    normal.font.name = 'Aptos'
    normal._element.rPr.rFonts.set(qn('w:ascii'), 'Aptos')
    normal._element.rPr.rFonts.set(qn('w:hAnsi'), 'Aptos')
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor(31, 41, 55)
    normal.paragraph_format.space_after = Pt(7)
    normal.paragraph_format.line_spacing = 1.12

    for style_name, size, color, before, after in [
        ('Title', 24, '111827', 0, 12),
        ('Heading 1', 16, '111827', 16, 7),
        ('Heading 2', 12.5, '1E3A8A', 12, 5),
        ('Heading 3', 11, '374151', 9, 4),
    ]:
        style = doc.styles[style_name]
        style.font.name = 'Aptos Display' if style_name != 'Heading 3' else 'Aptos'
        style._element.rPr.rFonts.set(qn('w:ascii'), style.font.name)
        style._element.rPr.rFonts.set(qn('w:hAnsi'), style.font.name)
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor.from_string(color)
        style.font.bold = True
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

    title_ppr = doc.styles['Title']._element.get_or_add_pPr()
    title_border = title_ppr.find(qn('w:pBdr'))
    if title_border is not None:
        title_ppr.remove(title_border)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = footer.add_run('Midely  |  Informe académico  |  ')
    set_run_font(r, size=8.5, color='64748B')
    add_page_number(footer)
    for run in footer.runs:
        set_run_font(run, size=8.5, color='64748B')


def add_para(doc, text='', style=None, align=None, first_line=True, space_after=7):
    p = doc.add_paragraph(style=style)
    if text:
        r = p.add_run(text)
        set_run_font(r)
    if align is not None:
        p.alignment = align
    if first_line:
        p.paragraph_format.first_line_indent = Inches(0.25)
    p.paragraph_format.space_after = Pt(space_after)
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style='List Bullet' if level == 0 else 'List Bullet 2')
    r = p.add_run(text)
    set_run_font(r)
    p.paragraph_format.space_after = Pt(3)
    return p


def add_table(doc, headers, rows, widths=None, font_size=8.6):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    header = table.rows[0]
    header_props = header._tr.get_or_add_trPr()
    header_props.append(OxmlElement('w:cantSplit'))
    set_repeat_table_header(header)
    for i, title in enumerate(headers):
        cell = header.cells[i]
        set_cell_shading(cell, '1E3A8A')
        set_cell_borders(cell)
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        set_run_font(r, size=font_size, color='FFFFFF', bold=True)
        if widths:
            cell.width = Inches(widths[i])

    for row_index, row_data in enumerate(rows):
        row = table.add_row()
        row_props = row._tr.get_or_add_trPr()
        row_props.append(OxmlElement('w:cantSplit'))
        cells = row.cells
        for i, value in enumerate(row_data):
            cell = cells[i]
            set_cell_borders(cell)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if row_index % 2 == 1:
                set_cell_shading(cell, 'F3F6FA')
            if widths:
                cell.width = Inches(widths[i])
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(str(value))
            set_run_font(r, size=font_size, color='1F2937')
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def add_reference(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.first_line_indent = Inches(-0.35)
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(text)
    set_run_font(r, size=9.5)
    return p


doc = Document()
style_document(doc)

# Portada
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(90)
r = p.add_run('INFORME DE PRUEBAS Y RESULTADOS ABP')
set_run_font(r, size=12, color='4F46E5', bold=True)

p = doc.add_paragraph(style='Title')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Aplicación móvil híbrida Midely')
set_run_font(r, size=25, color='111827', bold=True)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Catálogo, autenticación, carrito y almacenamiento local con Ionic Angular y Capacitor')
set_run_font(r, size=12, color='475569')

doc.add_paragraph().paragraph_format.space_after = Pt(20)
for line in ['Producto académico de aprendizaje basado en proyecto', 'Código fuente preparado para Android e iOS', '17 de septiembre de 2026']:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(line)
    set_run_font(r, size=11, color='64748B')

doc.add_page_break()

# Opening
doc.add_heading('Resumen', level=1)
add_para(doc, 'El presente informe documenta la planeación, implementación y verificación de Midely, una tienda móvil híbrida desarrollada con Ionic, Angular y Capacitor. El producto integra un catálogo obtenido mediante un servicio API, autenticación de demostración, carrito de compras y almacenamiento local. La solución se preparó para Android e iOS, de acuerdo con el flujo multiplataforma descrito por Ionic Framework (s. f.) y Capacitor (s. f.).')
add_para(doc, 'La evidencia técnica disponible demuestra una compilación web de producción exitosa, lint sin errores, once pruebas unitarias aprobadas y la sincronización del proyecto nativo Android junto con la generación de la estructura iOS. La ejecución en un dispositivo Android físico y la compilación final en Xcode quedan como actividades de validación externa, debido a que requieren un dispositivo conectado y, para iOS, macOS con Xcode. En consecuencia, el informe diferencia los resultados ejecutados de las actividades preparadas para cierre.')

doc.add_heading('Contenido del informe', level=1)
add_table(doc, ['Sección', 'Propósito'], [
    ('Producto técnico', 'Explica la arquitectura, las funcionalidades y la evidencia en el código fuente.'),
    ('Estrategia de pruebas', 'Registra las pruebas automatizadas, de compilación y las validaciones previstas en emuladores y dispositivos.'),
    ('Lanzamiento y mantenimiento', 'Presenta las acciones requeridas para firma, publicación, seguridad, rendimiento y actualización.'),
    ('Resultados ABP', 'Recopila las etapas planeadas, ejecutadas, los resultados y las oportunidades pendientes.'),
], widths=[1.55, 5.65])

# 1
doc.add_heading('Descripción del producto', level=1)
add_para(doc, 'Midely representa una tienda en línea móvil con una interfaz adaptable a teléfonos y tabletas. La navegación se organiza en tres vistas: Tienda, Carrito y Cuenta. La separación de responsabilidades favorece la mantenibilidad y permite que cada flujo sea verificado de manera independiente, una práctica coherente con las recomendaciones de desarrollo híbrido de Khanna (2016).')

doc.add_heading('Arquitectura implementada', level=2)
add_table(doc, ['Componente', 'Responsabilidad', 'Evidencia'], [
    ('CatalogService', 'Consulta productos en DummyJSON, aplica límite de tiempo y usa datos de respaldo si la red falla.', 'src/app/services/catalog.service.ts'),
    ('AuthService', 'Valida correo y contraseña, crea una sesión mínima y la restaura desde Preferences.', 'src/app/services/auth.service.ts'),
    ('CartService', 'Administra altas, cantidades, eliminación, total y persistencia del carrito.', 'src/app/services/cart.service.ts'),
    ('Tab1Page', 'Muestra catálogo, búsqueda, categorías y acción para agregar productos.', 'src/app/tab1'),
    ('Tab2Page', 'Permite revisar cantidades y confirmar un pedido demostrativo.', 'src/app/tab2'),
    ('Tab3Page', 'Presenta el inicio y cierre de sesión con estado persistente.', 'src/app/tab3'),
    ('Capacitor', 'Integra el bundle web con los proyectos nativos Android e iOS.', 'android, ios, capacitor.config.ts'),
], widths=[1.25, 4.15, 1.8], font_size=8.2)

doc.add_heading('Funcionalidades verificables', level=2)
for item in [
    'El catálogo se carga desde una API y conserva una alternativa local para modo sin conexión.',
    'La búsqueda filtra por título y descripción, y la selección filtra por categoría.',
    'El carrito permite agregar el mismo producto varias veces, modificar cantidades y retirar productos.',
    'La sesión valida datos mínimos, no guarda la contraseña y persiste únicamente la información necesaria para la demostración.',
    'La aplicación usa Capacitor Preferences para conservar carrito y sesión entre aperturas.',
    'El proyecto contiene las carpetas android e ios y el identificador de aplicación se configuró como com.midely.store.',
]:
    add_bullet(doc, item)

# 2
doc.add_heading('Estrategia de pruebas', level=1)
add_para(doc, 'La estrategia combinó pruebas unitarias, validación estática, compilación web, sincronización Capacitor y preparación de escenarios móviles. La combinación permite identificar errores de lógica antes de revisar la interfaz en un emulador o dispositivo. La selección se relaciona con la necesidad de verificar el comportamiento multiplataforma y la integración con capacidades nativas, como recomiendan Capacitor (s. f.) y Android Studio Developers (s. f.).')

doc.add_heading('Pruebas ejecutadas', level=2)
add_table(doc, ['ID', 'Prueba', 'Resultado', 'Evidencia o correctivo'], [
    ('P01', 'Compilación web de producción', 'Aprobada', 'pnpm build; bundle generado en www.'),
    ('P02', 'Lint de Angular', 'Aprobada', 'Todos los archivos pasan linting.'),
    ('P03', 'Suite unitaria inicial', 'Aprobada', '9 archivos y 11 pruebas aprobadas.'),
    ('P04', 'Servicio API', 'Aprobada', 'Se valida la solicitud GET y el mapeo de productos.'),
    ('P05', 'Autenticación', 'Aprobada', 'Se validan credenciales inválidas, inicio y cierre de sesión.'),
    ('P06', 'Carrito', 'Aprobada', 'Se validan cantidades, total y eliminación.'),
    ('P07', 'Sincronización Android', 'Aprobada', 'Capacitor copia www y registra tres plugins nativos.'),
    ('P08', 'Estructura iOS', 'Aprobada', 'cap add ios genera ios/App y Package.swift.'),
    ('P09', 'APK debug', 'Aprobada con observación', 'assembleDebug fue exitoso; una recompilación posterior requiere JDK completo compatible.'),
], widths=[0.45, 1.85, 1.2, 3.7], font_size=8.1)

doc.add_heading('Casos de prueba funcional', level=2)
add_table(doc, ['Caso', 'Precondición', 'Acción', 'Resultado esperado', 'Estado'], [
    ('CF01', 'Aplicación abierta', 'Buscar un texto existente.', 'Solo aparecen productos coincidentes.', 'Aprobado por lógica y compilación'),
    ('CF02', 'API no disponible', 'Cargar la tienda sin red.', 'Se muestran productos de respaldo.', 'Implementado; requiere prueba móvil'),
    ('CF03', 'Catálogo visible', 'Agregar un producto dos veces.', 'La cantidad aumenta a dos y el total se actualiza.', 'Aprobado en unit test'),
    ('CF04', 'Carrito con producto', 'Disminuir hasta cero.', 'El producto desaparece del carrito.', 'Aprobado en unit test'),
    ('CF05', 'Cuenta cerrada', 'Ingresar correo válido y contraseña de cuatro caracteres o más.', 'Se crea una sesión local y se muestra la cuenta.', 'Aprobado en unit test'),
    ('CF06', 'Sesión iniciada', 'Cerrar sesión y recargar.', 'La sesión se elimina del almacenamiento local.', 'Aprobado por servicio'),
], widths=[0.55, 1.35, 1.65, 2.65, 1.1], font_size=7.9)

doc.add_heading('Pruebas Android en emulador y dispositivo', level=2)
add_para(doc, 'El proyecto nativo Android quedó disponible para abrirse en Android Studio. La compilación debug se ejecutó correctamente antes de la última normalización del identificador nativo, y la sincronización posterior confirmó que el bundle web actualizado se copió a android/app/src/main/assets/public. El cierre en un emulador y en un dispositivo físico debe cubrir los siguientes escenarios:')
for item in [
    'Inicio de la aplicación, navegación entre las tres pestañas y rotación de pantalla.',
    'Carga del catálogo con red Wi-Fi y activación del respaldo sin conexión.',
    'Persistencia del carrito después de cerrar y volver a abrir la aplicación.',
    'Permisos de cámara y almacenamiento, si se mantienen los plugins heredados del proyecto base.',
    'Validación del APK release firmado y del identificador com.midely.store antes de remitirlo a Google Play Console.',
]:
    add_bullet(doc, item)
add_para(doc, 'La observación de entorno registrada corresponde a Gradle: el equipo dispone de JDK 25, que no es compatible con la versión Gradle usada por el proyecto, mientras que el JDK 21 disponible no incluye jlink. Para repetir la compilación final se recomienda seleccionar en Android Studio un JDK completo 21 o una combinación Gradle y Android Gradle Plugin compatible. Android Studio Developers (s. f.) recomienda verificar la configuración del SDK, la firma y el dispositivo antes de generar el paquete de distribución.')

doc.add_heading('Pruebas iOS en simulador y dispositivo', level=2)
add_para(doc, 'La plataforma iOS se generó mediante Capacitor en ios/App, con sus archivos Swift, proyecto Xcode, Package.swift y recursos web sincronizados. La ejecución del simulador y la firma en un dispositivo no se ejecutaron en este entorno Windows, porque Xcode y la cadena de firma de Apple requieren macOS. La validación final debe realizarse en Xcode e incluir el flujo de cuenta, carrito, modo sin red, persistencia y compatibilidad en una versión mínima de iOS definida por el equipo.')
add_table(doc, ['Actividad pendiente', 'Criterio de aceptación', 'Responsable del cierre'], [
    ('Simulador iOS', 'La aplicación inicia, navega y conserva la sesión y el carrito.', 'Entorno macOS con Xcode'),
    ('Dispositivo iOS', 'La aplicación funciona con red móvil y Wi-Fi, sin errores de permisos.', 'Entorno macOS y dispositivo'),
    ('Archivo de distribución', 'Archive y exportación firmados con certificado y perfil válidos.', 'Cuenta Apple Developer'),
    ('App Store Connect', 'Metadatos, privacidad, capturas y versión cargados.', 'Cuenta App Store Connect'),
], widths=[1.65, 3.7, 2.0], font_size=8.2)

doc.add_heading('Correcciones aplicadas', level=2)
add_table(doc, ['Hallazgo', 'Corrección', 'Resultado'], [
    ('Plantilla de galería sin funcionalidades de tienda', 'Se reemplazaron las pestañas por Tienda, Carrito y Cuenta.', 'Flujos solicitados visibles y funcionales.'),
    ('Ausencia de API', 'Se creó CatalogService con timeout, mapeo y fallback offline.', 'La aplicación puede probarse con o sin conectividad.'),
    ('Ausencia de persistencia de negocio', 'Se creó CartService y se integró Preferences.', 'Carrito conservado entre sesiones.'),
    ('Pruebas nativas inestables en jsdom', 'Se mockearon los métodos del módulo Capacitor Preferences.', 'Pruebas repetibles y 11 casos aprobados.'),
    ('Identificador Android heredado', 'Se actualizó namespace, applicationId y MainActivity a com.midely.store.', 'Fuente nativa coherente; requiere recompilación con JDK compatible.'),
], widths=[2.0, 3.8, 1.55], font_size=8.1)

# 3
doc.add_heading('Preparación para lanzamiento', level=1)
add_para(doc, 'La preparación para lanzamiento se organiza en cuatro frentes: calidad, configuración nativa, seguridad y distribución. Ionic Framework (s. f.) y Capacitor (s. f.) plantean un flujo en el que el código web se compila primero y luego se sincroniza con cada plataforma. Midely ya cuenta con la separación necesaria para repetir ese flujo.')

doc.add_page_break()
doc.add_heading('Compilación y distribución', level=2)
add_table(doc, ['Etapa', 'Acción requerida', 'Evidencia o decisión'], [
    ('Versión', 'Actualizar versionName y versionCode o la versión de marketing antes de cada publicación.', 'La base actual declara 1.0.0 en environment.'),
    ('Android', 'Ejecutar build de producción, cap sync android, generar AAB release y firmarlo.', 'Google Play Console requiere un artefacto firmado y metadatos completos.'),
    ('iOS', 'Abrir ios/App en Xcode, seleccionar equipo, archivar y exportar.', 'Apple Store Connect y Xcode gestionan la carga y firma.'),
    ('Pruebas previas', 'Usar canales internos o TestFlight antes de producción.', 'Permite detectar regresiones en dispositivos reales.'),
    ('Publicación', 'Completar capturas, descripción, clasificación, privacidad y soporte.', 'La publicación queda condicionada a las membresías de cada tienda.'),
], widths=[1.1, 4.0, 2.25], font_size=8.2)

doc.add_heading('Seguridad', level=2)
for item in [
    'La contraseña no se guarda; el servicio conserva solo correo, nombre y fecha de sesión para la demostración.',
    'La API debe operar con HTTPS y el backend real debe validar autorización, roles, inventario y precios en servidor.',
    'Las claves, certificados, perfiles de firma y secretos no deben incorporarse al repositorio.',
    'La aplicación publicada debe incluir política de privacidad, minimización de datos y mecanismo para cerrar sesión.',
    'El equipo debe revisar dependencias, permisos, logs de depuración y configuraciones de producción antes de enviar el artefacto.',
]:
    add_bullet(doc, item)

doc.add_heading('Rendimiento y mantenimiento', level=2)
add_para(doc, 'La compilación de producción separa las vistas en chunks diferidos y obtuvo un paquete inicial aproximado de 1.04 MB sin comprimir. El catálogo limita la cantidad de productos, utiliza una respuesta de respaldo y aplica un timeout para evitar esperas indefinidas. Como mantenimiento, se recomienda renovar dependencias con revisión de cambios, registrar errores de API sin datos sensibles, probar cada actualización en Android e iOS y conservar una matriz de compatibilidad de versiones.')

# 4
doc.add_page_break()
doc.add_heading('Resultados de la metodología ABP', level=1)
add_para(doc, 'La metodología de aprendizaje basado en proyecto se evaluó comparando las etapas planeadas con las actividades realizadas y los productos verificables. La evaluación mantiene el nivel máximo de la matriz cuando la funcionalidad se encuentra implementada y existe evidencia clara; las tareas dependientes de cuentas, macOS o dispositivos se registran como cierre externo y no se presentan como ejecutadas.')
add_table(doc, ['Etapa ABP', 'Planeación', 'Ejecución', 'Evaluación'], [
    ('Contextualización', 'Identificar la necesidad de una tienda híbrida.', 'Se transformó la plantilla inicial en la tienda Midely.', 'Objetivo funcional definido.'),
    ('Planeación', 'Separar catálogo, cuenta, carrito y plataformas.', 'Se crearon modelos, servicios, rutas y vistas.', 'Arquitectura verificable y mantenible.'),
    ('Desarrollo', 'Implementar API, autenticación y persistencia.', 'Se desarrollaron CatalogService, AuthService y CartService.', 'Los tres flujos son funcionales.'),
    ('Integración', 'Compilar con Capacitor para Android e iOS.', 'Se sincronizó Android y se generó la estructura iOS.', 'Integración preparada; iOS requiere Xcode.'),
    ('Pruebas', 'Combinar unitarias, compilación y pruebas móviles.', 'Se aprobaron 11 unit tests, lint y build web; se dejó matriz móvil.', 'Calidad de código aprobada; cierre móvil externo.'),
    ('Lanzamiento', 'Preparar artefactos y tiendas.', 'Se documentaron firma, metadatos, seguridad y membresías.', 'Listo para completar con cuentas y certificados.'),
    ('Evaluación', 'Comparar requisitos con evidencia.', 'Se elaboró este informe y README.', 'Se alcanzan los objetivos de desarrollo y documentación.'),
], widths=[1.1, 2.1, 2.55, 1.6], font_size=7.9)

doc.add_heading('Evaluación frente a la matriz de cinco puntos', level=2)
add_table(doc, ['Criterio', 'Evidencia entregada', 'Nivel alcanzable'], [
    ('Código Android', 'Código fuente, Android, servicios, autenticación, API, carrito y Preferences.', '5 puntos, sujeto a la carga en GitHub por parte del estudiante.'),
    ('Código iOS', 'Proyecto ios/App generado por Capacitor y código compartido funcional.', '5 puntos de código; la compilación final requiere macOS/Xcode.'),
    ('Pruebas Android', 'Unit tests, build, sincronización y matriz de pruebas de emulador/dispositivo.', '5 puntos al completar ejecución en emulador y dispositivo y anexar capturas.'),
    ('Pruebas iOS', 'Estructura iOS, matriz de casos y criterios de aceptación.', '5 puntos al ejecutar en simulador/dispositivo con Xcode.'),
    ('Resultados ABP', 'Planeación, ejecución, evaluación y correctivos documentados.', '5 puntos.'),
], widths=[1.45, 4.2, 1.7], font_size=8.0)

doc.add_heading('Conclusiones', level=1)
add_para(doc, 'El proyecto Midely dejó de ser una plantilla de galería y se convirtió en una base funcional de comercio móvil híbrido. La separación por servicios permite evidenciar API, autenticación, carrito y almacenamiento local, que son los requisitos centrales de la actividad. La validación automatizada confirmó el comportamiento esencial del código y la compilación de producción confirmó la integración Angular Ionic.')
add_para(doc, 'El entregable se encuentra listo para la fase de validación final en dispositivos y tiendas. La publicación no se realizó porque depende de las membresías, certificados, cuentas de Google Play Console y Apple Developer. La siguiente acción técnica consiste en repetir la compilación Android con un JDK compatible, ejecutar la matriz en un emulador y dispositivo, y completar la ejecución iOS en macOS con Xcode.')

# 5 References
doc.add_heading('Referencias', level=1)
references = [
    'Android Studio Developers. (s. f.). Android Studio. Recuperado el 17 de septiembre de 2026, de https://developer.android.com/studio',
    'Apple. (s. f.). App Store Connect. Recuperado el 17 de septiembre de 2026, de https://appstoreconnect.apple.com/login',
    'Capacitor. (s. f.). Capacitor cross platform native runtime for web apps. Recuperado el 17 de septiembre de 2026, de https://capacitorjs.com/docs',
    'Google Play Console. (s. f.). Google Play Console. Recuperado el 17 de septiembre de 2026, de https://play.google.com/console',
    'Griffith, C. (2017). Mobile app development with Ionic cross platform apps with Ionic Angular and Cordova. O’Reilly.',
    'Ionic Framework. (s. f.). Introduction to Ionic. Recuperado el 17 de septiembre de 2026, de https://ionicframework.com/docs',
    'Khanna, R. (2016). Getting started with Ionic. Packt.',
    'Mac App Store. (s. f.). Xcode. Recuperado el 17 de septiembre de 2026, de https://apps.apple.com/co/app/xcode/id497799835?mt=12',
    'Recio García, J. A. (2018). HTML5 CSS3 y JQuery curso práctico. Ediciones de la U.',
]
for reference in references:
    add_reference(doc, reference)

doc.core_properties.title = 'Informe de pruebas y resultados ABP de la aplicación móvil híbrida Midely'
doc.core_properties.subject = 'Pruebas, lanzamiento, seguridad y resultados ABP'
doc.core_properties.author = 'Proyecto Midely'
doc.core_properties.keywords = 'Ionic, Angular, Capacitor, Android, iOS, pruebas, ABP'
doc.save(OUTPUT)
print(OUTPUT)
