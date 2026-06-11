from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/health", tags=["Invoices"])

@router.get("/",)
def health():
    return {"status": "ok"}