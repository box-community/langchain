from __future__ import annotations

import logging
from typing import Dict, Optional, List, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env

from langchain_box.utilities import BoxAPIWrapper

logger = logging.getLogger(__name__)


class BoxAIAskInput(BaseModel):
    """The query argument to send to the Box AI Ask tool."""

    query: str = Field(description="Box AI prompt")


class BoxAIAskTool(BaseTool):
    """
    Tool that calls Box AI to ask a question on a document(s) and adds the answer to your Documents.
    """

    box_developer_token: str = ""  #: :meta private:
    box_file_ids: List[str] = None

    name: str = "box_ai_ask_tool"
    description: str = (
        "A wrapper for asking Box AI a question about one or more documents. "
        "The input must be an object as follows: "
        "_run('query'='a valid string.')"
        "The response is a langchain_core.documents.base.Document."
    )

    args_schema: Type[BaseModel] = BoxAIAskInput

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and endpoint exists in environment."""
        box_developer_token = get_from_dict_or_env(
            values, "box_developer_token", "BOX_DEVELOPER_TOKEN"
        )

        if not values.get("box_file_ids"):
            raise ValueError("Box AI requires List[str] with file_ids.")

        box = BoxAPIWrapper(
            auth_type="token",
            box_developer_token=box_developer_token,
            box_file_ids=values.get("box_file_ids"),
        )

        values["box"] = box

        return values

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        print(f"query")
        try:
            return self.box.get_documents_by_box_ai_ask(query)
        except Exception as e:
            raise RuntimeError(f"Error while running BoxAIAskTool: {e}")
