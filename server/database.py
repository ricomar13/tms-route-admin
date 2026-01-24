import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
        
def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)


#if __name__ == "__main__":
 #   drop_db_and_tables()
  #  create_db_and_tables()