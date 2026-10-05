"""Entry point CLI dell'agente (opzionale rispetto all'uso diretto in Copilot CLI).

Uso:
    python -m teams_channel_agent.main chat
    python -m teams_channel_agent.main check-env

La modalità 'chat' interattiva è opzionale (vedi documento di concept):
va mantenuta solo se l'interazione nativa della Copilot CLI non risulta
sufficiente.
"""
from __future__ import annotations

import sys

from rich.console import Console

console = Console()


def check_env() -> None:
    """Verifica non distruttiva dell'ambiente (Milestone 0 / 1)."""
    import platform

    from .config import graph_settings

    console.print("[bold]Teams Channel Agent — check ambiente[/bold]")
    console.print(f"Python: {sys.version.split()[0]}")
    console.print(f"Piattaforma: {platform.platform()}")
    console.print(
        f"MS_TENANT_ID configurato: {'si' if graph_settings.tenant_id else 'NO (vedi .env.example)'}"
    )
    console.print(
        f"MS_CLIENT_ID configurato: {'si' if graph_settings.client_id else 'NO (vedi .env.example)'}"
    )


def chat() -> None:
    console.print(
        "[yellow]Modalita chat interattiva non ancora implementata.[/yellow]\n"
        "In questa fase l'interazione avviene direttamente tramite GitHub Copilot CLI."
    )


def login() -> None:
    """Milestone 3: primo test di autenticazione device code flow."""
    from .config import graph_settings
    from .graph.auth import get_access_token

    console.print("[bold]Teams Channel Agent — login Microsoft Graph[/bold]")
    console.print(f"Authority: {graph_settings.authority}")
    console.print(f"Client ID: {graph_settings.client_id}")
    console.print(f"Scopes: {', '.join(graph_settings.scopes)}")
    console.print(
        "Segui le istruzioni mostrate (apri il link nel browser Windows e "
        "inserisci il codice). L'esecuzione resta in WSL.\n"
    )
    token = get_access_token()
    console.print(f"\n[green]Login riuscito.[/green] Token ricevuto (len={len(token)}).")


def whoami() -> None:
    """Milestone 4: prima chiamata reale a Microsoft Graph (/me)."""
    import httpx

    from .config import graph_settings
    from .graph.auth import get_access_token

    token = get_access_token()
    resp = httpx.get(
        f"{graph_settings.graph_base_url}/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    console.print("[bold]/me[/bold]")
    console.print(f"Nome: {data.get('displayName')}")
    console.print(f"UPN: {data.get('userPrincipalName')}")


def list_opportunities() -> None:
    """Elenca le opportunità (sottocartelle) nel canale Teams sincronizzato."""
    from .local_files.browser import list_opportunities as _list_opportunities

    console.print("[bold]Opportunità disponibili (fonte: file locale / OneDrive sync)[/bold]")
    for opp in _list_opportunities():
        console.print(f"- {opp.name}")


def list_files() -> None:
    """Elenca i file di una opportunità. Uso: list-files <nome opportunità>"""
    from .local_files.browser import list_files as _list_files

    args = sys.argv[2:]
    if not args:
        console.print("[red]Specifica il nome dell'opportunità.[/red]")
        console.print("Uso: python -m teams_channel_agent.main list-files <nome>")
        sys.exit(1)

    opportunity_name = args[0]
    console.print(f"[bold]File per opportunità '{opportunity_name}' (fonte: file locale / OneDrive sync)[/bold]")
    for f in _list_files(opportunity_name):
        console.print(f"- {f}")


def main() -> None:
    args = sys.argv[1:]
    command = args[0] if args else "check-env"

    commands = {
        "check-env": check_env,
        "chat": chat,
        "login": login,
        "whoami": whoami,
        "list-opportunities": list_opportunities,
        "list-files": list_files,
    }

    if command in commands:
        commands[command]()
    else:
        console.print(f"[red]Comando sconosciuto:[/red] {command}")
        console.print(f"Comandi disponibili: {', '.join(commands)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
