import os
from sqlmodel import  create_engine, Session
from dotenv import load_dotenv


load_dotenv()  #.env file ki value load karne ke liye
DB_USER= os.getenv('DB_USER')
DB_PASSWORD= os.getenv('DB_PASSWORD')
DB_HOST= os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_NAME= os.getenv('DB_NAME')

# DATABASE_URL= f'postgresql://postgres:yourpassword@localhost:5432/eskills_db' # for database connection
DATABASE_URL= f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine= create_engine(DATABASE_URL, echo= True)

def get_session():
    with Session (engine) as session:
        # yield session  #both are working and CRUD operation is performing
        return session