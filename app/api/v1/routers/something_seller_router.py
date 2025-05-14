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

##BUSCAR TODOS OS PRODUTOS
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

#BUSCAR PRODUTO POR SELLER_ID + SKU
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
    # Valida se o produto pode ser criado
    await something_service.validate_product_creation(something.seller_id, something.sku)

    # Cria o produto
    return await something_service.create(something)

#DELETA UM PRODUTO
@router.delete("/{seller_id}/{sku}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete(
    seller_id: str,
    sku: str,
    something_service: "SomethingService" = Depends(Provide[Container.something_service]),
):
    product = await something_service.find_product(seller_id, sku)
 
    await something_service.delete_product(product)


"""nao utilizadas"""

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