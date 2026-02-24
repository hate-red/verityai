from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker


class BaseDA:
    model = None


    @classmethod
    async def get(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by) # type: ignore
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
        
        return instance
    

    @classmethod
    async def get_or_create(cls, **values):
        instance = await cls.get(**values)
        
        if not instance:
            instance = await cls.create(**values)
        
        return instance


    @classmethod
    async def create(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values) # type: ignore
                session.add(new_instance)

                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
        
        return new_instance


    @classmethod
    async def filter(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by) # type: ignore
            result = await session.execute(query)
            instances = result.scalars().all()
        
        return instances


    @classmethod
    async def update(cls, filter_by: dict, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    update(cls.model) # type: ignore
                    .where(
                        *[getattr(cls.model, key) == value
                        for key, value in filter_by.items()]
                    )
                    .values(**values)
                    .execution_options(synchronize_session='fetch')
                )
                result = await session.execute(query)

                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

        return result.rowcount # type: ignore


    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            async with session.begin():
                query = delete(cls.model).filter_by(**filter_by) # type: ignore
                result = await session.execute(query)

                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                
        return result.rowcount # type: ignore
