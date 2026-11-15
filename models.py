from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    ciudad = db.Column(db.String(100))
    pais = db.Column(db.String(100))
    
class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="Pendiente")
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    cliente = db.relationship("Cliente", backref="facturas")
    items = db.relationship("ItemFactura", backref="factura")
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.items) #Esta línea define una propiedad llamada total que calcula la suma de los subtotales de todos los items asociados a la factura. Utiliza una expresión generadora para iterar sobre la lista de items y sumar sus subtotales, proporcionando así el total de la factura.

class ItemFactura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    factura_id = db.Column(db.Integer, db.ForeignKey("factura.id"), nullable=False)
    
    @property
    def subtotal(self):
        return self.cantidad * self.valor_unitario #Esta línea define una propiedad llamada subtotal que calcula el subtotal de un item de factura multiplicando la cantidad por el valor unitario. Esto permite obtener el costo total de ese item específico en la factura.