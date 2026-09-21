# RetailPulse

Análisis end-to-end de ventas, clientes y retención para un e-commerce del Reino Unido.

## Objetivo

Identificar qué clientes, productos, mercados y periodos generan mayor valor, así como oportunidades para mejorar la retención y vigilar cancelaciones.

## Fuente

[Online Retail II — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii). El dataset contiene 1,067,371 líneas transaccionales registradas entre diciembre de 2009 y diciembre de 2011.

## Herramientas

- Python: pandas, matplotlib y seaborn.
- SQL: SQLite y consultas de negocio.
- Power BI: dashboard ejecutivo y análisis de clientes.

## Resultados principales

| KPI | Resultado |
|---|---:|
| Ingresos válidos | £20,913,891.47 |
| Pedidos válidos | 40,077 |
| Clientes identificados | 5,878 |
| Ticket promedio | £521.84 |
| Facturas canceladas | 8,292 |
| Tasa de cancelación por factura | 15.46% |

Hallazgos:

- El Reino Unido concentró 85.18% de los ingresos válidos.
- Noviembre fue el mes de mayor ingreso tanto en 2010 como en 2011, lo que muestra una estacionalidad previa a las fiestas.
- El 72.39% de los clientes identificados realizó más de un pedido.
- Los clientes `Champions` representaron 1,175 de 5,878 clientes y generaron aproximadamente £12.23 millones.
- Se detectaron 12,133 filas duplicadas y 243,007 registros sin identificador de cliente.
- Un total de 401 pedidos quedó por encima del percentil 99 de ingresos por pedido (£4,542.06), por lo que deben revisarse en un análisis de sensibilidad.

## Recomendaciones

1. Diseñar campañas de recompra para los segmentos `Needs attention` y `At risk`.
2. Preparar inventario y campañas antes de octubre y noviembre, los meses de mayor demanda.
3. Proteger la relación con clientes mayoristas de alto valor y evitar depender de pocos compradores.
4. Separar mercancía, postage y ajustes administrativos en los reportes comerciales.
5. Investigar las causas de cancelación antes de fijar una meta de reducción.

## Decisiones de limpieza

- Se eliminaron duplicados exactos.
- Se consideró venta válida una factura no cancelada, con cantidad y precio positivos y fecha válida.
- Los registros sin `Customer ID` se conservaron para ventas generales, pero se excluyeron de cohortes y RFM.
- Los códigos administrativos se separaron del ranking de productos.
- Los pedidos extremos se marcaron, pero no se borraron sin evidencia de error.

## Estructura

```text
retailpulse/
├── data/
│   ├── raw/                 # dataset
│   └── processed/           # Resultados generados
├── docs/                    # Guía y diccionario
├── images/                  # Gráficas exportadas
├── notebooks/               # Análisis reproducible
├── powerbi/                 # Diseño y medidas del dashboard
├── sql/                     # Consultas de negocio
├── README.md
└── requirements.txt
```

## Cómo reproducir el proyecto

1. Instala dependencias con `pip install -r requirements.txt`.
2. Ejecuta `python notebooks/01_exploracion_limpieza.py`.
3. Revisa los archivos creados en `data/processed/` e `images/`.
4. Abre Power BI y sigue `powerbi/GUIA_DASHBOARD.md`.

## Limitaciones

- Los datos corresponden a 2009–2011 y no representan necesariamente el comportamiento actual del e-commerce.
- Diciembre de 2011 solo contiene datos hasta el día 9; no debe compararse como un mes completo.
- No existe información de costos, margen, canal de adquisición ni motivo de cancelación.
- Los registros sin cliente no pueden utilizarse para retención o segmentación.
- La segmentación RFM es descriptiva y depende del periodo observado.
