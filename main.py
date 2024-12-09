from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi import APIRouter
app = FastAPI()
router = APIRouter(
    prefix="/home"
)

@router.post("/getStart")
def start():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message":"Run"}
    )