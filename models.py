from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db_conection import Base

class departamentos(Base):
    __tablename__= "Departamentos"

    id_departamento = Column(String(50), primary_key=True)
    nombre_departamento = Column(String(50), unique=True)

class empleados(Base):
    __tablename__ = "Empleados"

    id_empleado = Column(String(50), primary_key=True)
    documento = Column(String(50), unique=True, nullable=False)
    nombre_completo = Column(String(50))
    correo= Column(String(50), unique=True)
    contraseña = Column(String(500))
    salario = Column(Integer)
    area = Column(String(50), ForeignKey("Departamentos.id_departamento"))
    pago_realizado = Column(Boolean, default=False)

