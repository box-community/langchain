from typing import Any, Dict, Iterator, List, Optional
from enum import Enum

from langchain_core.document_loaders.base import BaseLoader
from langchain_box.utilities import BoxAPIWrapper, BoxAuthType
from langchain_core.documents import Document
from langchain_core.pydantic_v1 import BaseModel, root_validator, ConfigDict, validator
from langchain_core.utils import get_from_dict_or_env


class BoxMetadataQueryLoader(BaseLoader, BaseModel):
    """
    BoxMetadataQueryLoader

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
    mode | how to retrieve documents | enum | yes
    auth_type | authentication type to use | enum | yes
    box_developer_token | token to use for auth. Should only use for development | string | no
    box_client_id | client id for you app. Used for CCG | string | no
    box_client_secret | client secret for you app. Used for CCG | string | no
    box_user_id | User ID or Enterprise ID to make calls for. Used for CCG or JWT | string | no
    box_enterprise_id | Enterprise ID to make calls for. Used for CCG. | string | no
    box_jwt_path | Local file system path the the jwt config JSON | string | no
    box_metadata_query | metadata query to search for files to retrieve | string | no
    box_metadata_template | metadata template to search for files to retrieve | string | no
    box_metadata_params | params to complete the metadata query to search for files to retrieve | string | no
    """

    model_config = ConfigDict(use_enum_values=True)

    auth_type: BoxAuthType
    box_developer_token: Optional[str] = None
    box_client_id: Optional[str] = None
    box_client_secret: Optional[str] = None
    box_user_id: Optional[str] = None
    box_enterprise_id: Optional[str] = None
    box_jwt_path: Optional[str] = None
    box_metadata_query: Optional[str] = None
    box_metadata_template: Optional[str] = None
    box_metadata_params: Optional[str] = None

    @validator("auth_type")
    def validate_auth_type(cls, value):
        if value is None and hasattr(BoxAuthType, value):
            raise ValueError("You must provide a valid auth_type")

        return value.value

    @root_validator()
    def validate_inputs(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        box = None

        """Validate that METADATA_QUERY mode provides metadata_query."""
        if (
            not values.get("box_metadata_query")
            and not values.get("box_metadata_template")
            and not values.get("box_metadata_params")
            and not values.get("box_enterprise_id")
        ):
            raise ValueError(
                f"{values.get('mode')} requires box_metadata_query, box_metadata_template, box_metadata_params, and boc_enterprise_id to be set"
            )

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
            box_metadata_query=values.get("box_metadata_query"),
            box_metadata_template=values.get("box_metadata_template"),
            box_metadata_params=values.get("box_metadata_params"),
        )

        values["box"] = box

        return values

    def lazy_load(self) -> Iterator[Document]:
        files = self.box.get_metadata_query_results(
            query=self.box_metadata_query,
            template=self.box_metadata_template,
            param_string=self.box_metadata_params,
            eid=self.box_enterprise_id,
        )

        for file_id in files:
            yield self.box.get_document_by_file_id(file_id)
