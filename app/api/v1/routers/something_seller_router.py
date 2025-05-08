from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status


from app.api.common.schemas import ListResponse, Paginator, UuidType, get_request_pagination
from app.container import Container

from ..schemas.something_schema import SomethingCreate, SomethingResponse, SomethingUpdate
from . import SOMETHING_PREFIX



if TYPE_CHECKING:
    from app.services import SomethingService


router = APIRouter(prefix=SOMETHING_PREFIX, tags=["CRUD Catálogo"])

##Busca todos os produtos
@router.get("",
    response_model=ListResponse[SomethingResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_products(
    paginator: Paginator = Depends(get_request_pagination),
    something_service: "SomethingService" = Depends(Provide[Container.something_service]),
):
    results = await something_service.find(paginator=paginator, filters={})

    return paginator.paginate(results=results)


#Busca o produto pelo ID
@router.get(
    "/{seller_id}",
    response_model=SomethingResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_by_id(
    seller_id: str,
    something_service: "SomethingService" = Depends(Provide[Container.something_service]),
):
    return await something_service.find_by_id(seller_id)

#Busca o produto pelo ID + SKU
@router.get(
    "/{seller_id}/{sku}",
    response_model=SomethingResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_product(
    seller_id: str,
    sku: str,
    something_service: "SomethingService" = Depends(Provide[Container.something_service]),
):
    return await something_service.find_product(seller_id, sku)


#CADASTRO DE UM PRODUTO
@router.post(
    "",
    response_model=SomethingResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create(
    something: SomethingCreate, something_service: "SomethingService" = Depends(Provide[Container.something_service])
):
    try:
        # Tenta encontrar o produto pelo seller_id e SKU
        product_exist = await something_service.find_product(something.seller_id, something.sku)
    except HTTPException:
        # Se o produto não for encontrado, continua o fluxo normalmente
        product_exist = None

    # Se o produto já existir, lança uma exceção
    if product_exist:
        raise HTTPException(status.HTTP_409_CONFLICT,"Produto já cadastrado.")

    # Cria o produto
    return await something_service.create(something)


@router.patch(
    "/{seller_id}",
    response_model=SomethingResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def update_by_id(
    seller_id: str,
    something: SomethingUpdate,
    something_service: "SomethingService" = Depends(Provide[Container.something_service]),
):
    return await something_service.update(seller_id, something)


@router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete(
    seller_id: UuidType, something_service: "SomethingService" = Depends(Provide[Container.something_service])
):
    await something_service.delete_by_id(seller_id)
