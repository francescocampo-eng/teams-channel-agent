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


def main() -> None:
    args = sys.argv[1:]
    command = args[0] if args else "check-env"

    if command == "check-env":
        check_env()
    elif command == "chat":
        chat()
    else:
        console.print(f"[red]Comando sconosciuto:[/red] {command}")
        console.print("Comandi disponibili: check-env, chat")
        sys.exit(1)


if __name__ == "__main__":
    main()
