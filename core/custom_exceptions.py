from fastapi import HTTPException


def raise_exception(status: int = 400, info: str = "Something went wrong"):
    raise HTTPException(status_code=status, detail=info)


def invalid_id(id_number, http_status: int = 400, message: str = "item_id must be a positive integer number"):
    if not isinstance(id_number, int) or id_number < 1:
        raise_exception(status=http_status, info=message)


def non_existent_object(http_status: int = 404, message: str = "There are no objects with this id"):
    raise_exception(status=http_status, info=message)


def non_existing_foreign_key(http_status: int = 400, message: str = "There are no candidates with such id"):
    raise_exception(status=http_status, info=message)
