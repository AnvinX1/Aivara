
import os
import sys # Added

from fastapi import APIRouter, status

_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

router = APIRouter()

@router.post("/sync", status_code=status.HTTP_200_OK)
def abha_sync_mock():
    """
    Mock endpoint for ABHA synchronization.
    In a real application, this would handle actual ABHA integration logic.
    """
    return {"message": "ABHA synchronization initiated successfully (mock response)."}
