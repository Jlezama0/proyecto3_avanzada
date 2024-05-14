from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import models
import schemas
import bcrypt
import pytz

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30
SECRET = "Proyecto3@proAvan&2024"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypto = CryptContext(schemes=["bcrypt"])

def verify_password(plain_password, hashed_password):
    return crypto.verify(plain_password, hashed_password)

def authenticate_user(documento: str, contraseña: str, db: Session):
    user = get_empleado_by_documento(db, documento)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not verify_password(contraseña, user.contraseña):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(pytz.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(access_token: str, db: Session):
    
    try:
        payload = jwt.decode(access_token, SECRET, algorithms=[ALGORITHM])
        #print(payload.get("sub"))
        user_documento = payload.get("sub")
        db_empleado = get_empleado_by_documento(db, documento=user_documento)
        if db_empleado and db_empleado.area == "D01":
            return db_empleado
        else:
            raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail="Usted no está autorizado para realizar esta acción")
            
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


def get_empleado_by_documento(db: Session, documento: str):
    return db.query(models.empleados).filter(models.empleados.documento == documento).first()

def get_empleado_by_id(db: Session, id_empleado: str):
    return db.query(models.empleados).filter(models.empleados.id_empleado == id_empleado).first()

def get_contraseña(db:Session, documento: str):
    return db.query(models.empleados.contraseña).filter(models.empleados.documento == documento).first()

def crear_empleado(db: Session, empleado: schemas.EmpleadoCreado):
    contraseña=empleado.contraseña
    contraseña_encriptada = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt())
    db_empleado = models.empleados(id_empleado=empleado.id_empleado,
                                documento = empleado.documento, 
                                nombre_completo=empleado.nombre_completo,
                                correo=empleado.correo,
                                contraseña=contraseña_encriptada,
                                salario=empleado.salario,
                                area=empleado.area)
    db.add(db_empleado)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado

def get_empleados(db: Session, skip: int=0, limit: int=100):
    return db.query(models.empleados).offset(skip).limit(limit).all()

def actualizarInfoPers(db: Session, empleado: schemas.InfoEmpleado, documento: str):
    print("actualizando...")
    db.query(models.empleados).filter(models.empleados.documento == documento).update({"documento": empleado.documento,
                                                                                    "nombre_completo": empleado.nombre_completo,
                                                                                    "correo": empleado.correo})
    db.commit()

def actualizar_empleado(db: Session, empleado: schemas.GeneralEmpleado, id_empleado: str):
    db.query(models.empleados).filter(models.empleados.id_empleado == id_empleado).update({
                                                                                    
                                                                                    "documento": empleado.documento,
                                                                                    "nombre_completo": empleado.nombre_completo,
                                                                                    "correo": empleado.correo,
                                                                                    "salario": empleado.salario,
                                                                                    "area": empleado.area,
                                                                                    "pago_realizado":empleado.pago_realizado})
    db.commit()