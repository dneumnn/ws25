import requests

r = requests.get("http://localhost:8000")
for key in r.headers:
    print(key, r.headers[key])

match r.headers["Content-Type"]:
    case "text/plain":    
        print(f"\n{r.content}")
    case "application/json":
        print(f"\n{r.json()}")
