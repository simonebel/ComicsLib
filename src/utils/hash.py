import xxhash


def hash_xxh(text: str) -> int:
    x = xxhash.xxh32()
    x.update(text)
    return x.intdigest()
