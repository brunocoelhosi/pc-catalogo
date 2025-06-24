from fastapi import HTTPException, status
from fastapi.requests import Request


async def get_seller_id(request: Request) -> str:
    seller_id = request.headers.get("x-seller-id")
    if not seller_id:
        raise HTTPException(
            # XXX Teria um outro melhor?
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Faltando cabeçalho x-seller-id",
        )

    return seller_id
