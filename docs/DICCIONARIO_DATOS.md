# Diccionario de datos

## Tabla `sales`

| Campo | Descripción |
|---|---|
| `invoice_no` | Identificador de factura. Las facturas que comienzan con C son cancelaciones. |
| `stock_code` | Código del producto. |
| `description` | Nombre o descripción del producto. |
| `quantity` | Unidades registradas en la línea. |
| `invoice_date` | Fecha y hora de la transacción. |
| `unit_price` | Precio unitario en libras esterlinas. |
| `customer_id` | Identificador del cliente; puede faltar. |
| `country` | País del cliente. |
| `is_cancelled` | Indica si la factura comienza con C. |
| `is_return` | Indica si la cantidad es negativa. |
| `is_valid_sale` | Compra no cancelada, con cantidad y precio positivos. |
| `line_revenue` | `quantity × unit_price` para ventas válidas. |
| `is_non_merchandise` | Identifica postage, cargos manuales y otros códigos administrativos que se excluyen del ranking de productos. |

## Tabla `orders`

Una fila por factura válida. Contiene ingresos, unidades y productos distintos por pedido. `is_high_value_outlier` marca pedidos por encima del percentil 99 para análisis de sensibilidad, sin borrarlos automáticamente.

## Tabla `customer_rfm`

Una fila por cliente identificado. Incluye recencia, frecuencia, valor monetario y segmento RFM.
