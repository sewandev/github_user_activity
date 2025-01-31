import sys
import http.client
import json
import colors as c

def fetch_github_activity(username):
    connection = http.client.HTTPSConnection("api.github.com")
    url = f"/users/{username}/events"
    
    connection.request("GET", url, headers={"User-Agent": "github-activity-cli"})
    response = connection.getresponse()

    if response.status != 200:
        print(f"{c.RED}Error: No se pudo obtener datos (Código {response.status}){c.RESET}")
        return None

    data = response.read().decode()
    connection.close()
    
    return json.loads(data)  

def display_activity(events):
    if not events:
        print(f"{c.YELLOW}No hay actividad reciente.{c.RESET}")
        return

    print(f"{c.BLUE}Última actividad en GitHub:{c.RESET}\n")

    for event in events[:5]:  
        event_type = event["type"]
        repo_name = event["repo"]["name"]
        
        if event_type == "PushEvent":
            commits = len(event["payload"].get("commits", []))
            print(f"{c.GREEN}- Pushed {commits} commit(s) to {repo_name}{c.RESET}")
        
        elif event_type == "IssuesEvent":
            action = event["payload"]["action"]
            print(f"{c.YELLOW}- {action.capitalize()} an issue in {repo_name}{c.RESET}")
        
        elif event_type == "WatchEvent":
            print(f"{c.BLUE}- Starred {repo_name}{c.RESET}")
        
        else:
            print(f"{c.RED}- {event_type} in {repo_name}{c.RESET}")

def main():
    if len(sys.argv) < 2:
        print(f"{c.RED}Uso: github-activity <username>{c.RESET}")
        return

    username = sys.argv[1]
    print(f"{c.BLUE}Buscando actividad para el usuario: {username}{c.RESET}")

    events = fetch_github_activity(username)
    
    if events:
        display_activity(events)

if __name__ == "__main__":
    main()
