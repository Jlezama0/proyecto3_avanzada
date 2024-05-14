import cruds
from sqlalchemy.orm import Session
import main
from fastapi import Depends
import models
from db_conection import SessionLocal, engine
from fpdf import FPDF
from datetime import datetime


date = datetime.now()
fecha = f"{date.day}/{date.month}/{date.year}"


def generate_pdf(db : Session):

        empleados = cruds.get_empleados(db, skip=0, limit=100)

        for empleado in empleados:

                empleado_dict={
                        "id_empleado": empleado.id_empleado,
                        "documento": empleado.documento,
                        "nombre_completo": empleado.nombre_completo,
                        "correo": empleado.correo,
                        "salario": empleado.salario,
                        "area": empleado.area,
                        "pago_realizado": empleado.pago_realizado
                }

                if empleado_dict["pago_realizado"] == False :
                        pdf = FPDF(orientation="P", unit="mm", format="A4")
                        pdf.add_page()
                        pdf.set_font('Arial','', 10)

                        pdf.cell(w=190, h=15, txt="Comprobante nomina", border="B", ln=1,
                                align="C", fill=0)

                        pdf.multi_cell(w=0, h=5, txt=f"Fecha: {fecha}\nNombre:  {empleado_dict['nombre_completo']}\nDocumento:  {empleado_dict['documento']}\nCorreo:   {empleado_dict['correo']}\nArea:  {empleado_dict['area']}\n", border=0,
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
                        print(f"Archivo PDF generado: pdfs/pago_{nombre}.pdf")

                        cruds.actualizar_pago_realizado(empleado_dict["id_empleado"], db)




