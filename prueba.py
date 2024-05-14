import cruds
from sqlalchemy.orm import Session
import main
from fastapi import Depends
import models
from db_conection import SessionLocal, engine
from fpdf import FPDF


def ingreso_db(db: Session=Depends(main.get_db)):
    return db.query(models.empleados).all()

def actualizar_pago_realizado(db: Session, empleados: models.empleados):
        empleados.pago_realizado = 1
        db.commit()

db= Session(engine)

empleados = ingreso_db(db)



def generate():
    for i in empleados:
        print(i)
        empleado_dict={
            "id_empleado": i.id_empleado,
            "documento": i.documento,
            "nombre_completo": i.nombre_completo,
            "correo": i.correo,
            "salario": i.salario,
            "area": i.area
        }
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font('Arial','', 10)

        pdf.cell(w=190, h=15, txt="Comprobante nomina", border="B", ln=1,
                align="C", fill=0)

        pdf.multi_cell(w=0, h=5, txt=f"\nNombre:  {empleado_dict['id_empleado']}\nDocumento:  {empleado_dict['documento']}\nCorreo:   {empleado_dict['correo']}\nArea:  {empleado_dict['area']}\n\n\n", border=0,
                        align="L", fill=0)

        pdf.cell(w=180, h=15, txt="Ingresos", border="TLR", ln=3,
                align="C", fill=0)

        pdf.cell(w=90, h=10, txt="Conceptos", border=1, 
                align="C", fill=0)
        pdf.multi_cell(w=90, h=10, txt="Valor", border=1, 
                align="C", fill=0)

        pdf.cell(w=90, h=10, txt="sueldo", border=1, 
                align="C", fill=0)
        pdf.multi_cell(w=90, h=10, txt=str(empleado_dict["salario"]), border=1, 
                align="C", fill=0)

        total_ingresos = empleado_dict["salario"]

        pdf.cell(w=90, h=10, txt="Total ingreso:      ", border=1, 
                align="R", fill=0)
        pdf.multi_cell(w=90, h=10, txt=str(total_ingresos), border=1, 
                align="C", fill=0)
        
        nombre_com = empleado_dict["nombre_completo"]
        nombre = nombre_com.replace(' ', '_')

        pdf.output(f"pdfs/pago_{nombre}.pdf")


