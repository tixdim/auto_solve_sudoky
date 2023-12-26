from typing import Optional, TypeAlias
import pyautogui
import screenshot

Sudoku: TypeAlias = list[list[int]]


def get_solution(sudoku: Sudoku) -> Sudoku:
    def find_empty_cell() -> Optional[tuple[int, int]]:
        for row in range(9):
            for col in range(9):
                if sudoku[row][col] == 0:
                    return row, col
        return None

    def value_is_valid(row_idx: int, col_idx: int, val: int) -> bool:
        row_ok = all(val != sudoku[row_idx][k] for k in range(9))
        if row_ok:
            col_ok = all(val != sudoku[k][col_idx] for k in range(9))
            if col_ok:
                box_row, box_col = 3 * (row_idx // 3), 3 * (col_idx // 3)
                for box_row_idx in range(box_row, box_row + 3):
                    for box_col_idx in range(box_col, box_col + 3):
                        if val == sudoku[box_row_idx][box_col_idx]:
                            return False
                return True
        return False

    def backtrack() -> bool:
        empty_cell = find_empty_cell()
        if empty_cell is None:
            return True
        row, col = empty_cell
        for value in range(1, 10):
            if value_is_valid(row, col, value):
                sudoku[row][col] = value
                if backtrack():
                    return True
                sudoku[row][col] = 0
        return False

    backtrack()
    return sudoku


def print_pretty(sudoku: Sudoku) -> None:
    horizontal_divider = '-------------------------'
    vertical_divider = '|'

    print(horizontal_divider)

    for i, row in enumerate(sudoku):
        print(vertical_divider, end=' ')

        for j, digit in enumerate(row):
            print(digit, end=' ')

            if (j + 1) % 3 == 0:
                print(vertical_divider, end=' ')

        print()

        if (i + 1) % 3 == 0 and i != 8:
            print(horizontal_divider)

    print(horizontal_divider)


def click_on_first_cell(bounds: screenshot.SudokuBounds) -> None:
    cell_center_width = bounds.cell_width / 2
    cell_center_x = bounds.top_left_x + cell_center_width
    cell_center_y = bounds.top_left_y + cell_center_width
    pyautogui.click(cell_center_x, cell_center_y)


def fill_in_gui(sudoku: Sudoku, bounds: screenshot.SudokuBounds) -> None:
    click_on_first_cell(bounds)

    for row in range(9):
        for i in range(9):
            pyautogui.press(str(sudoku[row][i]))
            pyautogui.press('right')
        for i in range(9):
            pyautogui.press('left')
        pyautogui.press('down')