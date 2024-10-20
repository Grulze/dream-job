from typing import List
from logging import getLogger

from fastapi import APIRouter, Depends
# from fastapi_cache.decorator import cache

from query_db import add_candidates_db, delete_candidates_db, get_candidates_db, update_candidates_db
from schema import CRUDSkills, RelationshipSkills, AddCandidates, UpdateCandidates, PATCHCandidates, GetCandidate
from custom_exceptions import invalid_id

# from redis_conf import check_cache_memory, clear_cache_on_update

crud_candidates = APIRouter(prefix="/candidates", tags=["CRUD candidates"])
crud_skills = APIRouter(prefix="/candidates/skills", tags=["CRUD skills"])


@crud_candidates.get("/{candidate_id}")
async def get_candidates(candidate_id: int) -> GetCandidate:
    invalid_id(id_number=candidate_id)
    return await get_candidates_db(candidate_id)


@crud_candidates.post("", status_code=201)
async def add_candidates(candidate_data: AddCandidates):
    await add_candidates_db(candidate_data)


@crud_candidates.put("/{candidate_id}", status_code=204)
async def candidates_user(candidate_id: int, data: UpdateCandidates):
    invalid_id(id_number=candidate_id)
    await update_candidates_db(candidate_id, data.dict())


@crud_candidates.patch("/{candidate_id}", status_code=201)
async def partial_update_candidates(candidate_id: int, data: PATCHCandidates):
    invalid_id(id_number=candidate_id)
    await update_candidates_db(candidate_id, data.dict(exclude_none=True))
    return await get_candidates_db(candidate_id)


@crud_candidates.delete("/{candidate_id}", status_code=204)
async def delete_candidates(candidate_id: int):
    invalid_id(id_number=candidate_id)
    await delete_candidates_db(candidate_id)









#
#
# @crud_skills.get("/{skill_id}")
# async def get_users(skill_id: int) -> AddCandidates:
#     invalid_id(id_number=skill_id)
#
#
# @crud_skills.post("", status_code=201)
# async def add_users(user_data: AddCandidates):
#     pass
#
#
# @crud_skills.put("/{skill_id}", status_code=204)
# async def update_user(skill_id: int):
#     invalid_id(id_number=skill_id)
#
#
# @crud_skills.patch("/{skill_id}", status_code=201)
# async def partial_update_user(skill_id: int):
#     invalid_id(id_number=skill_id)
#
#
# @crud_skills.delete("/{skill_id}", status_code=204)
# async def delete_user(skill_id: int):
#     invalid_id(id_number=skill_id)
#
#
#
#












#
#
# @router.get("")
# async def get_all_items(pagination: Pagination = Depends()) -> List[GetItems]:
#     """
#     Return all items from database with pagination.
#     :param pagination: class with information that used for pagination
#     :return: List[GetItems]
#     """
#
#     async def send_request_to_db():
#         return await get_items_db(lim=pagination.limit, page=pagination.page)
#
#     return await send_request_to_db()
#
#
# @crud_router.get("/{item_id}")
# async def get_items(item_id: int) -> List[GetItems]:
#     """
#     Return the item by the specified id from database.
#     :param item_id: id of item from database
#     :return: List[GetItem]
#     """
#
#     if type(item_id) != int or item_id < 1:
#         invalid_id()
#
#     async def send_request_to_db():
#         return await get_items_db(item_id_db=item_id)
#
#     return await send_request_to_db()
#
#
# @crud_router.post("", status_code=201)
# async def new_items(item: AddItems = Depends()):
#     """
#     Add a new item to the database.
#     :param item: class with information that needs to be added to database
#     :return: str
#     """
#
#     await add_items_db(item)
#
#
# @crud_router.put("/{item_id}", status_code=204)
# async def update_items(item_id: int, data: PutItems = Depends()):
#     """
#     Update all information about the product with the specified id.
#     :param item_id: id of item from database
#     :param data: class with information that needs to be updated in database
#     :return:
#     """
#
#     if type(item_id) != int or item_id < 1:
#         invalid_id()
#
#     await update_items_db(item_id, data.dict())
#
#
# @crud_router.patch("/{item_id}")
# async def partial_update_items(item_id: int, data: PatchItems = Depends()) -> List[GetItems]:
#     """
#     Update partial information about the product with the specified id.
#     :param item_id: id of item from database
#     :param data: class with a piece of information that needs to be updated in database
#     :return:
#     """
#
#     if type(item_id) != int or item_id < 1:
#         invalid_id()
#
#     await update_items_db(item_id, data.dict(exclude_none=True))
#     return await get_items_db(item_id)
#
#
# @crud_router.delete("/{item_id}", status_code=204)
# async def delete_items(item_id: int):
#     """
#     Delete item with the passed id.
#     :param item_id: id of item from database
#     :return: str
#     """
#
#     if type(item_id) != int or item_id < 1:
#         invalid_id()
#
#     await delete_items_db(item_id)
