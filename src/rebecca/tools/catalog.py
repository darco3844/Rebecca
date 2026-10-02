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
        "permission": "safe",
    },
]
