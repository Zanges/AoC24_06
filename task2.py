from task1 import load, prepare, DIRECTIONS


current_direction = 0


def next_direction() -> None:
    global current_direction
    current_direction = (current_direction + 1) % 4


def get_start_position(map_2d: list[list[str]]) -> tuple[int, int]:
    for y, row in enumerate(map_2d):
        for x, cell in enumerate(row):
            if cell == "G":
                return x, y
    raise ValueError("Guard not found")


def build_alternative_maps(solved_map_2d: list[list[str]], blank_map_2d: list[list[str]], start_x: int, start_y: int) -> list[list[list[str]]]:
    possible_positions: list[tuple[int, int]] = []
    for y, row in enumerate(solved_map_2d):
        for x, cell in enumerate(row):
            if cell == "X":
                possible_positions.append((x, y))
    possible_positions.remove((start_x, start_y))

    for x, y in possible_positions:
        new_map_2d = [row.copy() for row in blank_map_2d]
        new_map_2d[y][x] = "O"
        new_map_2d[start_y][start_x] = "G"
        yield new_map_2d


def move(map_2d: list[list[str]]):
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
        return new_map_2d, None

    if new_map_2d[guard_y + DIRECTIONS[current_direction]["dy"]][guard_x + DIRECTIONS[current_direction]["dx"]] in "#O":
        next_direction()
        return new_map_2d, None

    new_map_2d[guard_y + DIRECTIONS[current_direction]["dy"]][guard_x + DIRECTIONS[current_direction]["dx"]] = "G"
    new_map_2d[guard_y][guard_x] = "X"
    done_move = ((guard_x, guard_y), current_direction, (guard_x + DIRECTIONS[current_direction]["dx"], guard_y + DIRECTIONS[current_direction]["dy"]))
    return new_map_2d, done_move


def main():
    global current_direction
    data = load("input.txt")
    # data = load("dummy_data.txt")
    map_2d = prepare(data)
    blank_map_2d = [row.copy() for row in map_2d]
    start_x, start_y = get_start_position(map_2d)
    start_direction = current_direction

    while True:
        try:
            map_2d, _ = move(map_2d)
        except ValueError as e:
            print(e)
            break
    for row in map_2d:
        print("".join(row))
    print()

    alternative_maps = list(build_alternative_maps(map_2d, blank_map_2d, start_x, start_y))
    alt_map_count = len(alternative_maps)
    curr_map_count = 1
    possible_loops = []
    for alternative_map_2d in alternative_maps:
        print(f"{curr_map_count}/{alt_map_count}")
        curr_map_count += 1
        current_direction = start_direction
        map_2d = [row.copy() for row in alternative_map_2d]
        previous_moves = []
        tries = 0
        while tries < 100000:
            try:
                map_2d, last_move = move(map_2d)
            except ValueError as e:
                break
            if last_move is not None:
                if last_move in previous_moves:
                    possible_loops.append(previous_moves[previous_moves.index(last_move):])
                    break
                previous_moves.append(last_move)
            tries += 1
        if tries == 100000:
            print("Too many tries")
            for row in map_2d:
                print("".join(row))

    print(len(possible_loops))


if __name__ == "__main__":
    main()