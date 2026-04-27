
import urllib.request
import urllib.error
import time

print("Waiting for server to start...")
time.sleep(3)

try:
    url = "http://127.0.0.1:5000/counsellors"
    try:
        response = urllib.request.urlopen(url)
        print(f"Status Code: {response.getcode()}")
        content = response.read().decode('utf-8')
        if "On-Campus" in content and "Off-Campus" in content:
             print("SUCCESS: Counsellors content verified")
        else:
             print("WARNING: Counsellor sections missing")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
    except Exception as e:
        print(f"Error accessing page: {e}")

except Exception as e:
    print(f"General Error: {e}")
