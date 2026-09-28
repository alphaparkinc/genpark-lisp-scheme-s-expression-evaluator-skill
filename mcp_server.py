import sys
import json
from client import LispEvaluator

evaluator = LispEvaluator()

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-lisp-scheme-s-expression-evaluator-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "eval_lisp",
                    "description": "Parse and evaluate Lisp/Scheme S-expression string",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string"}
                        },
                        "required": ["code"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "eval_lisp":
            code = args.get("code", "")
            tokens = evaluator.tokenize(code)
            ast = evaluator.parse(tokens)
            val = evaluator.eval(ast)
            res = {"content": [{"type": "text", "text": json.dumps({"result": val, "parsed_ast": ast})}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
