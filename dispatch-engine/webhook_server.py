import http.server
import json
import urllib.request
import os
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PORT = 8000

class LeadHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/lead':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                lead = json.loads(body)
            except Exception:
                lead = {}

            print("\n" + "="*55)
            print("[NEW LEAD INTAKE - RECEIVED FROM UK HOMEOWNER]")
            print(f"Customer Name: {lead.get('name')}")
            print(f"Phone: {lead.get('phone')}")
            print(f"Postcode: {lead.get('postcode')}")
            print(f"Service: {lead.get('service')}")
            print(f"Notes: {lead.get('notes')}")

            # AI 自动清洗与中转派单卡片 (生成发往微信/Telegram的纯中文结构化抢单通知)
            chinese_dispatch_card = {
                "title": f"【英国本地装修新单 - {lead.get('postcode', 'RG1')}】",
                "customer_name": lead.get('name', 'UK Client'),
                "contact_phone": lead.get('phone', '07xxx'),
                "postcode_area": lead.get('postcode', 'RG1'),
                "project_type": lead.get('service', '卫浴瓷砖翻新'),
                "notes_translated": f"客户备注需求: {lead.get('notes', '无特别说明')}",
                "ai_suggested_labour_price": "£550 - £750 (建议工期 2-3 天)",
                "action_url": f"https://dispatch.primetilers.uk/accept?lead_id=LEAD_98231"
            }

            print("\n[AI 自动派发至华人师傅端 (微信/Telegram 卡片)]")
            print(f"> {chinese_dispatch_card['title']}")
            print(f"> 客户: {chinese_dispatch_card['customer_name']} (电话: {chinese_dispatch_card['contact_phone']})")
            print(f"> 区域: {chinese_dispatch_card['postcode_area']}")
            print(f"> 施工项目: {chinese_dispatch_card['project_type']}")
            print(f"> 需求详情: {chinese_dispatch_card['notes_translated']}")
            print(f"> AI参考报价: {chinese_dispatch_card['ai_suggested_labour_price']}")
            print(f"> 点击抢单: {chinese_dispatch_card['action_url']}")
            print("="*55 + "\n")

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "dispatch_id": "DISP_98231"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    print(f"AI Lead Dispatch Server running at http://127.0.0.1:{PORT}")
    server = http.server.HTTPServer(('127.0.0.1', PORT), LeadHandler)
    server.serve_forever()
