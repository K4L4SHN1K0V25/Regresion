# Importamos las herramientas necesarias para nuestro proyecto:
# pandas: Es la librería para manipular datos en tablas.
import pandas as pd 
# matplotlib.pyplot: Nos permite crear gráficas, dibujar líneas, puntos y personalizar ejes.
import matplotlib.pyplot as plt 
# LinearRegression de sklearn: Es el cerebro matemático que calculará la línea de tendencia.
from sklearn.linear_model import LinearRegression 
# FPDF: Librería para crear documentos PDF.
from fpdf import FPDF 
# os: Nos permite interactuar con el sistema operativo de tu computadora.
import os 

# =====================================================================
# 1. CARGA DE DATOS
# =====================================================================
# Definimos la ruta exacta donde vive nuestro archivo con los datos históricos.
archivo_csv = 'C:/Users/Ezio0/OneDrive/Escritorio/Regresion/Inegi.csv'

# Usamos pandas para leer el archivo. 
# NOTA CLAVE: 'encoding=latin1' es vital aquí porque hay caracteres especiales del español (como acentos o la 'ñ').
df = pd.read_csv(archivo_csv, encoding='latin1')


# =====================================================================
# 2. LIMPIEZA Y PREPARACIÓN DE DATOS
# =====================================================================
# El INEGI a menudo pone texto basura al final ("Fuente: SEP...", "Notas...").
# Esas filas no tienen un "Área geográfica" válida. Usamos dropna() para eliminar 
# cualquier fila donde la columna 'Área geográfica' esté vacía (NaN) y creamos una copia limpia.
df_clean = df.dropna(subset=['Área geográfica']).copy()

# Convertimos la columna 'Periodos' (que trae los años) explícitamente a números enteros (int).
# Esto evita que Python piense que el año "2015" es un texto o un decimal "2015.0".
df_clean['Periodos'] = df_clean['Periodos'].astype(int)

# En lugar de escribir el nombre kilométrico de las columnas a mano, le decimos a pandas
# que tome el nombre exacto de la columna en la posición 2 (Media Superior) y 3 (Secundaria).
# En programación empezamos a contar desde 0.
col_media_sup = df_clean.columns[2]
col_secundaria = df_clean.columns[3]

# Filtramos la tabla general para crear dos "mini tablas" exclusivas para cada nivel educativo.
# Si en algún año falta el dato (NaN) de Secundaria o Media Superior, se elimina esa fila específica.
df_ms = df_clean[['Periodos', col_media_sup]].dropna()
df_sec = df_clean[['Periodos', col_secundaria]].dropna()


# =====================================================================
# 3. ENTRENAMIENTO DEL MODELO DE REGRESIÓN LINEAL
# =====================================================================
# La "X" mayúscula siempre es la variable independiente (el Tiempo/Años).
# Va en corchetes dobles [['Periodos']] porque sklearn espera una matriz de datos (2D).
X_ms = df_ms[['Periodos']]
X_sec = df_sec[['Periodos']]

# La "y" minúscula es la variable dependiente (lo que queremos predecir: la Eficiencia Terminal).
y_ms = df_ms[col_media_sup]
y_sec = df_sec[col_secundaria]

# Aquí ocurre la magia matemática. LinearRegression() inicializa el algoritmo.
# .fit(X, y) "entrena" al algoritmo, obligándolo a encontrar la línea recta que mejor 
# pase por el medio de todos nuestros puntos históricos.
modelo_ms = LinearRegression().fit(X_ms, y_ms)
modelo_sec = LinearRegression().fit(X_sec, y_sec)

# EXTRAER PARÁMETROS MATEMÁTICOS PARA EL PDF (y = mx + b)
# .coef_[0] nos da la pendiente 'm' (cuánto sube o baja el porcentaje cada año).
m_ms = modelo_ms.coef_[0]
m_sec = modelo_sec.coef_[0]

# .intercept_ nos da la 'b' (el punto donde la línea cruzaría si el año fuera el 0).
b_ms = modelo_ms.intercept_
b_sec = modelo_sec.intercept_


# =====================================================================
# 4. PREDICCIONES HACIA EL FUTURO (2026 - 2030)
# =====================================================================
# Creamos un nuevo DataFrame solo con los años de los que NO tenemos datos reales.
anios_futuros = pd.DataFrame({'Periodos': [2026, 2027, 2028, 2029, 2030]})

# Le pasamos estos años futuros a los modelos que ya entrenamos usando el método .predict()
# Nos devolverá listas con los porcentajes teóricos esperados para esos años.
pred_ms_futuro = modelo_ms.predict(anios_futuros)
pred_sec_futuro = modelo_sec.predict(anios_futuros)

# Empaquetamos nuestras predicciones en una tabla limpia (DataFrame) para 
# poder imprimirla fácilmente más adelante en el PDF.
df_pred = pd.DataFrame({
    'Anio': [2026, 2027, 2028, 2029, 2030],
    'Secundaria (%)': pred_sec_futuro,
    'Media Superior (%)': pred_ms_futuro
})


# =====================================================================
# 5. CREACIÓN DE LA GRÁFICA Y GUARDADO TEMPORAL
# =====================================================================
# Preparamos un "lienzo" en blanco de 10x6 pulgadas para dibujar.
plt.figure(figsize=(10, 6))

# Trazos para MEDIA SUPERIOR (Color Azul)
# 1. Puntos reales históricos (scatter)
plt.scatter(df_ms['Periodos'], y_ms, color='blue', label='Media Sup. (Datos Reales)')
# 2. Línea de tendencia histórica calculada por el modelo (plot con línea punteada '--')
plt.plot(df_ms['Periodos'], modelo_ms.predict(X_ms), color='blue', linestyle='--')

# Trazos para SECUNDARIA (Color Naranja)
# 1. Puntos reales históricos (scatter)
plt.scatter(df_sec['Periodos'], y_sec, color='orange', label='Secundaria (Datos Reales)')
# 2. Línea de tendencia (plot)
plt.plot(df_sec['Periodos'], modelo_sec.predict(X_sec), color='orange', linestyle='--')

# Trazos para el FUTURO (Cruces rojas y azul marino)
# Usamos marker='X' y s=100 (size) para que resalten visualmente respecto al pasado.
plt.scatter(anios_futuros['Periodos'], pred_ms_futuro, color='navy', marker='X', s=100, label='Predicciones Media Sup.')
plt.scatter(anios_futuros['Periodos'], pred_sec_futuro, color='red', marker='X', s=100, label='Predicciones Secundaria')

# Maquillaje de la gráfica: Títulos, etiquetas de los ejes X y Y, y cuadricula de fondo.
plt.title('Regresión Lineal: Eficiencia Terminal en México (INEGI)')
plt.xlabel('Año')
plt.ylabel('Porcentaje de Eficiencia Terminal (%)')
plt.legend() # Muestra el cuadrito que explica qué significa cada color
plt.grid(True, linestyle=':', alpha=0.7) # Malla punteada semitransparente (alpha)
plt.tight_layout() # Auto-ajusta los márgenes para que nada quede cortado

# Guardado temporal: En vez de mostrar la imagen en pantalla, la guardamos como un PNG
# en tu disco duro temporalmente para poder incrustarla en el PDF.
ruta_imagen = 'C:/Users/Ezio0/OneDrive/Escritorio/Regresion/grafica_temp.png'
plt.savefig(ruta_imagen)
plt.close() # MUY IMPORTANTE: Cierra la gráfica en la memoria para que el programa siga corriendo.


# =====================================================================
# 6. ENSAMBLAJE DEL REPORTE EN PDF
# =====================================================================
# Creamos una "clase" hija de FPDF para poder personalizar el encabezado del documento.
# Todo PDF que generemos con esta clase, llevará automáticamente este título en la parte superior.
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15) # Arial, Bold (Negrita), Tamaño 15
        # cell: Imprime una "celda" de texto. (ancho 0 = toda la hoja, alto 10, texto, bordes 0, salto línea 1, Centrado 'C')
        self.cell(0, 10, 'Reporte de Eficiencia Terminal - Predicciones', 0, 1, 'C')
        self.ln(5) # ln = Line Break (Salto de línea de 5 unidades)

# Instanciamos el objeto PDF y creamos la primera página en blanco.
pdf = PDF()
pdf.add_page()

# --- SECCIÓN 1: TEXTO EXPLICATIVO ---
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, '1. Explicacion de las Previsiones', 0, 1) # Título de sección

pdf.set_font('Arial', '', 11) # Quitamos negritas para el cuerpo del texto
explicacion_general = (
    "El presente modelo utiliza Regresion Lineal simple sobre los datos historicos del INEGI. "
    "Esto significa que identifica la tendencia de crecimiento o decrecimiento de los ultimos "
    "años y asume que este ritmo se mantendra constante en el futuro."
)
# multi_cell es especial para párrafos largos, ya que hace el salto de línea automático si el texto topa con el borde derecho.
pdf.multi_cell(0, 6, explicacion_general)
pdf.ln(5)

# --- SECCIÓN 2: MATEMÁTICAS ---
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, '2. Operaciones y Explicacion Matematica', 0, 1)

pdf.set_font('Arial', '', 11)
explicacion_mate = (
    "Para calcular el futuro, la Inteligencia Artificial de la libreria scikit-learn "
    "utiliza la ecuacion universal de la linea recta:  y = mx + b \n\n"
    "¿Que significa cada letra en nuestro estudio de estudiantes?\n"
    "- 'y' (El Resultado): Es el Porcentaje de Eficiencia Terminal que queremos descubrir.\n"
    "- 'x' (El Tiempo): Es el año exacto que queremos predecir (ejemplo: 2028).\n"
    "- 'm' (La Tendencia): Es el ritmo de crecimiento. Si 'm' es 0.5, significa que cada "
    "año que pasa, un 0.5% mas de alumnos logran graduarse. Si es negativo, indica "
    "que la educacion esta empeorando año con año.\n"
    "- 'b' (El Anclaje): Es el punto de partida matematico. Literalmente significa 'cual "
    "seria el porcentaje en el año cero (año 0)'. Aunque historicamente no evaluamos el año 0, "
    "la formula necesita este ancla para trazar la recta perfecta a lo largo de los siglos."
)
pdf.multi_cell(0, 6, explicacion_mate)
pdf.ln(5)

pdf.set_font('Arial', 'I', 11) # 'I' de Italic (Cursiva)
pdf.cell(0, 6, 'A continuacion, las formulas exactas calculadas con los datos del INEGI:', 0, 1)
pdf.ln(3)

# Imprimimos la fórmula de Secundaria concatenando las variables que extrajimos en el Paso 3.
# El formato :.4f indica que solo queremos imprimir 4 decimales para no saturar el texto.
pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 6, 'Formula detectada para Secundaria:', 0, 1)
pdf.set_font('Courier', '', 10) # Cambiamos a fuente estilo máquina de escribir para que parezca código
pdf.cell(0, 6, f"Porcentaje (y) = ({m_sec:.4f} * año) + ({b_sec:.4f})", 0, 1)
pdf.ln(2)

# Imprimimos la fórmula de Media Superior
pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 6, 'Formula detectada para Media Superior:', 0, 1)
pdf.set_font('Courier', '', 10)
pdf.cell(0, 6, f"Porcentaje (y) = ({m_ms:.4f} * año) + ({b_ms:.4f})", 0, 1)
pdf.ln(8)

# --- SECCIÓN 3: DIBUJAR LA TABLA ---
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, '3. Tabla de Predicciones (%)', 0, 1)

# Primero dibujamos los "encabezados" de la tabla. El '1' como cuarto parámetro significa "Dibujar borde".
pdf.set_font('Arial', 'B', 11)
pdf.cell(40, 10, 'año', 1, 0, 'C') # 0 al final = no des salto de línea, quédate en la misma fila
pdf.cell(60, 10, 'Secundaria', 1, 0, 'C')
pdf.cell(60, 10, 'Media Superior', 1, 1, 'C') # 1 al final = ahora sí baja de renglón

# Llenamos la tabla fila por fila usando un ciclo FOR.
pdf.set_font('Arial', '', 11)
for i in range(len(df_pred)):
    # Extraemos el valor fila por fila (iloc) de nuestro dataframe df_pred
    anio = str(df_pred['Anio'].iloc[i])
    sec = f"{df_pred['Secundaria (%)'].iloc[i]:.2f}%" # :.2f% lo formatea a 2 decimales y le añade el símbolo %
    ms = f"{df_pred['Media Superior (%)'].iloc[i]:.2f}%"
    
    # Dibujamos las tres celdas de la fila actual
    pdf.cell(40, 10, anio, 1, 0, 'C')
    pdf.cell(60, 10, sec, 1, 0, 'C')
    pdf.cell(60, 10, ms, 1, 1, 'C')
pdf.ln(10)

# --- SECCIÓN 4: INCRUSTAR LA IMAGEN ---
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, '4. Visualizacion del Modelo', 0, 1)

# Tomamos el archivo PNG que guardamos en el Paso 5 y lo pegamos en el PDF.
# x=10 es el margen izquierdo, w=180 es el ancho de la imagen para que encaje bien en la hoja A4.
pdf.image(ruta_imagen, x=10, y=None, w=180)

# =====================================================================
# 7. EXPORTACIÓN FINAL Y LIMPIEZA
# =====================================================================
ruta_pdf = 'C:/Users/Ezio0/OneDrive/Escritorio/Regresion/Reporte_INEGI.pdf'
pdf.output(ruta_pdf) # Aquí se guarda el archivo PDF.

# Finalmente, borramos la imagen temporal.
if os.path.exists(ruta_imagen):
    os.remove(ruta_imagen)

# Confirmación en consola para saber que todo salió perfecto.
print(f"¡Éxito! Reporte super detallado generado en: {ruta_pdf}")