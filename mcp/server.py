from fastmcp import FastMCP

mcp = FastMCP(name="KnowlegeManagerMCPServer")

@mcp.tool()
def casual_tool():
    return 1


if __name__=="__main__":
    mcp.run(transport="http",host="127.0.0.1",port=7322)