from fastapi import FastAPI, Depends, HTTPException, status
import pytz
from sqlalchemy.orm import Session
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import  timedelta
import cruds, models, schemas
from db_conection import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''CRUD para empleados: Este crud permite hacer login a cada empleado, ademas permite la visualización
    de todos los registros, de un registro utilizando el numero de identificacion y la actulización de
    datos personales, como lo puede ser el nombre y el correo. '''

@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = cruds.authenticate_user(form_data.username, form_data.password, db)
    access_token_expires = timedelta(minutes=cruds.ACCESS_TOKEN_DURATION)
    access_token = cruds.create_access_token(
        data={"sub": user.documento},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    

@app.get("/empleado/{doc_empleado}", response_model=schemas.EmpleadoBase)
def get_empleado(doc_empleado: str, db: Session= Depends(get_db)):
    db_empleado= cruds.get_empleado_by_documento(db, documento=doc_empleado)
    if db_empleado is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_empleado

@app.get("/empleados/", response_model=list[schemas.EmpleadoBase])
def obtener_empleados(db: Session= Depends(get_db), skip: int = 0, limit: int = 100):
    users = cruds.get_empleados(db , skip=skip, limit=limit)
    print(users)
    return users

@app.put("/actualizarInfo/", response_model=schemas.InfoEmpleado)
def actualizarInfo(empleado: schemas.InfoEmpleado,db: Session= Depends(get_db) ):
    print(empleado.documento)
    db_empleado = cruds.get_empleado_by_documento(db, documento=empleado.documento)
    print(db_empleado)
    if db_empleado:
        cruds.actualizarInfoPers(db, empleado=empleado, documento=empleado.documento)
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Registro actualizado.")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado.")
    
'''CRUD para recursos humanos: Este crud permite actualizar la informacion del empleado, crear un nuevo empleado
    y eliminacion de registros. Para poder acceder a estos privilegios, se pide un token de autorizacion, el cual se
    genera en el archivo cruds.py y mira si el token suministrado da acceso a estas funciones, de lo contrario no se
    permite hacer uso de esta funciones. '''
    

@app.put("/actualizarEmpleado/")
def actualizar_empleado(verify: schemas.Actualizar_empleado,db: Session= Depends(get_db) ):
    verify_auth = cruds.verify_token(verify.Autorizacion , db)
    print(verify.id_empleado)
    if verify_auth:
        db_empleado = cruds.get_empleado_by_id(db, id_empleado=verify.id_empleado)
        if db_empleado:
            cruds.actualizar_empleado(db, empleado=verify.Info_empleado, id_empleado=verify.id_empleado)
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Registro actualizado.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado.")


@app.post("/crearEmpleado/", response_model=schemas.EmpleadoBase)
def crear_empleado(empleado: schemas.Crear_empleado,db: Session= Depends(get_db)):
    verify_auth = cruds.verify_token(empleado.Autorizacion , db)
    if verify_auth:
        db_empleado = cruds.get_empleado_by_documento(db, documento=empleado.Empleado.documento)
        print(db_empleado)
        if db_empleado:
            raise HTTPException(status_code=400, detail="Documento ya registrado")
        else:
            return cruds.crear_empleado(db=db, empleado=empleado.Empleado)

@app.delete("/eliminarRegistro/")
def eliminar_empleado(verify: schemas.Eliminar_empleado, db: Session= Depends(get_db)):
    verify_auth = cruds.verify_token(verify.Autorizacion , db)
    if verify_auth:
        db_empleado = cruds.get_empleado_by_documento(db, documento=verify.Doc_empleado)
        if db_empleado:
            db.delete(db_empleado)
            db.commit()
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Registro eliminado.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado.")
    
@app.post("/crear/", response_model=schemas.EmpleadoBase)
def crear_empleado(empleado: schemas.EmpleadoCreado,db: Session= Depends(get_db)):

    db_empleado = cruds.get_empleado_by_documento(db, documento=empleado.documento)
    print(db_empleado)
    if db_empleado:
        raise HTTPException(status_code=400, detail="Documento ya registrado")
    else:
        return cruds.crear_empleado(db=db, empleado=empleado)
    
# Unicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc

