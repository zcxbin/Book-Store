from schemas.base_response import BaseResponse

ERROR_CODES = {
    101: 'Author not found',
    201: 'Category not exist'
}


def raise_error(error_code: int) -> BaseResponse:
    return BaseResponse(
        message=ERROR_CODES.get(error_code),
        status='error',
    )
