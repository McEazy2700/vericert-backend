from dataclasses import dataclass
import json
from fastapi import UploadFile
from pydantic import BaseModel
import requests
from graphql import GraphQLError
from veecert_backend.config.settings import settings
from typing import Any, Dict, Optional, Tuple, cast

from strawberry.file_uploads import Upload


PINATA_API_ENDPOINT = "https://api.pinata.cloud"


class PinataResponse(BaseModel):
    IpfsHash: str
    PinSize: int
    Timestamp: str
    isDuplicate: Optional[bool] = None


@dataclass()
class PinataMetadata:
    name: Optional[str] = None
    keyvalues: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return {"name": self.name, "keyvalues": self.keyvalues}


class Pinata:
    @classmethod
    async def pin_file_to_ipfs(
        cls, file: Upload, metadata: Optional[PinataMetadata] = None
    ) -> PinataResponse:
        headers = {
            "pinata_api_key": settings.pinyata_api_key,
            "pinata_secret_api_key": settings.pinyata_api_secret,
            # "Authorization": f"Bearer {settings.pinyata_jwt}"
        }
        file_content = await file.read()  # type: ignore
        file_upload = cast(UploadFile, file)
        print(file_upload)
        files: Dict[str, Upload | Tuple[Any, Any, str]] = {
            "file": (
                str(file_upload.filename),
                file_content,
                file_upload.content_type or "",
            ),
        }
        if metadata is None:
            metadata = PinataMetadata(name=file_upload.filename)
        if metadata.keyvalues is None:
            metadata.keyvalues = {}
        metadata.keyvalues["size"] = file_upload.size
        files["pinataMetadata"] = (
            None,
            json.dumps(metadata.to_dict()),
            "application/json",
        )

        response = requests.post(
            f"{PINATA_API_ENDPOINT}/pinning/pinFileToIPFS", headers=headers, files=files
        )
        print(response.status_code)
        if response.status_code == 200:
            response_data = response.json()
            return PinataResponse.model_validate(response_data)
        else:
            raise GraphQLError("Failed to pin file")
