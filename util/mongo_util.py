def is_mongo_connected(mongo_client) -> bool:
    """
    Check if the MongoDB client is connected by pinging the server.

    Args:
        mongo_client (Database): The MongoDB Database client instance.

    Returns:
        bool: True if connected, False otherwise.
    """
    try:
        mongo_client.client.admin.command('ping')
        return True
    except Exception:
        return False
