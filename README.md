**Regresión Lineal — Predicciones de Eficiencia Terminal (INEGI)**

- **Descripción:**: Script que entrena modelos de regresión lineal sobre datos históricos del INEGI y genera predicciones (2026–2030) junto con un reporte en PDF que incluye la gráfica y una tabla de resultados.

**Requisitos**
- **Python:** 3.8+
- **Librerías:** pandas, matplotlib, scikit-learn, fpdf

Instala las dependencias con:

```bash
pip install pandas matplotlib scikit-learn fpdf
```

**Archivos importantes**
- **Script principal:** [Regresion_INEGI.py](Regresion_INEGI.py)
- **Datos (entrada):** [Inegi.csv](Inegi.csv)
- **Salida (PDF):** Reporte generado en `Reporte_INEGI.pdf` en la misma carpeta del proyecto.

**Uso**
1. Asegúrate de que `Inegi.csv` esté en la ruta indicada dentro del script o ajusta la variable `archivo_csv` en [Regresion_INEGI.py](Regresion_INEGI.py).
2. Ejecuta el script:

```bash
python Regresion_INEGI.py
```

3. Al finalizar, el script guarda `Reporte_INEGI.pdf` en la carpeta del proyecto y muestra en consola la ruta del archivo.

**Qué hace el script (resumen por secciones)**
- **Carga de datos:** lee `Inegi.csv` usando `encoding='latin1'` (importante para acentos y caracteres especiales).
- **Limpieza y selección:** elimina filas sin `Área geográfica`, convierte `Periodos` a enteros y extrae las columnas de Secundaria y Media Superior.
- **Entrenamiento:** ajusta un `LinearRegression` por cada nivel educativo y extrae `m` (pendiente) y `b` (intercepto).
- **Predicción:** genera predicciones para los años 2026–2030 y crea un DataFrame con los resultados.
- **Visualización:** traza puntos históricos, líneas de tendencia y cruces para las predicciones; guarda la gráfica temporal `grafica_temp.png`.
- **Reporte PDF:** arma un PDF con explicación, fórmulas (m, b), tabla de predicciones e incrusta la gráfica.
- **Limpieza final:** elimina la imagen temporal y guarda `Reporte_INEGI.pdf`.

**Salida esperada**
- `Reporte_INEGI.pdf` — reporte listo para imprimir/compartir.
- La imagen temporal `grafica_temp.png` se borra automáticamente al final.

**Notas**
- Si el script falla por codificación, confirma que `encoding='latin1'` y que el CSV contiene las columnas esperadas.
- Las rutas en el script son absolutas (ej. `C:/Users/.../Inegi.csv`). Modifica `archivo_csv` si prefieres rutas relativas.

Si quieres, puedo:
- Ejecutar el script aquí y generar el PDF (requiere tener Python y librerías instaladas).
- Hacer un commit con este `README.md`.

