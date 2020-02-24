import pyperclip
import keyboard_mouse
import re
import time

# Configurations
STASH_FILLED_COLUMNS = 12
INVENTORY_EMPTY_COLUMNS = 12

# Mouse X,Y Coordinates
POINT_STASH_FIRST = (40, 190)
POINT_STASH_LAST = (620, 770)
POINT_INVENTORY_FIRST = (1940, 610)
POINT_INVENTORY_LAST = (2520, 820)

# 0. Keyboard & Mouse Class Instances
keyboard = keyboard_mouse.Keyboard()
mouse = keyboard_mouse.Mouse(POINT_STASH_FIRST, POINT_STASH_LAST, POINT_INVENTORY_FIRST, POINT_INVENTORY_LAST)
quality_pattern = re.compile(r"Quality: \+(\d{1,2})%")


def main():
    # 1. Gather Info (Skill Gems in StashTab)
    stash_items = set()
    for idx in range(12 * STASH_FILLED_COLUMNS):
        # Clean Clipboard
        pyperclip.copy('')

        # Move Mouse & [Ctrl + C]
        mouse.move(idx, 'stash')
        time.sleep(0.1)
        keyboard.ctrl_c()
        time.sleep(0.05)

        # Extract Gem Quality from clipboard text
        clipboard_text = pyperclip.paste()
        quality = extract_quality(clipboard_text)
        if quality:
            stash_items.add((idx, quality))

    # 2. Find Quality Sum 40 (Backtracking)
    found_groups = list()
    while True:
        found_group = backtrack_find_sum_40(list(), stash_items)
        if found_group:
            found_groups.append(found_group)
            stash_items -= set(found_group)
        else:
            break

    # 3. Move Gems from Stash tab to Inventory (Skill Gems with 40 sum)
    current_inventory_position = 0
    for found in found_groups:
        if current_inventory_position + len(found) <= INVENTORY_EMPTY_COLUMNS * 5:
            for gem_idx, _ in found:
                # From Stash
                mouse.move(gem_idx, 'stash')
                mouse.click()
                # To Inventory
                mouse.move(current_inventory_position, 'inventory')
                mouse.click()
                # Move to Next Position
                current_inventory_position += 1

            # Make sure each group start from a new Column
            mod = current_inventory_position % 5
            if mod > 0:
                current_inventory_position += 5 - mod


def extract_quality(text):
    search_result = quality_pattern.search(text)
    if search_result:
        quality = int(search_result.group(1))
        if quality:
            return quality


def backtrack_find_sum_40(pick, pool):
    sum_ = sum(p[1] for p in pick)
    if sum_ == 40:
        return True
    elif sum_ > 40:
        return False

    for pool_item in pool:
        pick.append(pool_item)
        if backtrack_find_sum_40(pick, pool - {pool_item}):
            return pick
        else:
            pick.remove(pool_item)


if __name__ == '__main__':
    time.sleep(2)
    main()
