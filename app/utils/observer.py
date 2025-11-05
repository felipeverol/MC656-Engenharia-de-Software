from typing import List, Callable, Dict, Any

_listeners: Dict[str, List[Callable]] = {}

def subscribe(event_name: str, callback: Callable):
    # Anexa um observador a um evento.
    if event_name not in _listeners:
        _listeners[event_name] = []
    _listeners[event_name].append(callback)

def post_event(event_name: str, *args, **kwargs):
    # Chama todos os observadores registrados para um evento.

    if event_name not in _listeners:
        return 
    print(f"--- [Observer] Evento '{event_name}' disparado ---")
    for callback in _listeners[event_name]:
        callback(*args, **kwargs) # Chama a função do observador