def chunk(get_key, items):
    current_key = None
    current_chunk = []
    for item in items:
        key = get_key(item)
        if key == current_key:
            current_chunk.append(item)
        else:
            if current_chunk:
                yield current_key, current_chunk
            current_chunk = [item]
            current_key = key
    if current_chunk:
        yield current_key, current_chunk


# def chunk2(get_key, items):
#   def helper(current_chunk, current_key, items):
#     item = items.pop()
#     key = get_key(item)
#     if key == current_key:
#       return helper(current_chunk + [item], current_key, items)


def by_key(key, items):
    return chunk(lambda item: item[key], items)


def indent(num, string):
    return ("  " * num) + string
