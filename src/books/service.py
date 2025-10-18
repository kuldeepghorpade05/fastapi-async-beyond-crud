from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from .schemas import BookCreateModel, BookUpdateModel

class BookService:
    async def get_all_books(self, session: AsyncSession):
        result = await session.exec(select(Book).order_by(Book.created_at.desc()))
        return result.all()

    async def get_user_books(self, user_uid: str, session: AsyncSession):
        result = await session.exec(
            select(Book).where(Book.user_uid == user_uid).order_by(Book.created_at.desc())
        )
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        result = await session.exec(select(Book).where(Book.uid == book_uid))
        return result.first()

    async def create_book(self, book_data: BookCreateModel, user_uid: str, session: AsyncSession):
        book_dict = book_data.model_dump()
        new_book = Book(**book_dict)
        new_book.published_date = datetime.strptime(book_dict["published_date"], "%Y-%m-%d")
        new_book.user_uid = user_uid
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        if not book_to_update:
            return None
        update_dict = update_data.model_dump(exclude_unset=True)
        for k, v in update_dict.items():
            setattr(book_to_update, k, v)
        await session.commit()
        await session.refresh(book_to_update)
        return book_to_update

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if not book_to_delete:
            return None
        await session.delete(book_to_delete)
        await session.commit()
        return {}
