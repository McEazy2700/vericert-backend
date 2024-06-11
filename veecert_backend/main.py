import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from veecert_backend.config.schema import schema
from veecert_backend.config.context import get_app_context
from veecert_backend.config.settings import settings

app = FastAPI()
allowed_origins = settings.allowed_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def on_startup():
    subprocess.run(["alembic", "upgrade", "head"])


app.add_event_handler("startup", on_startup)
graphql_app = GraphQLRouter(schema=schema, context_getter=get_app_context)

app.include_router(
    graphql_app,
    prefix="/graphql",
)
