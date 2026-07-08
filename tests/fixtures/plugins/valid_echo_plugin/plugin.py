"""Valid test plugin used to prove discovery and loading."""

LOADED = False


def load() -> dict[str, object]:
    """Return a sentinel that proves the plugin entry point ran."""

    global LOADED
    LOADED = True
    return {"plugin": "valid-echo", "loaded": True}

