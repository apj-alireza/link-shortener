from fastapi import FastAPI
from api.users import router as users_router
from api.links import router as links_router


app = FastAPI(title="Link shortener API")

app.include_router(users_router)
app.include_router(links_router)
