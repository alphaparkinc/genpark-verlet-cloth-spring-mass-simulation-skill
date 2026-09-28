import sys
import json
from client import VerletClothSimulation

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-verlet-cloth-spring-mass-simulation-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "simulate_cloth_step",
                        "description": "Run Verlet integration step on cloth spring-mass grid",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "cols": {"type": "integer", "default": 4},
                                "rows": {"type": "integer", "default": 4},
                                "spacing": {"type": "number", "default": 1.0},
                                "dt": {"type": "number", "default": 0.02},
                                "gravity": {"type": "number", "default": 9.8}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "simulate_cloth_step":
            cols = args.get("cols", 4)
            rows = args.get("rows", 4)
            spacing = args.get("spacing", 1.0)
            cloth = VerletClothSimulation(cols=cols, rows=rows, spacing=spacing)
            cloth.step(dt=args.get("dt", 0.02), gravity=args.get("gravity", 9.8), iterations=5)
            pts = [{"x": p.x, "y": p.y, "pinned": p.pinned} for p in cloth.particles]
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"num_particles": len(pts), "particles": pts[:10]})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
