from typing import Any, Dict, Iterator, List, Optional
from enum import Enum

from langchain_core.document_loaders.base import BaseLoader
from langchain_box.utilities import BoxAPIWrapper, BoxAuthType
from langchain_core.documents import Document
from langchain_core.pydantic_v1 import BaseModel, root_validator, ConfigDict, validator
from langchain_core.utils import get_from_dict_or_env

"""
    BoxAIMode - an enum to tell BoxAILoader which endpoint to use.

    Options are:
    ASK - provide `box_ai_prompt` and `[box_file_ids]`. Will return the response to your prompt.
"""


class BoxAIMode(Enum):
    ASK = "ask"


class BoxAILoader(BaseLoader, BaseModel):
    """
    BoxAILoader

    This class will help you load files from your Box instance. You must have a Box account.
    If you need one, you can sign up for a free developer account. You will also need a Box
    application created in the developer portal, where you can select your authorization type.
    If you wish to use either of the Box AI options, you must be on an Enterprise Plus plan or
    above. The free developer account does not have access to Box AI.

    In addition, using the Box AI API requires a few prerequisite steps:
    * Your administrator must enable the Box AI API
    * You must enable the `Manage AI` scope in your application in the developer console.
    * Your administratormust install and enable your application.

    Example Implementation
    ```
    ```

    Initialization variables
    variable | description | type | required
    ---+---+---
    mode | Box AI endpoint | enum | yes
    auth_type | authentication type to use | enum | yes
    box_developer_token | token to use for auth. Should only use for development | string | no
    box_client_id | client id for you app. Used for CCG | string | no
    box_client_secret | client secret for you app. Used for CCG | string | no
    box_user_id | User ID or Enterprise ID to make calls for. Used for CCG or JWT | string | no
    box_enterprise_id | Enterprise ID to make calls for. Used for CCG. | string | no
    box_jwt_path | Local file system path the the jwt config JSON | string | no
    box_file_ids | Array of Box file Ids to retrieve | array of strings | no
    box_ai_prompt | prompt to query Box AI to retrieve a response or citations | string | no
    """

    model_config = ConfigDict(use_enum_values=True)

    mode: BoxAIMode
    auth_type: BoxAuthType
    box_developer_token: Optional[str] = None
    box_client_id: Optional[str] = None
    box_client_secret: Optional[str] = None
    box_user_id: Optional[str] = None
    box_enterprise_id: Optional[str] = None
    box_jwt_path: Optional[str] = None
    box_file_ids: Optional[List[str]] = None
    box_ai_prompt: Optional[str] = None

    @validator("mode")
    def validate_mode(cls, value):
        if value is None and hasattr(BoxAIMode, value):
            raise ValueError("You must provide a valid mode")

        return value.value

    @validator("auth_type")
    def validate_auth_type(cls, value):
        if value is None and hasattr(BoxAuthType, value):
            raise ValueError("You must provide a valid auth_type")

        return value.value

    @root_validator()
    def validate_inputs(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        box = None

        """Validate that FILES mode provides box_file_ids."""
        if not values.get("box_ai_prompt") or not values.get("box_file_ids"):
            raise ValueError(f"You must provide box_ai_prompt and box_file_ids")

        """Validate that TOKEN auth type provides box_developer_token."""
        if values.get("auth_type") == "token" and not values.get("box_developer_token"):
            raise ValueError(
                f"{values.get('auth_type')} requires box_developer_token to be set"
            )

        """Validate that JWT auth type provides box_jwt_path."""
        if values.get("auth_type") == "jwt" and not values.get("box_jwt_path"):
            raise ValueError(
                f"{values.get('auth_type')} requires box_jwt_path to be set"
            )

        """Validate that CCG auth type provides box_client_id and box_client_secret and either 
        box_enterprise_id or box_user_id."""
        if values.get("auth_type") == "ccg":
            if (
                not values.get("box_client_id")
                or not values.get("box_client_secret")
                or (
                    not values.get("box_user_id")
                    and not values.get("box_enterprise_id")
                )
            ):
                raise ValueError(
                    f"{values.get('auth_type')} requires box_client_id, box_client_secret, and box_enterprise_id."
                )

        box = BoxAPIWrapper(
            auth_type=values.get("auth_type"),
            box_developer_token=values.get("box_developer_token"),
            box_client_id=values.get("box_client_id"),
            box_client_secret=values.get("box_client_secret"),
            box_enterprise_id=values.get("box_enterprise_id"),
            box_jwt_path=values.get("box_jwt_path"),
            box_user_id=values.get("box_user_id"),
            box_file_ids=values.get("box_file_ids"),
            box_ai_prompt=values.get("box_ai_prompt"),
        )

        values["box"] = box

        return values

    def lazy_load(self) -> Iterator[Document]:
        """Load documents."""
        match self.mode:
            case "ask":
                yield self.box.get_documents_by_box_ai_ask(
                    query=self.box_ai_prompt, file_ids=self.box_file_ids
                )
            case _:
                raise ValueError(f"{self.mode} currently only accepts `BoxAIMode.ASK`")
