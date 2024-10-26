from schemas.base_response import BaseResponse

ERROR_CODES = {
    101: 'Author not found',
    201: 'Category not exist',
    301: 'Not enough book quantity',
    302: 'Book quantity order incorrect',
    401: 'You dont have admin permission',
    501: 'You don\'t have any orders'
}


def raise_error(error_code: int) -> BaseResponse:
    return BaseResponse(
        message=ERROR_CODES.get(error_code),
        status='error',
    )
