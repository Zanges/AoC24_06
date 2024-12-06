DIRECTIONS = {
    0: {"readable": "UP", "dx": 0, "dy": -1},
    1: {"readable": "RIGHT", "dx": 1, "dy": 0},
    2: {"readable": "DOWN", "dx": 0, "dy": 1},
    3: {"readable": "LEFT", "dx": -1, "dy": 0},
}

current_direction = 0


def load(filename: str) -> str:
    """Load data as a long string"""
    with open(filename, "r") as fileobj:
        return fileobj.read()


def prepare(data: str) -> list[list[str]]:
    global current_direction
    if "^" in data:
        current_direction= 0
        data = data.replace("^", "G")
    elif ">" in data:
        current_direction = 1
        data = data.replace(">", "G")
    elif "v" in data:
        current_direction = 2
        data = data.replace("v", "G")
    elif "<" in data:
        current_direction = 3
        data = data.replace("<", "G")
    return [list(row) for row in data.split("\n") if row]


def next_direction() -> None:
    global current_direction
    current_direction = (current_direction + 1) % 4


def move(map_2d: list[list[str]]) -> list[list[str]]:
    global current_direction

    guard_x, guard_y = None, None
    for y, row in enumerate(map_2d):
        for x, cell in enumerate(row):
            if cell == "G":
                guard_x, guard_y = x, y
                break

    if guard_x is None or guard_y is None:
        raise ValueError("Guard not found")

    current_direction_readable = DIRECTIONS[current_direction]["readable"]
    new_map_2d = [row.copy() for row in map_2d]
    if (
        (current_direction_readable == "UP" and guard_y == 0)
        or (current_direction_readable == "RIGHT" and guard_x == len(map_2d[0]) - 1)
        or (current_direction_readable == "DOWN" and guard_y == len(map_2d) - 1)
        or (current_direction_readable == "LEFT" and guard_x == 0)
    ):
        new_map_2d[guard_y][guard_x] = "X"
        return new_map_2d

    if new_map_2d[guard_y + DIRECTIONS[current_direction]["dy"]][guard_x + DIRECTIONS[current_direction]["dx"]] in "#O":
        next_direction()
        return new_map_2d

    new_map_2d[guard_y + DIRECTIONS[current_direction]["dy"]][guard_x + DIRECTIONS[current_direction]["dx"]] = "G"
    new_map_2d[guard_y][guard_x] = "X"
    return new_map_2d


def count_guard_visited_cells(map_2d: list[list[str]]) -> int:
    return sum(row.count("X") for row in map_2d)


def main():
    data = load("input.txt")
    # data = load("dummy_data2.txt")
    map_2d = prepare(data)
    for row in map_2d:
        print("".join(row))
    print()
    tries = 0
    while tries < 100000:
        try:
            map_2d = move(map_2d)
        except ValueError as e:
            print(e)
            break
        tries += 1
    if tries == 100000:
        print("Loop detected")
    for row in map_2d:
        print("".join(row))
    print()
    print(count_guard_visited_cells(map_2d))


if __name__ == "__main__":
    main()