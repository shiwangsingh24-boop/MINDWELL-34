
import urllib.request
import urllib.error

try:
    url = "http://127.0.0.1:5000/refresh_scenario"
    # Create a request that doesn't automatically follow redirects
    class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(NoRedirectHandler)
    try:
        response = opener.open(url)
        # If we get here, it might be a 200 OK (if no redirect happened, which is unexpected)
        print(f"Status Code: {response.getcode()}")
    except urllib.error.HTTPError as e:
        if e.code == 302:
            print(f"Status Code: {e.code}")
            print(f"Location Header: {e.headers.get('Location')}")
            if '/dashboard' in e.headers.get('Location', ''):
                print("SUCCESS: Redirected to dashboard")
            else:
                print("FAILURE: Redirect target incorrect")
        else:
            print(f"HTTP Error: {e.code}")
    except Exception as e:
        print(f"Error: {e}")

except Exception as e:
    print(f"General Error: {e}")
