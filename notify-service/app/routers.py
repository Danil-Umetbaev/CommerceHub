from fastapi import APIRouter
from app.schemas import NotifySchema, NotifyCreateSchema, NotifyUpdateSchema
from app.services import NotifyService
from app.database import DBDep
router = APIRouter(prefix='/payments')

@router.get("/", response_model=list[NotifySchema])
async def get_notifys(
    db: DBDep
):
    return await NotifyService(db).get_notifyes()

@router.post("/")
async def add_notify(
    notify: NotifyCreateSchema,
    db: DBDep
):
    return await NotifyService(db).create_notify(notify)




@router.get("/{id_notify}", response_model=NotifySchema)
async def get_notify(
    id_payment: str,
    db: DBDep
):
    return await NotifyService(db).get_notify_or_none(id_payment)




@router.delete("/{id_notify}")
async def delete_notify(
    id_notify: str,
    db: DBDep
):
    return await NotifyService(db).delete_notify(id_notify)


@router.put("/{id_notify}")
async def update_notify(
    notify: NotifyUpdateSchema,
    id_notify: str,
    db: DBDep
):
    return await NotifyService(db).update_notify(notify, id=id_notify)


@router.patch("/{id_notify}")
async def patch_update_notify(
    notify: NotifyUpdateSchema,
    id_notify: str,
    db: DBDep
):
    return await NotifyService(db).update_notify(notify, exclude_unset=True, id=id_notify)




