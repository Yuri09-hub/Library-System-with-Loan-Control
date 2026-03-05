from fastapi import APIRouter


loan_router = APIRouter(prefix="/loan", tags=["loan"])


@loan_router.get("/", tags=["loan"])
async def loan_routter():
    return {"message": "loan routed successfully"}