#!/usr/bin/env python3
"""
KillCloud — Replace $20/mo Cloud AI Subscriptions with 100% Offline Local AI (MIT)
Zero external Python dependencies (stdlib only). Powered by MYCA-Modchip (0 GPU).
"""
import argparse
import http.server
import json
import os
import shutil
import socketserver
import subprocess

PORT = 8989


def run_myca(prompt, max_tokens=72):
    home = os.path.expanduser("~")
    myca = shutil.which("myca-modchip") or os.path.join(home, ".local/bin/myca-modchip")
    model = os.path.join(home, ".myca/models/smollm2-135m-ghr.myca")
    if os.path.isfile(myca) and os.path.isfile(model):
        out = subprocess.check_output(
            [myca, "run", model, "-p", prompt, "-n", str(max_tokens)],
            stderr=subprocess.STDOUT,
            timeout=45,
        ).decode(errors="ignore")
        return {"ok": True, "output": out, "bytes_sent_to_cloud": 0, "cost_usd": 0.0}
    return {
        "ok": False,
        "output": "Install MYCA-Modchip first:\n  curl -fsSL https://raw.githubusercontent.com/brienteth/myca-ghr-modchip/main/install.sh | sh\n  myca-modchip pull smollm2-135m",
        "bytes_sent_to_cloud": 0,
        "cost_usd": 0.0,
    }


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>KillCloud — $0/mo 100% Offline AI Suite</title>
<style>
  body{margin:0;background:#0B0C10;color:#EAE6DF;font-family:system-ui,-apple-system,sans-serif}
  .wrap{max-width:960px;margin:0 auto;padding:28px 20px}
  .top{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #222633;padding-bottom:16px;margin-bottom:20px}
  .badge{background:#5AE39B22;color:#5AE39B;border:1px solid #5AE39B55;padding:5px 12px;border-radius:99px;font-size:12px;font-weight:700}
  .tabs{display:flex;gap:10px;margin-bottom:16px}
  .tab{background:#141720;color:#8D96AA;border:1px solid #252A38;padding:10px 16px;border-radius:10px;cursor:pointer;font-weight:600}
  .tab.active{background:#C8A86B;color:#0B0C10;border-color:#C8A86B}
  .card{background:#141720;border:1px solid #252A38;border-radius:14px;padding:20px}
  textarea{width:100%;box-sizing:border-box;background:#0E1016;border:1px solid #282E3E;color:#EAE6DF;padding:12px;border-radius:10px;font-size:14px;min-height:110px;font-family:inherit}
  .btn{background:#C8A86B;color:#0B0C10;border:0;padding:11px 20px;border-radius:10px;font-weight:700;cursor:pointer;margin-top:10px}
  pre{background:#0E1016;border:1px solid #252A38;border-radius:10px;padding:14px;white-space:pre-wrap;font-size:14px;color:#5AE39B;min-height:90px;margin-top:14px}
  .stats{display:flex;gap:16px;margin-top:14px;color:#8D96AA;font-size:13px}
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div><h2 style="margin:0">KillCloud</h2><div style="color:#8D96AA;font-size:13px">Cancel $20/mo Cloud AI Subscriptions · 100% Local CPU Inference</div></div>
    <span class="badge">$0/mo · 0 Bytes Sent to Cloud · 0 GPU</span>
  </div>
  <div class="tabs">
    <button class="tab active" onclick="setMode('chat',this)">Private Chat</button>
    <button class="tab" onclick="setMode('summarize',this)">Note / Doc Summarizer</button>
    <button class="tab" onclick="setMode('code',this)">Offline Code Helper</button>
  </div>
  <div class="card">
    <div id="hint" style="color:#8D96AA;font-size:13px;margin-bottom:8px">Ask anything offline — runs locally via MYCA-Modchip:</div>
    <textarea id="inp">Explain why running local AI on CPU matters for privacy in two sentences.</textarea>
    <button class="btn" onclick="runTask()">Run Locally (0 GPU)</button>
    <pre id="out">Ready.</pre>
    <div class="stats">
      <span>Cloud Bytes Sent: <b style="color:#5AE39B">0 B</b></span>
      <span>Monthly Cost: <b style="color:#C8A86B">$0.00</b></span>
      <span>Tasks Run Offline: <b id="cnt" style="color:#EAE6DF">0</b></span>
    </div>
  </div>
</div>
<script>
let mode='chat', count=0;
function setMode(m,el){
  mode=m;document.querySelectorAll('.tab').forEach(b=>b.classList.remove('active'));el.classList.add('active');
  const h=document.getElementById('hint'), inp=document.getElementById('inp');
  if(m==='summarize'){h.textContent='Paste notes, emails, or logs to summarize locally:';inp.value='Summarize: Meeting at 3pm to ship v1.3.0 SIMD engine, cut cloud costs, and publish MIT runtime.';}
  else if(m==='code'){h.textContent='Paste code or ask for a snippet offline:';inp.value='Explain what a mutex and condition variable do in C pthreads in two sentences.';}
  else{h.textContent='Ask anything offline — runs locally via MYCA-Modchip:';inp.value='Explain why running local AI on CPU matters for privacy in two sentences.';}
}
async function runTask(){
  const out=document.getElementById('out');out.textContent='Running locally on CPU (0 GPU)...';
  const r=await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mode,text:document.getElementById('inp').value})});
  const d=await r.json();out.textContent=d.output;
  count++;document.getElementById('cnt').textContent=String(count);
}
</script>
</body></html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _send(self, code, ctype, body):
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/":
            self._send(200, "text/html; charset=utf-8", HTML_PAGE)
        else:
            self._send(404, "application/json", '{"error":"not found"}')

    def do_POST(self):
        if self.path == "/api/run":
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n).decode() or "{}")
            mode = payload.get("mode", "chat")
            text = payload.get("text", "")
            prefix = {
                "summarize": "Summarize concisely in bullet points:\n",
                "code": "Answer concisely as a senior C/systems engineer:\n",
            }.get(mode, "")
            res = run_myca(prefix + text)
            self._send(200, "application/json", json.dumps(res))
        else:
            self._send(404, "application/json", '{"error":"not found"}')


def main():
    ap = argparse.ArgumentParser(description="KillCloud Offline AI Suite")
    ap.add_argument("--port", type=int, default=PORT)
    args = ap.parse_args()
    with socketserver.TCPServer(("127.0.0.1", args.port), Handler) as httpd:
        print(f"KillCloud running at http://127.0.0.1:{args.port}/")
        httpd.serve_forever()


if __name__ == "__main__":
    main()

