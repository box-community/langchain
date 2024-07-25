"""Util that calls Box APIs."""

from enum import Enum
import json
import requests
from typing import Any, Dict, Iterator, List, Optional

from langchain_core.documents import Document
from langchain_core.pydantic_v1 import BaseModel, root_validator, ConfigDict
from langchain_core.utils import get_from_dict_or_env

from langchain_box.utilities import BoxAuth

from box_sdk_gen import BoxClient


class BoxAPIWrapper(BaseModel):
    """Wrapper for Box API."""

    auth_type: str
    box_developer_token: Optional[str] = None
    box_client_id: Optional[str] = None
    box_client_secret: Optional[str] = None
    box_user_id: Optional[str] = None
    box_enterprise_id: Optional[str] = None
    box_jwt_path: Optional[str] = None
    box_file_id: Optional[str] = None
    box_file_ids: Optional[List[str]] = None
    box_folder_id: Optional[str] = None
    box_search_query: Optional[str] = None
    box_metadata_query: Optional[str] = None
    box_metadata_template: Optional[str] = None
    box_metadata_params: Optional[str] = None
    box_ai_prompt: Optional[str] = None
    box: Optional[BoxClient] = None

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        extra = "allow"

    @root_validator()
    def validate_inputs(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate auth_type is set"""
        if not values.get("auth_type"):
            raise ValueError(f"Auth type must be set.")

        """Validate that TOKEN auth type provides box_developer_token."""
        if values.get("auth_type") == "token" and not get_from_dict_or_env(
            values, "box_developer_token", "BOX_DEVELOPER_TOKEN"
        ):
            raise ValueError(
                f"{values.get('auth_type')} requires box_developer_token to be set"
            )

        """Validate that JWT auth type provides box_jwt_path."""
        if values.get("auth_type") == "jwt" and not get_from_dict_or_env(
            values, "box_jwt_path", "BOX_JWT_PATH"
        ):
            raise ValueError(
                f"{values.get('auth_type')} requires box_jwt_path to be set"
            )

        """Validate that CCG auth type provides box_client_id and box_client_secret and either 
        box_enterprise_id or box_user_id."""
        if values.get("auth_type") == "ccg":
            if (
                not get_from_dict_or_env(values, "box_client_id", "BOX_CLIENT_ID")
                or not get_from_dict_or_env(
                    values, "box_client_secret", "BOX_CLIENT_SECRET"
                )
                or (
                    not values.get("box_enterprise_id")
                    and not values.get("box_user_id")
                )
            ):
                raise ValueError(
                    f"{values.get('auth_type')} requires box_client_id, box_client_secret, and box_enterprise_id."
                )

        values["box"] = None

        DOCUMENT_EXTENSIONS = [
            "doc",
            "docx",
            "gdoc",
            "gsheet",
            "numbers",
            "ods",
            "odt",
            "pages",
            "pdf",
            "rtf",
            "wpd",
            "xls",
            "xlsm",
            "xlsx",
            "as",
            "as3",
            "asm",
            "bat",
            "c",
            "cc",
            "cmake",
            "cpp",
            "cs",
            "css",
            "csv",
            "cxx",
            "diff",
            "erb",
            "groovy",
            "h",
            "haml",
            "hh",
            "htm",
            "html",
            "java",
            "js",
            "json",
            "less",
            "log",
            "m",
            "make",
            "md",
            "ml",
            "mm",
            "msg",
            "php",
            "pl",
            "properties",
            "py",
            "rb",
            "rst",
            "sass",
            "scala",
            "scm",
            "script",
            "sh",
            "sml",
            "sql",
            "txt",
            "vi",
            "vim",
            "webdoc",
            "xhtml",
            "xlsb",
            "xml",
            "xsd",
            "xsl",
            "yaml",
            "gslide",
            "gslides",
            "key",
            "odp",
            "ppt",
            "pptx",
        ]
        values["DOCUMENT_EXTENSIONS"] = DOCUMENT_EXTENSIONS
        values["TOKEN_LIMIT"] = 10000

        return values

    def get_box_client(self):
        box_auth = BoxAuth(
            auth_type=self.auth_type,
            box_developer_token=self.box_developer_token,
            box_client_id=self.box_client_id,
            box_client_secret=self.box_client_secret,
            box_user_id=self.box_user_id,
            box_enterprise_id=self.box_enterprise_id,
            box_jwt_path=self.box_jwt_path,
        )

        self.box = box_auth.get_client()

    def _do_request(self, url: str) -> str:
        try:
            from box_sdk_gen import BoxSDKError
        except ImportError:
            raise ImportError("You must run `pip install box-sdk-gen`")

        try:
            access_token = self.box.auth.retrieve_token().access_token
        except BoxSDKError as bse:
            raise RuntimeError(f"Error getting client from jwt token: {bse.message}")

        resp = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
        resp.raise_for_status()
        return resp.content

    def get_folder_items(self, folder_id: str):
        try:
            from box_sdk_gen import BoxAPIError, BoxSDKError
        except ImportError:
            raise ImportError("You must run `pip install box-sdk-gen`")

        if self.box is None:
            self.get_box_client()

        try:
            folder_contents = self.box.folders.get_folder_items(
                folder_id, fields=["id", "type"]
            )
        except BoxAPIError as bae:
            raise RuntimeError(
                f"BoxAPIError: Error getting folder content: {bae.message}"
            )
        except BoxSDKError as bse:
            raise RuntimeError(
                f"BoxSDKError: Error getting folder content: {bse.message}"
            )

        return folder_contents.entries

    def get_text_representation(
        self, query: str = None, file_id: str = None
    ) -> tuple[str, str, str]:
        try:
            from box_sdk_gen import BoxSDKError, BoxAPIError
        except ImportError:
            raise ImportError("You must run `pip install box-sdk-gen`")

        if file_id is None:
            file_id = self.box_file_id

        if self.box is None:
            self.get_box_client()

        try:
            file = self.box.files.get_file_by_id(
                file_id,
                x_rep_hints="[extracted_text]",
                fields=["name", "representations", "type"],
            )
        except BoxAPIError as bae:
            raise RuntimeError(f"BoxAPIError: Error getting text rep: {bae.message}")
        except BoxSDKError as bse:
            raise RuntimeError(f"BoxSDKError: Error getting text rep: {bse.message}")
        except Exception as ex:
            print(f"Exception: Error getting text rep: {ex}")
            return None, None, None

        file_repr = file.representations.entries

        if len(file_repr) <= 0:
            print(f"No text representations for file {file_id}\n\n")
            return None, None, None

        for entry in file_repr:
            if entry.representation == "extracted_text":
                # If the file representation doesn't exist, calling info.url will generate text if possible
                if entry.status.state == "none":
                    self._do_request(entry.info.url)

                url = entry.content.url_template.replace("{+asset_path}", "")
                file_name = file.name.replace(".", "_").replace(" ", "_")

                raw_content = self._do_request(url)

                content = raw_content[0 : self.TOKEN_LIMIT]

                return file_name, content, url

    def get_document_by_file_id(self, file_id: str) -> Optional[Document]:
        """Load a file from a Box id."""

        file_name, content, url = self.get_text_representation(file_id=file_id)

        if file_name is None or content is None or url is None:
            print("No text representation available for file {file_id}. Skipping...")
            return None

        metadata = {
            "source": f"{url}",
            "title": f"{file_name}",
        }

        return Document(page_content=content, metadata=metadata)

    def get_documents_by_file_ids(
        self, box_file_ids: List[str] = None
    ) -> List[Document]:
        """Load documents from a list of Box file paths."""

        print(f"GDBFI self {self}")
        if box_file_ids is None:
            box_file_ids = self.box_file_ids

        if self.box is None:
            self.get_box_client()

        files = []

        for file_id in box_file_ids:
            file = self.get_document_by_file_id(file_id)

            if file is not None:
                files.append(file)

        return files

    def get_documents_by_folder_id(
        self, box_folder_id: str = None
    ) -> Iterator[Document]:
        if box_folder_id is None:
            box_folder_id = self.box_folder_id

        if self.box is None:
            self.get_box_client()

        """Load documents from a Box folder."""
        return self.get_folder_items(box_folder_id)

    def get_search_results(self, query: str = None) -> List[str]:
        try:
            from box_sdk_gen import BoxAPIError, BoxSDKError
        except ImportError:
            raise ImportError("You must run `pip install box-sdk-gen`")

        if query is None:
            query = self.box_search_query

        if self.box is None:
            self.get_box_client()

        files = []
        try:
            results = self.box.search.search_for_content(
                query=query, fields=["id", "type", "extension"]
            )
            print(f"GSR: results.entries {results.entries}")
            for file in results.entries:
                print(f"GSR: file {file}")
                if (
                    file is not None
                    and file.type == "file"
                    and file.extension in self.DOCUMENT_EXTENSIONS
                ):
                    files.append(file.id)

            return files
        except BoxAPIError as bae:
            raise RuntimeError(
                f"BoxAPIError: Error getting search results: {bae.message}"
            )
        except BoxSDKError as bse:
            raise RuntimeError(
                f"BoxSDKError: Error getting search results: {bse.message}"
            )

    def get_documents_by_search(self, query: str = None) -> List[Document]:
        if query is None:
            query = self.box_search_query

        if self.box is None:
            self.get_box_client()

        print(f"GDBS: query {query} token {self.box_developer_token}")
        files = self.get_search_results(query)

        if files is None or len(files) <= 0:
            return "no files found"

        print(f"GDBS: files {files}")

        return self.get_documents_by_file_ids(files)

    def get_metadata_query_results(
        self,
        query: str = None,
        template: str = None,
        param_string: str = None,
        eid: str = None,
    ) -> List[str]:
        try:
            from box_sdk_gen import BoxAPIError, BoxSDKError
        except ImportError:
            raise ImportError("You must run `pip install box-sdk-gen`")

        if query is None:
            query = self.box_metadata_query

        if template is None:
            template = self.box_metadata_template

        if param_string is None:
            param_string = self.box_metadata_params

        if eid is None:
            eid = self.box_enterprise_id

        if self.box is None:
            self.get_box_client()

        files = []
        params = json.loads(param_string)

        try:
            results = self.box.search.search_by_metadata_query(
                f"enterprise_{eid}.{template}",
                ancestor_folder_id="0",
                query=query,
                query_params=params,
            )
        except BoxAPIError as bae:
            raise RuntimeError(
                f"BoxAPIError: Error getting Metadata query results: {bae.message}"
            )
        except BoxSDKError as bse:
            raise RuntimeError(
                f"BoxSDKError: Error getting Metadata query results: {bse.message}"
            )

        for file in results.entries:
            if file is not None:
                files.append(file.id)

        return files

    def get_documents_by_metadata_query(
        self,
        query: str = None,
        template: str = None,
        param_string: str = None,
        eid: str = None,
    ) -> List[Document]:
        if query is None:
            query = self.box_metadata_query

        if template is None:
            template = self.box_metadata_template

        if param_string is None:
            param_string = self.box_metadata_params

        if eid is None:
            eid = self.box_enterprise_id

        files = self.get_metadata_query_results(query, template, param_string, eid)

        if len(files) <= 0:
            return "no files found"

        return self.get_documents_by_file_ids(files)

    def get_documents_by_box_ai_ask(
        self,
        query: str = None,
        file_ids: List[str] = None,
        return_response: bool = False,
    ) -> Document:
        if query is None:
            query = self.box_ai_prompt

        if file_ids is None:
            file_ids = self.box_file_ids

        if self.box is None:
            self.get_box_client()

        try:
            from box_sdk_gen import (
                CreateAiAskMode,
                CreateAiAskItems,
                CreateAiAskItemsTypeField,
                BoxAPIError,
                BoxSDKError,
            )
        except ImportError:
            raise ImportError("You must run `pip install box-sdk-gen`")

        ai_mode = CreateAiAskMode.SINGLE_ITEM_QA.value

        if len(file_ids) > 1:
            ai_mode = CreateAiAskMode.MULTIPLE_ITEM_QA.value
        elif len(file_ids) <= 0:
            raise ValueError("BOX_AI_ASK requires at least one file ID")

        items = []

        for file_id in file_ids:
            item = CreateAiAskItems(
                id=file_id, type=CreateAiAskItemsTypeField.FILE.value
            )
            items.append(item)

        try:
            response = self.box.ai.create_ai_ask(ai_mode, query, items)
        except BoxAPIError as bae:
            raise RuntimeError(
                f"BoxAPIError: Error getting Box AI result: {bae.message}"
            )
        except BoxSDKError as bse:
            raise RuntimeError(
                f"BoxSDKError: Error getting Box AI result: {bse.message}"
            )

        content = response.answer

        if return_response:
            return content

        metadata = {"source": f"Box AI", "title": f"Box AI {query}"}

        return Document(page_content=content, metadata=metadata)

    def run(self, mode: str, query: str) -> str:
        match mode:
            case "search":
                return self.search(query)
            case "metadata_query":
                return self.metadata_query(query)
            case "box_ai_ask":
                return self.box_ai_ask_response(query)
            case _:
                raise ValueError(f"Got unexpected mode {mode}")
