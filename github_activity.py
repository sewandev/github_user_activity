import sys
import http.client
import json
import colors as c

def fetch_github_activity(username):
    connection = None
    try:
        connection = http.client.HTTPSConnection("api.github.com")
        connection.request("GET", f"/users/{username}/events", headers={"User-Agent": "github-activity-cli"})
        response = connection.getresponse()
        status = response.status

        if status == 404:
            print(f"{c.RED}Error: El usuario '{username}' no existe en GitHub.{c.RESET}")
        elif status != 200:
            print(f"{c.RED}Error: No se pudo obtener datos (Código {status}){c.RESET}")
        else:
            return json.loads(response.read().decode())

    except http.client.HTTPException as e:
        print(f"{c.RED}Error de conexión: {e}{c.RESET}")
    except json.JSONDecodeError:
        print(f"{c.RED}Error: No se pudo decodificar la respuesta de GitHub.{c.RESET}")
    finally:
        if connection:
            connection.close()

    return None

def display_activity(events):
    if not isinstance(events, list) or not events:
        print(f"{c.YELLOW}No hay actividad reciente o la respuesta no es válida.{c.RESET}")
        return

    print(f"{c.BLUE}Última actividad en GitHub:{c.RESET}\n")

    for i, event in enumerate(events[:5]):  
        event_type = event.get("type", "Evento desconocido")
        repo_name = event.get("repo", {}).get("name", "Repositorio desconocido")

        if event_type == "PushEvent":
            commits = event.get("payload", {}).get("commits", [])
            print(f"{c.GREEN}- Pushed {len(commits)} commit(s) to {repo_name}{c.RESET}")

            for commit in commits:
                print(f"    {c.CYAN}- {commit.get('message', 'Sin mensaje')}{c.RESET}")
        
        elif event_type == "IssuesEvent":
            print(f"{c.YELLOW}- {event.get('payload', {}).get('action', 'Realizó una acción')} en {repo_name}{c.RESET}")
        
        elif event_type == "WatchEvent":
            print(f"{c.BLUE}- Starred {repo_name}{c.RESET}")
        
        else:
            print(f"{c.RED}- {event_type} en {repo_name}{c.RESET}")

    if len(events) > 5 and input(f"{c.YELLOW}¿Quieres ver más eventos? (s/n): {c.RESET}").strip().lower() == "s":
        for event in events[5:10]:  
            print(f"{c.CYAN}- {event.get('type', 'Evento desconocido')} en {event.get('repo', {}).get('name', 'Repositorio desconocido')}{c.RESET}")

def main():
    if len(sys.argv) < 2:
        print(f"{c.RED}Uso: github-activity <username>{c.RESET}")
        return

    username = sys.argv[1].strip()
    if not username:
        print(f"{c.RED}Error: Debes proporcionar un nombre de usuario válido.{c.RESET}")
        return

    print(f"{c.BLUE}Buscando actividad para el usuario: {username}{c.RESET}")

    if (events := fetch_github_activity(username)) is not None:
        display_activity(events)

if __name__ == "__main__":
    main()
