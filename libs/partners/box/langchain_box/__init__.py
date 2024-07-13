from importlib import metadata

from langchain_box.agent_toolkits import BoxToolkit
from langchain_box.document_loaders import (
    BoxAILoader,
    BoxFileLoader,
    BoxFolderLoader,
    BoxMetadataQueryLoader,
    BoxSearchLoader
)
from langchain_box.tools import (
    BoxAIAskTool,
    BoxFileSearchTool,
    BoxFolderContentsTool,
    BoxTextRepTool
)
from langchain_box.utilities import (
    BoxAuth,
    BoxAuthType,
    BoxAPIWrapper
)

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "BoxToolkit",
    "BoxAILoader",
    "BoxFileLoader",
    "BoxFolderLoader",
    "BoxMetadataQueryLoader",
    "BoxSearchLoader",
    "BoxAIAskTool",
    "BoxFileSearchTool",
    "BoxFolderContentsTool",
    "BoxTextRepTool",
    "BoxAuth",
    "BoxAuthType",
    "BoxAPIWrapper",
    "__version__",
]
