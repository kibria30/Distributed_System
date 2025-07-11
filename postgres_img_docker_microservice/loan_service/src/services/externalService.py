import os
import httpx

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL")

async def get_user(user_id):
    url = f"{USER_SERVICE_URL}/api/v1/users/{user_id}"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        
    except httpx.RequestError as e:
        print(f"Error fetching user {user_id}: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"Error fetching user {user_id}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching user {user_id}: {e}")
        return None


async def get_book(book_id):
    url = f"{BOOK_SERVICE_URL}/api/v1/books/{book_id}"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error fetching book {book_id}: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"Error fetching book {book_id}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching book {book_id}: {e}")
        return None


async def update_book(book_id, copies, available_copies):
    url = f"{BOOK_SERVICE_URL}/api/v1/books/{book_id}"
    data = {
        "copies": copies,
        "available_copies": available_copies
    }
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.put(url, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error updating book {book_id}: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"Error updating book {book_id}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error updating book {book_id}: {e}")
        return None

