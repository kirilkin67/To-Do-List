def add_viewer(name, fans=None):
    if fans is None:
        fans = list()
    fans.append(name)
    return fans
