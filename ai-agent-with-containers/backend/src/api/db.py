import os
import sqlmodel 
from sqlmodel import Session, SQLModel

DATABASE_URL=os.environ.get("DATABASE_URL", None) 
if not DATABASE_URL:
    raise ValueError("`DATABASE_URL` environment variable is not set")

engine = sqlmodel.create_engine(DATABASE_URL, echo=True)

# database models
def init_db():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)

# api routes
def get_session():
    with Session(engine) as session:
        yield session