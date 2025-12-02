from fastapi import APIRouter, Depends, HTTPException, status

from fastapi_limiter.depends import RateLimiter

from app.summaries.schemas import SummaryPublic, SummaryPost, SummaryUpdate, SummaryDelete
from app.summaries.summarize import summarize
from app.summaries.data_access import SummaryDA
from app.redis import set_storage


router = APIRouter(prefix='/summary', tags=['Summaries'])

storage = set_storage(SummaryPublic)


@router.get('/text/{id}')
async def get_summary(id: int) -> SummaryPublic:
    instance = await storage.get(str(id))
    if instance:
        return instance
    
    instance = await SummaryDA.get(id=id)
    if instance:
        _ = await storage.store(str(id), SummaryPublic.model_validate(instance.to_dict()))
        return instance
    
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.post('/text', dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def make_summary(request_body: SummaryPost) -> SummaryPublic:
    instance = await SummaryDA.get(**request_body.model_dump())
    if instance:
        return instance

    summarized_text = summarize(request_body.source_text)
    values = request_body.model_dump() | {'summarized_text': summarized_text}    
    new_instance = await SummaryDA.create(**values)
    
    return new_instance


@router.put('/text', dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def update_summary(request_body: SummaryUpdate) -> SummaryUpdate:
    filter_by = {'id': request_body.id}
    is_updated = await SummaryDA.update(
        filter_by, source_text=request_body.updated_text
    )
    
    if is_updated:
        instance = await SummaryDA.get(**filter_by)
        return instance # type: ignore
    
    raise HTTPException(status.HTTP_304_NOT_MODIFIED)


@router.delete('/text', dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def delete_summary(request_body: SummaryDelete) -> dict:
    is_deleted = await SummaryDA.delete(**request_body.to_dict())
    if is_deleted:
        return {'message': 'ok'}
    
    raise HTTPException(status.HTTP_404_NOT_FOUND)
