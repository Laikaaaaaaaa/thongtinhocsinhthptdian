import urllib.request
import json

def test_api():
    try:
        url = "http://localhost:5000/api/generate-sample-data"
        data = {"count": 2}
        
        # Tạo request
        req_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=req_data)
        req.add_header('Content-Type', 'application/json')
        
        print("📡 Sending request...")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        
        print("✅ Response:", result)
        
    except Exception as e:
        print("❌ Error:", str(e))

if __name__ == "__main__":
    test_api()
