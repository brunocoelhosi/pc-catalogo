from app.common.exceptions import ConflictException


class SomethingAlreadyExistsException(ConflictException):
    def __init__(self):
        details = [
            {
                "message": "Este Produto já existe",
                "slug": "409-produto-ja-existe",
            }
        ]
        super().__init__(details)
