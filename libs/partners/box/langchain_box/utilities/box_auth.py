from enum import Enum
from typing import Any, Dict, List, Optional

from box_sdk_gen import (
    BoxClient,
    BoxSDKError,
    BoxDeveloperTokenAuth,
    BoxJWTAuth,
    JWTConfig,
    BoxCCGAuth,
    CCGConfig,
)

"""
    AuthType - an enum to tell BoxLoader how you wish to autheticate your Box connection.

    Options are:
    TOKEN - Use a developer token generated from the Box Deevloper Token. Only recommended for development.
            provide `box_developer_token`.
    CCG - Client Credentials Grant.
          provide `box_client_id`, `box_client_secret`, `box_enterprise_id` and optionally `box_user_id`.
    JWT - Use JWT for authentication. Config should be stored on the file system accessible to your app.
          provide `box_jwt_path`. 
"""


class BoxAuthType(Enum):
    TOKEN = "token"
    CCG = "ccg"
    JWT = "jwt"


class BoxAuth:
    def __init__(
        self,
        auth_type: str,
        box_developer_token: Optional[str] = None,
        box_client_id: Optional[str] = None,
        box_client_secret: Optional[str] = None,
        box_user_id: Optional[str] = None,
        box_enterprise_id: Optional[str] = None,
        box_jwt_path: Optional[str] = None,
    ):
        self.auth_type = auth_type
        self.box_developer_token = box_developer_token
        self.box_client_id = box_client_id
        self.box_client_secret = box_client_secret
        self.box_user_id = box_user_id
        self.box_enterprise_id = box_enterprise_id
        self.box_jwt_path = box_jwt_path
        self.box_client = None
        self.custom_header: Dict = dict({"x-box-ai-library": "langchain"})

    def authorize(self):
        """Create a Box client."""
        match self.auth_type:
            case "token":
                try:
                    auth = BoxDeveloperTokenAuth(token=self.box_developer_token)
                    self.box_client = BoxClient(auth=auth).with_extra_headers(
                        extra_headers=self.custom_header
                    )

                except BoxSDKError as bse:
                    raise RuntimeError(
                        f"Error getting client from developer token: {bse.message}"
                    )
                except Exception as ex:
                    raise ValueError(
                        f"Invalid Box developer token. Please verify your token and try again.\n{ex}"
                    ) from ex

            case "jwt":
                try:
                    jwt_config = JWTConfig.from_config_file(
                        config_file_path=self.box_jwt_path
                    )
                    auth = BoxJWTAuth(config=jwt_config)

                    self.box_client = BoxClient(auth=auth).with_extra_headers(
                        extra_headers=self.custom_header
                    )

                    if self.box_user_id is not None:
                        user_auth = auth.with_user_subject(self.box_user_id)
                        self.box_client = BoxClient(auth=user_auth).with_extra_headers(
                            extra_headers=self.custom_header
                        )

                except BoxSDKError as bse:
                    raise RuntimeError(
                        f"Error getting client from jwt token: {bse.message}"
                    )
                except Exception as ex:
                    raise ValueError(
                        "Error authenticating. Please verify your JWT config and try again."
                    ) from ex

            case "ccg":
                try:
                    if self.box_user_id is not None:
                        ccg_config = CCGConfig(
                            client_id=self.box_client_id,
                            client_secret=self.box_client_secret,
                            user_id=self.box_user_id,
                        )
                    else:
                        ccg_config = CCGConfig(
                            client_id=self.box_client_id,
                            client_secret=self.box_client_secret,
                            enterprise_id=self.box_enterprise_id,
                        )
                    auth = BoxCCGAuth(config=ccg_config)

                    self.box_client = BoxClient(auth=auth).with_extra_headers(
                        extra_headers=self.custom_header
                    )

                except BoxSDKError as bse:
                    raise RuntimeError(
                        f"Error getting client from ccg token: {bse.message}"
                    )
                except Exception as ex:
                    raise ValueError(
                        "Error authenticating. Please verify you are providing a valid client id, secret \
                            and either a valid user ID or enterprise ID."
                    ) from ex

            case _:
                raise ValueError(f"{self.auth_type} is not a valid auth_type. Value must be \
                TOKEN, CCG, or JWT.")

    def get_client(self):
        if self.box_client is None:
            self.authorize()

        return self.box_client
