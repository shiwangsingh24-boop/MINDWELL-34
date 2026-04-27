
import urllib.request
import urllib.error

try:
    url = "http://127.0.0.1:5000/resources"
    try:
        response = urllib.request.urlopen(url)
        print(f"Status Code: {response.getcode()}")
        content = response.read().decode('utf-8')
        print("Page content length:", len(content))
        if "Education" in content and "Exercises" in content:
             print("SUCCESS: Resources content found")
        else:
             print("WARNING: Expected content missing")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"Error accessing page: {e}")

except Exception as e:
    print(f"General Error: {e}")
