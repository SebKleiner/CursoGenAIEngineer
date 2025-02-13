# pip install supabase
import os

from supabase import create_client, Client

# Retrieve Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Check if the environment variables are set
if not SUPABASE_URL or not SERVICE_ROLE_KEY:
    raise ValueError("Missing Supabase URL or Service Role Key in environment variables.")


# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

def insert_data(table: str, data: dict):
    """Insert a record into a Supabase table."""
    response = supabase.table(table).insert(data).execute()
    return response

def update_data(table: str, email: str, updates: dict):
    """Update records in a Supabase table based on filters."""
    response = (
        supabase.table(table)
        .update(updates)
        .eq('email',email)
        .execute()
    )
    return response

def select_data(table: str, email: str = None):
    """Select records from a Supabase table based on optional filters."""
    response = (
        supabase.table(table)
        .select("*")
        .eq('email',email)
        .execute()
    )
    return response

# Example usage
if __name__ == "__main__":
    # # Insert example
    # insert_response = insert_data("users", {"name": "John Doe", "email": "john@example.com"})
    # print("Insert Response:", insert_response)

    # Update example
    # update_response = update_data("users", "john@example.com", {"name": "John Updated"})
    # print("Update Response:", update_response)

    # # Select example
    select_response = select_data("users", "john@example.com")
    first_result = select_response.data[0]['name']
    print("Select Response:", first_result)
