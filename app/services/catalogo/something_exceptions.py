from app.common.exceptions import ConflictException, NotFoundException



class SomethingAlreadyExistsException(ConflictException):
    def __init__(self):
        details = [
            {
                "message": "Este Produto já existe",
                "slug": "409-produto-ja-existe",
            }
        ]
        super().__init__(details)

class ProductNotExistException(NotFoundException):
    def __init__(self):
        details = [
            {
                "message": "Este Produto não existe",
                "slug": "404-produto-não-existe",
            }
        ]
        super().__init__(details)

class ProductNameLengthException(NotFoundException):
    def __init__(self):
        details = [
            {
                "message": "Nome do Produto fora do tamanho permitido",
                "slug": "404-tamanho-nome-produto-não-permitido",
            }
        ]
        super().__init__(details)

class SellerIDException(NotFoundException):
    def __init__(self):
        details = [
            {
                "message": "Seller ID Inválido",
                "slug": "404-seller-id-invalido",
            }
        ]
        super().__init__(details)
class NoFieldsToUpdateException(NotFoundException):
    def __init__(self):
        details = [
            {
                "message": "Nenhum campo válido para atualizar",
                "slug": "400-nenhum-campo-para-atualizar",
            }
        ]
        super().__init__(details)
