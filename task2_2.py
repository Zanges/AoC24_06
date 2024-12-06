from task1 import load, prepare, DIRECTIONS


def next_direction(current_direction: int) -> int:
    return (current_direction + 1) % 4


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


def move(map_2d: list[list[str]], guard_x: int, guard_y: int, direction: int):
    rows, cols = len(map_2d), len(map_2d[0])
    dx, dy = 0, 0
    if direction == 0:  # UP
        dy = -1
    elif direction == 1:  # RIGHT
        dx = 1
    elif direction == 2:  # DOWN
        dy = 1
    elif direction == 3:  # LEFT
        dx = -1

    # Calculate new position
    new_x, new_y = guard_x + dx, guard_y + dy

    # Check boundaries or obstacles
    if new_x < 0 or new_x >= cols or new_y < 0 or new_y >= rows:
        #out of bounds
        map_2d[guard_y][guard_x] = "X"
        return map_2d, -1, -1, direction, None
    if map_2d[new_y][new_x] in "#O":
        #obstacle
        direction = next_direction(direction)
        return map_2d, guard_x, guard_y, direction, None

    # Move the guard
    map_2d[guard_y][guard_x] = "X"  # Mark previous position
    map_2d[new_y][new_x] = "G"  # Mark new position

    # Return updated map, new guard position, direction, and the move
    done_move = ((guard_x, guard_y), direction, (new_x, new_y))
    return map_2d, new_x, new_y, direction, done_move


def main():
    data = load("input.txt")
    #data = load("dummy_data.txt")
    map_2d = prepare(data)
    blank_map_2d = [row.copy() for row in map_2d]
    start_x, start_y = get_start_position(map_2d)
    start_direction = 0

    # Initialize guard position
    guard_x, guard_y = start_x, start_y
    direction = start_direction

    # Try moving the guard within the main map
    while True:
        map_2d, guard_x, guard_y, direction, _ = move(map_2d, guard_x, guard_y, direction)
        for row in map_2d:
            print("".join(row))
        print()
        if guard_x == -1 or guard_y == -1:
            break
    for row in map_2d:
        print("".join(row))
    print()

    # Build alternative maps
    alternative_maps = list(build_alternative_maps(map_2d, blank_map_2d, start_x, start_y))
    alt_map_count = len(alternative_maps)
    curr_map_count = 1
    possible_loops = []

    # Process each alternative map
    for alternative_map_2d in alternative_maps:
        print(f"{curr_map_count}/{alt_map_count}")
        curr_map_count += 1

        # Reset direction and guard position for each alternative map
        direction = start_direction
        guard_x, guard_y = start_x, start_y
        map_2d = [row.copy() for row in alternative_map_2d]
        previous_moves = []
        tries = 0

        # Simulate movements in the alternative map
        while tries < 100000:
            map_2d, guard_x, guard_y, direction, last_move = move(map_2d, guard_x, guard_y, direction)
            if guard_x == -1 or guard_y == -1:
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

    # Output the results
    print(len(possible_loops))


if __name__ == "__main__":
    main()