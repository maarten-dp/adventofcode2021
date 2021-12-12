from runner_utils import expected_test_result


def get_node(registry, name):
    if name in registry:
        return registry[name]
    node = Node(name)
    registry[name] = node
    return node


def get_paths(current_path, paths, end):
    node = current_path[-1]
    if node is end:
        paths.append(current_path)
        return

    for link in node.links:
        if link in current_path and not link.large:
            continue
        new_path = current_path[:]
        new_path.append(link)
        get_paths(new_path, paths, end)


def get_paths2(current_path, paths, end, visited_small_cave=None):
    node = current_path[-1]
    if len(current_path) > 1 and node is current_path[0]:
        return
    if node is end:
        if node not in current_path[:-1]:
            paths.append(current_path)
        return

    for link in node.links:
        new_visited_small_cave = visited_small_cave
        if link in current_path and not link.large:
            if visited_small_cave is None:
                new_visited_small_cave = link
            else:
                continue
        new_path = current_path[:]
        new_path.append(link)
        get_paths2(new_path, paths, end, new_visited_small_cave)


class Node:
    def __init__(self, name):
        self.name = name
        self.large = name.isupper()
        self.links = []

    def link(self, node):
        self.links.append(node)
        node.links.append(self)

    def __repr__(self):
        return self.name


def path_finder(input, finder):
    links = [l for l in input.split("\n") if l]
    registry = {}
    for link in links:
        name1, name2 = link.split("-")
        get_node(registry, name1).link(get_node(registry, name2))

    paths = []
    finder([registry["start"]], paths, registry['end'])
    return len(paths)


@expected_test_result(226)
def solve1(input):
    return path_finder(input, get_paths)


@expected_test_result(3509)
def solve2(input):
    return path_finder(input, get_paths2)
