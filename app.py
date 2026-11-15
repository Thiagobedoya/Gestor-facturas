from models import db, Cliente, Factura, ItemFactura
from flask import Flask, render_template, request, redirect
from datetime import date
from flask import make_response
from xhtml2pdf import pisa
from io import BytesIO
from flask import flash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///facturas.db"
app.config["SECRET_KEY"] = "cambia-esto-por-algo-largo-y-aleatorio"

db.init_app(app)

@app.route("/") #Esta es la ruta de inicio de la aplicación
def inicio():
    return "¡Hola! Mi gestor de facturas está funcionando."

@app.route("/clientes/nuevo", methods=["GET", "POST"]) #Esta ruta permite crear un nuevo cliente
def nuevo_cliente():
    if request.method == "POST":
        cliente = Cliente(
            nombre = request.form["nombre"],
            email = request.form["email"],
            telefono = request.form["telefono"],
            direccion = request.form["direccion"],
            ciudad = request.form["ciudad"],
            pais = request.form["pais"],
        )
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente creado exitosamente", "exito") #Esta linea muestra un mensaje rápido indicando que se creo el cliente
        return redirect("/clientes") #Esto redirige al usuario a la página de inicio después de crear un nuevo cliente

    return render_template("nuevo_cliente.html") #Esta línea renderiza la plantilla HTML para crear un nuevo cliente cuando se accede a la ruta "/clientes/nuevo" con el método GET.

@app.route("/clientes") #Esta ruta permite ver todos los clientes
def ver_clientes():
    clientes = Cliente.query.all()
    return render_template("clientes.html", clientes=clientes) #Esta línea renderiza la plantilla HTML para mostrar todos los clientes cuando se accede a la ruta "/clientes".

@app.route("/clientes/<int:id>/eliminar", methods=["POST"]) #Esta ruta permite eliminar un cliente existente
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id) #Esta línea obtiene el cliente con el ID proporcionado de la base de datos. Si no se encuentra, devuelve un error 404.
    
    if cliente.facturas: #Esta línea verifica si el cliente tiene facturas asociadas. Si es así, no se permite eliminar al cliente y se muestra un mensaje de error.
        flash("No se puede eliminar el cliente porque tiene facturas asociadas", "error")
        return redirect("/clientes")
    
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente eliminado exitosamente", "exito") #Esta linea muestra un mensaje rápido indicando que se elimino el cliente
    return redirect("/clientes") #Esta línea redirige al usuario a la página de clientes después de eliminar un cliente.

@app.route("/clientes/<int:id>/editar", methods=["GET", "POST"]) #Esta ruta permite editar un cliente existente
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id) #Esta línea obtiene el cliente con el ID proporcionado de la base de datos. Si no se encuentra, devuelve un error 404.
    
    if request.method == "POST": 
        cliente.nombre = request.form["nombre"]
        cliente.email = request.form["email"]
        cliente.telefono = request.form["telefono"]
        cliente.direccion = request.form["direccion"]
        cliente.ciudad = request.form["ciudad"]
        cliente.pais = request.form["pais"]
        
        db.session.commit()
        flash("Cliente editado exitosamente", "exito") #Esta linea muestra un mensaje rápido indicando que se edito el cliente
        return redirect("/clientes") #Esta línea redirige al usuario a la página de clientes después de editar un cliente.
    
    return render_template("editar_cliente.html", cliente=cliente) 

@app.route("/facturas/nueva", methods=["GET", "POST"]) #Esta ruta permite crear una nueva factura
def nueva_factura():
    if request.method == "POST": 
        
        productos = request.form.getlist("producto") 
        cantidades = request.form.getlist("cantidad")
        valores = request.form.getlist("valor_unitario")
        
        filas_validas = []

        for producto, cantidad, valor in zip(productos, cantidades, valores): #Esta línea itera sobre las listas de productos, cantidades y valores unitarios obtenidas del formulario, utilizando la función zip para agrupar los elementos correspondientes de cada lista en tuplas. Esto permite procesar cada producto junto con su cantidad y valor unitario en un solo bucle.
            if producto and cantidad and valor:
                filas_validas.append((producto,cantidad, valor)) 
            elif producto or cantidad or valor:
                if not producto:
                    flash("No ha agregado producto", "error")
                elif not cantidad:
                    flash("No ha ingresado la cantidad", "error")
                else:
                    flash("No ha ingresado valor", "error")
                return redirect("/facturas/nueva")
        
        if not filas_validas:
            flash("La factura está vacía", "error")
            return redirect("/facturas/nueva")
        
        ultima_factura = Factura.query.order_by(Factura.id.desc()).first() #Esta línea obtiene la última factura creada en la base de datos, ordenando por el ID en orden descendente y tomando el primer resultado. Esto se hace para determinar el número de la nueva factura.
        if ultima_factura:
            numero = str(int(ultima_factura.numero) + 1)
        else:
            numero="1"
        cliente_id = request.form["cliente_id"] #Esta línea obtiene el ID del cliente seleccionado en el formulario de creación de factura.
                
        factura = Factura( #Esta línea crea una nueva instancia de la clase Factura con los datos proporcionados en el formulario.
            numero=numero,
            fecha=date.today(),
            cliente_id=cliente_id
        )
        db.session.add(factura) #Esta línea agrega la nueva factura a la sesión de la base de datos, preparándola para ser guardada en la base de datos.
        db.session.commit()
                
        for producto, cantidad, valor in filas_validas:        
            item = ItemFactura(
                producto=producto,
                cantidad=int(cantidad),
                valor_unitario=float(valor),
                factura_id=factura.id
            )
            db.session.add(item)
        db.session.commit()
        flash("Factura creada exitosamente", "exito") #Esta linea muestra un mensaje rápido indicando que se creo la factura
        return redirect("/facturas")
    
    clientes = Cliente.query.all()
    return render_template("nueva_factura.html", clientes=clientes)

@app.route("/facturas") #Esta ruta permite ver todas las facturas
def ver_facturas():
    facturas = Factura.query.all()
    return render_template("facturas.html", facturas=facturas)

@app.route("/facturas/<int:id>") #Esta ruta permite ver el detalle de una factura específica
def ver_factura(id):
    factura = Factura.query.get_or_404(id) #Esta línea obtiene la factura con el ID proporcionado de la base de datos. Si no se encuentra, devuelve un error 404.
    return render_template("detalle_factura.html", factura=factura)

@app.route("/facturas/<int:id>/pdf") #Esta ruta permite generar un PDF de una factura específica
def generar_pdf(id):
    factura = Factura.query.get_or_404(id)
    html = render_template("pdf_factura.html", factura=factura) #Esta línea renderiza la plantilla HTML para generar el PDF de la factura, pasando la factura específica como contexto para que los datos de la factura se muestren correctamente en el PDF.
    
    pdf_buffer = BytesIO() #Esta línea crea un objeto BytesIO que actúa como un buffer en memoria para almacenar el contenido del PDF generado. Esto permite que el PDF se genere y se mantenga en memoria sin necesidad de guardarlo en un archivo temporal en el disco.
    pisa.CreatePDF(html, dest=pdf_buffer) #Utiliza la función CreatePDF de la bilioteca xhtml2pdf para convertir el contenido HTML a pdf
    
    response = make_response(pdf_buffer.getvalue()) 
    response.headers["Content-Type"] = "application/pdf" 
    response.headers["Content-Disposition"] = f"inline; filename=factura_{factura.numero}.pdf"
    return response

@app.route("/facturas/<int:id>/pagar", methods=["GET", "POST"]) #Esta ruta permite marcar una factura como pagada
def pagar_factura(id):
    factura = Factura.query.get_or_404(id)
    
    if factura.estado == "Pagada":
        flash("La factura ya está pagada", "error")
        return redirect("/facturas")
    
    if request.method == "POST":
        factura.estado = "Pagada"
        db.session.commit()
        flash("Factura marcada como pagada exitosamente", "exito") #Esta linea muestra un mensaje rápido indicando que se marco la factura como pagada
        return redirect("/facturas")
    
    return render_template("confirmar_pago.html", factura=factura)

@app.route("/facturas/<int:id>/revertir", methods=["POST"])
def revertir_factura(id):
    factura=Factura.query.get_or_404(id)
    
    if factura.estado == "Pendiente":
        flash("La factura está pendiente, no se puede revertir", "error")
        return redirect("/facturas")
    
    factura.estado = "Pendiente"
    db.session.commit()
    flash("Factura paga revertida", "exito")
    return redirect("/facturas")

@app.route("/facturas/<int:id>/eliminar", methods=["POST"]) #Esta ruta permite eliminar una factura existente
def eliminar_factura(id):
    factura = Factura.query.get_or_404(id) #Esta línea obtiene la factura con el ID proporcionado de la base de datos. Si no se encuentra, devuelve un error 404.
    
    if factura.estado == "Pagada": #Esta línea verifica si la factura está marcada como pagada. Si es así, no se permite eliminarla y se muestra un mensaje de error.
        flash("No se puede eliminar una factura pagada", "error")
        return redirect("/facturas")
    
    for item in factura.items: #Esta línea itera sobre los elementos (items) asociados a la factura y los elimina de la base de datos. Esto asegura que todos los elementos relacionados con la factura se eliminen antes de eliminar la factura en sí.
        db.session.delete(item)
    
    db.session.delete(factura)
    db.session.commit()
    flash("Factura eliminada exitosamente", "exito") #Esta linea muestra un mensaje rápido indicando que se elimino la factura
    return redirect("/facturas") #Esta línea redirige al usuario a la página de
    
if __name__ == "__main__": #Esta línea verifica si el archivo se está ejecutando directamente (no importado como módulo). Si es así, se ejecuta el bloque de código dentro de esta condición.
    with app.app_context():
        db.create_all()
    app.run(debug=True)