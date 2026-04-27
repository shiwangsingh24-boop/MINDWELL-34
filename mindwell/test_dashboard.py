
import urllib.request
import urllib.error

try:
    url = "http://127.0.0.1:5000/dashboard"
    try:
        response = urllib.request.urlopen(url)
        print(f"Status Code: {response.getcode()}")
        content = response.read().decode('utf-8')
        print("Page content length:", len(content))
        if "Hello, Alex" in content or "Daily Scenario" in content:
             print("SUCCESS: Dashboard content found")
        else:
             print("WARNING: Dashboard content might be missing")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"Error accessing page: {e}")

except Exception as e:
    print(f"General Error: {e}")
