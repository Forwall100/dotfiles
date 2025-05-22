import urllib.parse
import base64
from fastapi import APIRouter, HTTPException
import sqlite3
import requests
import uuid
import os
from utils.diagram_creator import generate_er_diagram

router = APIRouter()


@router.get("/er-diagram")
async def generate_er_diagram_endpoint(record_id: str):
    db_file_url = None
    conn = None
    try:
        response = requests.get(
            f"http://127.0.0.1:8090/api/collections/tests/records/{record_id}")
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error retrieving record with ID {record_id}: {response.text}"
            )
        record = response.json()
        db_file_url = f"http://127.0.0.1:8090/api/files/tests/{record_id}/{record.get('db_file')}"

        file_name = str(uuid.uuid4())

        # Download the database file
        urllib.request.urlretrieve(db_file_url, file_name)

        # Generate the ER diagram using the database file
        er_diagram_binary = generate_er_diagram(file_name)

        # Close the connection and remove the temporary database file
        os.remove(file_name)

        # Encode the binary data as Base64
        er_diagram_base64 = base64.b64encode(er_diagram_binary).decode("utf-8")

        return {"er_diagram": er_diagram_base64}
    except HTTPException:
        raise
    except Exception as e:
        if os.path.exists(file_name):
            os.remove(file_name)
        raise HTTPException(status_code=500, detail=str(e))

