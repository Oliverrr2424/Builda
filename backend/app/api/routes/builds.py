from fastapi import APIRouter

from app.schemas.build import BuildValidationRequest, BuildValidationResult
from app.services.sample_data import validate_build

router = APIRouter(prefix="/builds", tags=["builds"])


@router.post("/validate", response_model=BuildValidationResult)
async def validate(payload: BuildValidationRequest) -> BuildValidationResult:
    """Run a basic compatibility validation example."""

    # TODO: Implement real compatibility validation logic using payload.items
    return validate_build()
