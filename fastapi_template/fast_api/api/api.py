import os

from fastapi import HTTPException, APIRouter, Request
from supabase import create_client

from ..schemas.models import TemplateRequest

# Initialize with your Supabase project URL and API key
SUPABASE_URL = ""
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
API_KEY = os.getenv('API_KEY')

# Create an APIRouter instance
router = APIRouter()


@router.post("/endpoint")
def hello_world(data: TemplateRequest):
   return {"Hello": "World"}

@router.get("/")
def read_root():
    print(API_KEY)
    return {"Hello": "World", "SUPABASE_KEY": SUPABASE_KEY}
