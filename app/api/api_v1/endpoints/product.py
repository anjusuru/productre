from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Any, List

from app import schemas, models, crud

from app.api import session


router = APIRouter()


@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.CreateProduct, db: Session = Depends(session.get_db)
) -> JSONResponse:
    product_in = schemas.CreateProduct(**product.dict())
    product_in_db = crud.product_obj.create(db, product_in)
    status_code = status.HTTP_201_CREATED
    resp_data = {
        "product_id": product_in_db.id,
        "message": "Product Created",
    }
    return JSONResponse(status_code=status_code, content=resp_data)


@router.get("/{id}", response_model=schemas.Product)
def get_product(
    id: int,
    db: Session = Depends(session.get_db),
) -> Any:

    product_indb = crud.product_obj.get(db=db, id=id)

    status_code = status.HTTP_404_NOT_FOUND
    resp_data = {
        "product_id": id,
        "message": "product not found",
    }
    if product_indb:
        return product_indb
    else:
        return JSONResponse(status_code=status_code, content=resp_data)


@router.get("/", response_model=List[schemas.Product])
def get_products(
    skip: int = 0, limit: int = 100, db: Session = Depends(session.get_db)
) -> Any:

    products = crud.product_obj.get_many(db=db, skip=skip, limit=limit)

    return products


@router.put("/{id}", response_model=schemas.Product)
def update_product(
    id: int, product_in: schemas.UpdateProduct, db: Session = Depends(session.get_db)
) -> JSONResponse:

    product_db = crud.product_obj.get(db=db, id=id)
    # product_in = schemas.UpdateProduct(**product.dict())
    status_code = status.HTTP_404_NOT_FOUND
    resp_data = {
        "product_id": product_db.id,
        "message": "Product not found",
    }
    if not product_db:
        return JSONResponse(status_code=status_code, content=resp_data)
    product = crud.product_obj.update(db=db, db_obj=product_db, obj_in=product_in)
    return product


@router.delete("/{id}", response_model=schemas.Product)
def delete_item(
    *,
    db: Session = Depends(session.get_db),
    id: int,
) -> Any:

    # product_indb = crud.product_obj.get(db=db, id=id)
    product = crud.product_obj.delete(db=db, id=id)
    status_code = status.HTTP_404_NOT_FOUND
    resp_data = {
        "product_id": id,
        "message": "Product not found",
    }
    if not product:
        return JSONResponse(status_code=status_code, content=resp_data)

    # product = crud.product_obj.delete(db=db, id=id)
    return product
