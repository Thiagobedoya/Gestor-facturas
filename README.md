# Gestor de Facturas

Aplicación web para que un freelancer o un negocio pequeño lleve el registro de sus clientes y les emita facturas, con total calculado automáticamente, control de pagos y descarga en PDF. Reemplaza el trabajo manual en Word o Excel.

> **Estado del proyecto:** en desarrollo. Ya cubre el flujo central de facturación, pero todavía no está listo para producción (ver [Próximos pasos](#próximos-pasos)).

## Funcionalidades

**Clientes**

- Crear, ver, editar y eliminar clientes.
- No permite eliminar un cliente que ya tiene facturas, para no dejar facturas huérfanas.

**Facturas**

- Creación de facturas con varios ítems (producto, cantidad y valor unitario).
- Número de factura consecutivo y fecha asignados automáticamente.
- Total y subtotales calculados al momento, nunca guardados, para que no se desactualicen.
- Validaciones: avisa si una fila del formulario quedó incompleta y no deja guardar una factura sin ítems.
- Lista de facturas con estado (Pendiente o Pagada) y detalle de cada una.
- Descarga de la factura en PDF.
- Registro de pago con pantalla de confirmación que muestra el resumen de la factura.
- Reversa de un pago a estado Pendiente, con confirmación.
- Protección contra acciones sin sentido, como pagar una factura que ya está pagada.

**Interfaz**

- Mensajes de aviso de éxito y de error.
- Diseño propio con CSS: menú de navegación, tablas, botones y formularios.

## Tecnologías

- **Python 3** (desarrollado con Python 3.14)
- **Flask**: framework web
- **Flask-SQLAlchemy / SQLAlchemy**: acceso a la base de datos mediante un ORM
- **SQLite**: base de datos local
- **Jinja2**: plantillas HTML con herencia
- **xhtml2pdf**: generación de facturas en PDF
- **HTML y CSS**

## Cómo ejecutarlo

Estos pasos son para Windows con PowerShell.

1. Descargue o clone el proyecto y abra una terminal dentro de su carpeta.
2. Cree y active el entorno virtual:

```
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Instale las dependencias:

```
pip install -r requirements.txt
```

4. Inicie la aplicación:

```
python app.py
```

5. Abra en el navegador: <http://127.0.0.1:5000/clientes>

La base de datos se crea sola la primera vez que se ejecuta la aplicación, en la carpeta `instance/`.

## Configuración

La clave secreta de Flask está escrita directamente en `app.py` con un valor de ejemplo. **Antes de publicar la aplicación en un servidor real hay que reemplazarla** por una clave larga y aleatoria, guardada fuera del código (por ejemplo, en una variable de entorno).

## Estructura del proyecto

```
Gestor-facturas/
├── app.py                 Rutas y configuración de la aplicación
├── models.py              Modelos de la base de datos: Cliente, Factura, ItemFactura
├── requirements.txt       Dependencias del proyecto
├── static/
│   └── estilos.css        Estilos de toda la aplicación
├── templates/
│   ├── base.html          Plantilla base: menú y mensajes de aviso
│   ├── clientes.html
│   ├── nuevo_cliente.html
│   ├── editar_cliente.html
│   ├── facturas.html
│   ├── nueva_factura.html
│   ├── detalle_factura.html
│   ├── confirmar_pago.html
│   └── pdf_factura.html   Plantilla del PDF (no hereda de base.html)
└── instance/              Base de datos SQLite (se genera sola, no se versiona)
```

## Rutas principales

| Ruta | Métodos | Descripción |
|---|---|---|
| `/clientes` | GET | Lista de clientes |
| `/clientes/nuevo` | GET, POST | Crear cliente |
| `/clientes/<id>/editar` | GET, POST | Editar cliente |
| `/clientes/<id>/eliminar` | POST | Eliminar cliente |
| `/facturas` | GET | Lista de facturas |
| `/facturas/nueva` | GET, POST | Crear factura |
| `/facturas/<id>` | GET | Detalle de la factura |
| `/facturas/<id>/pdf` | GET | Descargar la factura en PDF |
| `/facturas/<id>/pagar` | GET, POST | Resumen y confirmación del pago |
| `/facturas/<id>/revertir` | POST | Devolver una factura pagada a pendiente |

## Próximos pasos

- Editar y eliminar facturas.
- Permitir agregar más de tres ítems por factura con un botón que añada filas.
- Enviar la factura por correo al cliente.
- Autenticación de usuarios, con los datos separados por empresa.
- Migrar de SQLite a PostgreSQL y desplegar en un servidor.
- Mover la clave secreta fuera del código y reforzar la seguridad.
- Resolver la numeración cuando dos personas crean una factura al mismo tiempo.
- Agregar pruebas automáticas.

## Autor

Santiago Bedoya Arango