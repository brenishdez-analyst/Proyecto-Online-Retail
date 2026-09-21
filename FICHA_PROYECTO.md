# Ficha del proyecto

## 1. Información general

- **Nombre:** Proyecto Online Retail: análisis de ventas, clientes y retención en e-commerce
- **Especialidad:** Data Analytics
- **Fuente:** Online Retail II — UCI Machine Learning Repository
- **Fuente original:** https://archive.ics.uci.edu/dataset/502/online+retail+ii
- **Proyecto publicado:** https://github.com/brenishdez-analyst/Proyecto-Online-Retail

## 2. Objetivo

Analizar las transacciones de una tienda online para identificar los factores que explican ventas, cancelaciones, recurrencia y concentración de ingresos. El análisis apoya decisiones de retención, surtido, mercados prioritarios y planeación comercial.

## 3. Plan de trabajo

1. Explorar estructura y calidad de los datos.
2. Limpiar los registros y documentar reglas de negocio.
3. Analizar KPIs, productos, mercados, RFM y cohortes con Python y SQL.
4. Construir y validar un dashboard ejecutivo en Power BI.
5. Documentar conclusiones y proximos pasos.

## 4. Preguntas clave

1. ¿Las cancelaciones y registros sin cliente deben incluirse en cada KPI?
2. ¿Qué parte del valor proviene de clientes recurrentes y segmentos de alto valor?
3. ¿Qué conclusiones están limitadas por la antigüedad y las variables disponibles?

## 5. Qué se hizo y cómo

Se combinaron dos hojas anuales y se normalizaron nombres y tipos. Se eliminaron duplicados exactos, se separaron cancelaciones, devoluciones y ventas válidas, y se conservaron ventas sin cliente únicamente para KPIs generales. Se crearon tablas de pedidos, desempeño mensual, países, productos, cohortes y RFM. Los datos limpios se exportaron a CSV y SQLite para validar resultados con SQL y alimentar Power BI.

## 6. Resultados

El análisis obtuvo £20.91 millones en ingresos válidos, 40,077 pedidos, 5,878 clientes identificados y un ticket promedio de £521.84. La tasa de cancelación por factura fue de 15.46%.

El Reino Unido concentró 85.18% de los ingresos y el 72.39% de los clientes identificados realizó más de una compra. Mediante la segmentación RFM se identificó al grupo Champions como el segmento de mayor valor: reunió 1,175 clientes y generó aproximadamente £12.23 millones.

Este proyecto no incluyó un modelo predictivo, ya que su objetivo fue descriptivo y de diagnóstico. Entre los métodos utilizados, la segmentación RFM fue la más útil para la toma de decisiones, porque permitió clasificar a los clientes según recencia, frecuencia y valor monetario, e identificar grupos prioritarios para retención y campañas comerciales. El análisis de cohortes complementó este resultado al mostrar la evolución de la recompra a lo largo del tiempo.

## 7. Conclusiones

El proyecto muestra que la calidad de las reglas de negocio cambia directamente los KPIs. Con más tiempo, se investigarían motivos de cancelación, margen y adquisición. En una entrevista destacaría la validación cruzada entre Python, SQL y Power BI, el tratamiento diferenciado de clientes no identificados y la conversión de resultados en acciones comerciales.

## 8. Checklist

- [x] README comprensible
- [x] Archivos organizados
- [x] Sin credenciales o datos sensibles
- [x] Fuente original incluida
- [x] Notebook y consultas SQL preparados
- [x] Dashboard terminado y validado
- [x] Repositorio publicado
- [x] Enlace compartido con el coach

