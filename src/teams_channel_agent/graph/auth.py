"""Autenticazione Microsoft Graph tramite device code flow (MSAL).

Nessun client secret: è un "public client" (vedi config.py). Il token
viene salvato in una cache locale cifrata-su-disco di MSAL
(`.msal_token_cache.bin`, ignorata da git) per evitare di rifare il
login a ogni esecuzione.
"""
from __future__ import annotations

import sys
from pathlib import Path

import msal

from ..config import PROJECT_ROOT, graph_settings

TOKEN_CACHE_PATH = PROJECT_ROOT / ".msal_token_cache.bin"


def _build_cache() -> msal.SerializableTokenCache:
    cache = msal.SerializableTokenCache()
    if TOKEN_CACHE_PATH.exists():
        cache.deserialize(TOKEN_CACHE_PATH.read_text())
    return cache


def _persist_cache(cache: msal.SerializableTokenCache) -> None:
    if cache.has_state_changed:
        TOKEN_CACHE_PATH.write_text(cache.serialize())


def _build_app(cache: msal.SerializableTokenCache) -> msal.PublicClientApplication:
    return msal.PublicClientApplication(
        client_id=graph_settings.client_id,
        authority=graph_settings.authority,
        token_cache=cache,
    )


def get_access_token(scopes: tuple[str, ...] | None = None) -> str:
    """Restituisce un access token valido, usando la cache se possibile,
    altrimenti avviando il device code flow (login via browser Windows).
    """
    scopes = scopes or graph_settings.scopes
    cache = _build_cache()
    app = _build_app(cache)

    accounts = app.get_accounts()
    result = None
    if accounts:
        result = app.acquire_token_silent(list(scopes), account=accounts[0])

    if not result:
        flow = app.initiate_device_flow(scopes=list(scopes))
        if "user_code" not in flow:
            raise RuntimeError(f"Impossibile avviare il device flow: {flow}")
        print(flow["message"], file=sys.stderr)
        result = app.acquire_token_by_device_flow(flow)

    _persist_cache(cache)

    if "access_token" not in result:
        error = result.get("error")
        description = result.get("error_description")
        raise RuntimeError(f"Autenticazione fallita: {error} — {description}")

    return result["access_token"]
