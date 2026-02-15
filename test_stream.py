import urllib.request
import json
import sys
import traceback

API_URL = "http://localhost:8000/api/chat/stream"

def test_stream():
    payload = {
        "message": "Apa keunggulan SMK Pertiwi?",
        "history": [],
        "session_id": "test_stream_session_v2"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(API_URL, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    print(f"Connecting to {API_URL}...")
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Connected. Status: {response.status}")
            
            while True:
                line = response.readline()
                if not line:
                    break
                
                decoded_line = line.decode('utf-8').strip()
                if not decoded_line:
                    continue

                try:
                    data = json.loads(decoded_line)
                    if data['type'] == 'chunk':
                        sys.stdout.write(data['content'])
                        sys.stdout.flush()
                    elif data['type'] == 'source':
                            print(f"\n\n[Source: {data.get('label')}]")
                    elif data['type'] == 'meta':
                            print(f"\n[Meta: Session ID {data.get('session_id')}]")
                    elif data['type'] == 'error':
                            print(f"\n[Error: {data.get('content')}]")
                except json.JSONDecodeError:
                    print(f"\n[Raw]: {decoded_line}")
                    
    except Exception as e:
        print(f"\nException: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_stream()
