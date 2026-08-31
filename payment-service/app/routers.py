from fastapi import APIRouter
from fastapi import Request
from app.schemas import PaymentCreateSchema, PaymentSchema
from app.services import PaymentService
from app.database import DBDep
router = APIRouter(prefix='/payments')

@router.get("", response_model=list[PaymentSchema])
async def get_payments(
    db: DBDep
):
    return await PaymentService(db).get_payments()

@router.post("")
async def add_payment(
    request: Request,
    payment: PaymentCreateSchema,
    db: DBDep
):
    payment = await PaymentService(db).create_payment(payment)
    await PaymentService(db).complete_payment(payment, exchange=request.app.state.payment_exchange, kafka_producer=request.app.state.kafka_producer)



@router.get("/{id_order}", response_model=PaymentSchema)
async def get_payment(
    id_payment: str,
    db: DBDep
):
    return await PaymentService(db).get_order_or_none(id_payment)




@router.delete("/{id_order}")
def delete_payment(
    id_product: str,
    db: DBDep
):
    return None




