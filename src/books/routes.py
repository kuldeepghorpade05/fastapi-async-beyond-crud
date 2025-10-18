from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.books.service import BookService
from src.db.main import get_session
from .schemas import Book, BookCreateModel, BookDetailModel, BookUpdateModel
from src.errors import BookNotFound

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))

@book_router.get("/", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    return await book_service.get_all_books(session)

@book_router.get("/user/{user_uid}", response_model=List[Book], dependencies=[role_checker])
async def get_user_books(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    return await book_service.get_user_books(user_uid, session)

@book_router.get("/{book_uid}", response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session), _: dict = Depends(access_token_bearer)):
    book = await book_service.get_book(book_uid, session)
    if not book:
        raise BookNotFound()
    return book

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker])
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    user_id = token_details["user"]["user_uid"]
    return await book_service.create_book(book_data, user_id, session)

@book_router.patch("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session), _: dict = Depends(access_token_bearer)):
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if not updated_book:
        raise BookNotFound()
    return updated_book

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session), _: dict = Depends(access_token_bearer)):
    deleted = await book_service.delete_book(book_uid, session)
    if deleted is None:
        raise BookNotFound()
    return {}
