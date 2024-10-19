from fastapi import FastAPI
from routers.authentication import router as authentication_router
from routers.book import router as book_router
from routers.review import router as review_router
from routers.order import router as order_router
from routers.permission import router as permission_router
app = FastAPI()


app.include_router(authentication_router, prefix="/auth", tags=["Authentication"])
app.include_router(book_router, prefix="/book", tags=["Books"])
app.include_router(review_router, prefix="/review", tags=["Reviews"])

app.include_router(order_router, prefix="/order", tags=["Orders"])
app.include_router(permission_router, prefix="/permission", tags=["Permissions"])
