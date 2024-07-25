from __future__ import annotations

import logging
from typing import Dict, Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env

from langchain_box.utilities import BoxAPIWrapper

logger = logging.getLogger(__name__)


class BoxTextRepInput(BaseModel):
    """Input for the Box Text Rep tool."""

    description: str = (
        "input to retrieve the text representation of a file in Box. The input should be a string "
        "and should contain the Box file id. An example of this is '1169680553945'. Do not include "
        "any other text."
    )

    query: str = Field(description=description)


class BoxTextRepTool(BaseTool):
    """
    Tool that retrieves a text representation of any file that has one.
    """

    box_developer_token: str = ""  #: :meta private:

    name: str = "box_text_rep"
    description: str = (
        "A wrapper for Box to retrieve the text representation of a file. "
        "set query equal to a string equal to the file Id you wish to "
        "download the text representation for."
    )

    args_schema: Type[BaseModel] = BoxTextRepInput

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and endpoint exists in environment."""
        box_developer_token = get_from_dict_or_env(
            values, "box_developer_token", "BOX_DEVELOPER_TOKEN"
        )

        box = BoxAPIWrapper(
            auth_type="token",
            box_developer_token=box_developer_token,
        )

        values["box"] = box

        return values

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        try:
            return self.box.get_text_representation(file_id=query)
        except Exception as e:
            raise RuntimeError(f"Error while running BoxTextRepTool: {e}")
