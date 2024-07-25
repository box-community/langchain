from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.documents.base import Document
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env

from langchain_box.utilities import BoxAPIWrapper

logger = logging.getLogger(__name__)


class BoxFolderContentInput(BaseModel):
    """Input for the BoxFolderContent tool."""

    description: str = (
        "folder id to retrieve the contents of a folder in Box. The input should be a string "
        "and should contain the Box folder id. An example of this is '1169680553945'. Do not include "
        "any other text."
    )

    query: str = Field(description="Query to search a folder for content")


class BoxFolderContentsTool(BaseTool):
    """List all files in a folder in Box"""

    box_developer_token: str = ""  #: :meta private:

    name: str = "box_folder_contents"
    description: str = (
        "A wrapper for listing all the files in a Box folder. "
        "This tool will return a Iterator[str,str] containing file names and ids. "
        "Query should be set to a string containing the folder id. "
        "These file ids can be used with other tools."
    )

    args_schema: Type[BaseModel] = BoxFolderContentInput

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and endpoint exists in environment."""
        box_developer_token = get_from_dict_or_env(
            values, "box_developer_token", "BOX_DEVELOPER_TOKEN"
        )

        box = BoxAPIWrapper(auth_type="token", box_developer_token=box_developer_token)

        values["box"] = box

        return values

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> List[Document]:
        """Use the tool."""
        try:
            folder_content = self.box.get_folder_items(folder_id=query)
            files = []
            for file in folder_content:
                if file.type == "file":
                    files.append(self.box.get_document_by_file_id(file.id))

            return files
        except Exception as e:
            raise RuntimeError(f"Error while running BoxFolderContentsTool: {e}")
