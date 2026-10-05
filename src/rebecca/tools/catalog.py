from src.rebecca.tools.web_open import (
    WebOpenTool,
)
from src.rebecca.tools.system_info import (
    SystemInfoTool,
)
from src.rebecca.tools.memory_info import (
    MemoryInfoTool,
)
from src.rebecca.tools.disk_info import (
    DiskInfoTool,
)
from src.rebecca.tools.cpu_info import (
    CPUInfoTool,
)
from src.rebecca.tools.process_info import (
    ProcessInfoTool,
)
from src.rebecca.tools.file_info import (
    FileInfoTool,
)
from src.rebecca.tools.file_read import (
    FileReadTool,
)
from src.rebecca.tools.file_write import (
    FileWriteTool,
)
from src.rebecca.tools.file_modify import (
    FileModifyTool,
)
from src.rebecca.tools.file_delete import (
    FileDeleteTool,
)
from src.rebecca.tools.web_search import (
    WebSearchTool,
)


TOOL_CATALOG = [
    {
        "tool": SystemInfoTool,
        "permission": "read",
    },
    {
        "tool": MemoryInfoTool,
        "permission": "read",
    },
    {
        "tool": DiskInfoTool,
        "permission": "read",
    },
    {
        "tool": CPUInfoTool,
        "permission": "read",
    },
    {
        "tool": ProcessInfoTool,
        "permission": "read",
    },
    {
        "tool": FileInfoTool,
        "permission": "read",
    },
    {
        "tool": FileReadTool,
        "permission": "read",
    },
    {
        "tool": FileWriteTool,
        "permission": "sensitive",
    },
    {
        "tool": FileModifyTool,
        "permission": "sensitive",
    },
    {
        "tool": FileDeleteTool,
        "permission": "sensitive",
    },
    {
        "tool": WebSearchTool,
        "permission": "read",
    },
    {
        "tool": WebOpenTool,
        "permission": "read",
    },
]

