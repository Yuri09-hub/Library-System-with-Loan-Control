from fastapi import APIRouter

book_router = APIRouter(prefix="/book", tags=["book"])


@book_router.post("/", tags=["book"])
async def book_routte():
    return {"message": "book routed successfully"}
