from crewai_tools import DirectorySearchTool, DirectoryReadTool, FileReadTool, FileWriterTool

file_read_tool = FileReadTool()
directory_read_tool = DirectoryReadTool()
# directory_search_tool = DirectorySearchTool()
file_writer = FileWriterTool()