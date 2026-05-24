#!/usr/bin/env python3
"""恋爱网站同步服务器 - 电脑运行后手机自动同步"""
import http.server, json, os, sys
from urllib.parse import urlparse

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloud_data.json')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        p = urlparse(self.path)
        if p.path == '/api/sync':
            d = load_data()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(d or {'ver':0,'data':''}).encode())
            return
        if p.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'OK')
            return
        return super().do_GET()

    def do_POST(self):
        p = urlparse(self.path)
        if p.path == '/api/sync':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                save_data(data)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True}).encode())
            except:
                self.send_response(400); self.end_headers()
            return
        return super().do_POST()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        if '/api/' in str(args[0]): print(f'  [Sync] {args[0]}')
        else: pass  # Suppress static file logs

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(f'[LoveSync] Server started on port {port}')
    print(f'   PC:   http://localhost:{port}')
    print(f'   Phone: http://YOUR_IP:{port}')
    print(f'   API:  http://YOUR_IP:{port}/api/sync')
    print(f'   Press Ctrl+C to stop\n')
    http.server.HTTPServer(('0.0.0.0', port), Handler).serve_forever()
