
import os
import sys

from fastapi import APIRouter

_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from api.routes import auth, reports, analysis, doctor, abha, hospital, forecasting

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(analysis.router, prefix="/ai", tags=["AI Analysis"])
api_router.include_router(doctor.router, prefix="/doctor", tags=["Doctor Review"])
api_router.include_router(abha.router, prefix="/abha", tags=["ABHA Integration"])
api_router.include_router(hospital.router, prefix="/hospitals", tags=["Hospitals"])
api_router.include_router(forecasting.router, prefix="/forecasting", tags=["Forecasting"])
