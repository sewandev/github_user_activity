import sys
import http.client
import json
import colors as c

def fetch_github_activity(username):
    try:
        connection = http.client.HTTPSConnection("api.github.com")
        url = f"/users/{username}/events"
        
        connection.request("GET", url, headers={"User-Agent": "github-activity-cli"})
        response = connection.getresponse()

        if response.status == 404:
                print(f"{c.RED}Error: El usuario '{username}' no existe en GitHub.{c.RESET}")
                return None

        if response.status != 200:
                print(f"{c.RED}Error: No se pudo obtener datos (Código {response.status}){c.RESET}")
                return None

        data = response.read().decode()
        
        
        return json.loads(data)  # Puede lanzar json.JSONDecodeError
    except http.client.HTTPException as e:
        print(f"{c.RED}Error de conexión: {e}{c.RESET}")
        return None
    except json.JSONDecodeError:
        print(f"{c.RED}Error: No se pudo decodificar la respuesta de GitHub.{c.RESET}")
        return None
    finally:
        if connection:
            connection.close()

def display_activity(events):
    if not events or not isinstance(events, list):
        print(f"{c.YELLOW}No hay actividad reciente o la respuesta no es válida.{c.RESET}")
        return

    print(f"{c.BLUE}Última actividad en GitHub:{c.RESET}\n")

    for i, event in enumerate(events[:5]):  
        event_type = event.get("type", "Evento desconocido")
        repo = event.get("repo", {})
        repo_name = repo.get("name", "Repositorio desconocido")

        for commit in commits:
            message = commit.get("message", "Sin mensaje")
            print(f"    {c.CYAN}- {message}{c.RESET}")

        if event_type == "PushEvent":
            commits = event.get("payload", {}).get("commits", [])
            print(f"{c.GREEN}- Pushed {len(commits)} commit(s) to {repo_name}{c.RESET}")

        elif event_type == "IssuesEvent":
            action = event.get("payload", {}).get("action", "realizó una acción en")
            print(f"{c.YELLOW}- {action.capitalize()} an issue in {repo_name}{c.RESET}")
        
        elif event_type == "WatchEvent":
            print(f"{c.BLUE}- Starred {repo_name}{c.RESET}")
        
        else:
            print(f"{c.RED}- {event_type} in {repo_name}{c.RESET}")

    if len(events) > 5:
        ver_mas = input(f"{c.YELLOW}¿Quieres ver más eventos? (s/n): {c.RESET}").strip().lower()
        if ver_mas == "s":
            for event in events[5:10]:  # Mostramos otros 5 eventos
                event_type = event.get("type", "Evento desconocido")
                repo = event.get("repo", {})
                repo_name = repo.get("name", "Repositorio desconocido")
                print(f"{c.CYAN}- {event_type} en {repo_name}{c.RESET}")



def main():
    if len(sys.argv) < 2:
        print(f"{c.RED}Uso: github-activity <username>{c.RESET}")
        return

    username = sys.argv[1].strip()  # Eliminar espacios extra
    if not username:
        print(f"{c.RED}Error: Debes proporcionar un nombre de usuario válido.{c.RESET}")
        return

    print(f"{c.BLUE}Buscando actividad para el usuario: {username}{c.RESET}")

    events = fetch_github_activity(username)
    
    if events is not None:
        display_activity(events)


if __name__ == "__main__":
    main()
