from fastapi import APIRouter

from routes import health, forms

apiRouter = APIRouter()
apiRouter.include_router(health.router)
apiRouter.include_router(forms.router)
