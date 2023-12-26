from PIL import Image
import numpy as np

import screenshot
import config
import sudoku


def recognize_digit(cell_image: Image) -> int:
    recognition_data = config.OCR.ocr(np.array(cell_image), det=False, rec=True, cls=False)
    digit = recognition_data[0][0][0] if recognition_data[0][0] != '' else ''

    if digit == '':
        return 0

    return int(digit)


def recognize_sudoku(img: Image) -> sudoku.Sudoku:
    cell_width = img.size[0] // 9
    cells_coordinates = screenshot.get_sudoku_cells_coordinates(cell_width)

    digits = []
    for cell in cells_coordinates:
        cell_img = img.crop((cell.x0, cell.y0, cell.x1, cell.y1))
        digit = recognize_digit(cell_img)
        digits.append(digit)
    grid = []
    for i in range(0, len(digits), 9):
        grid.append(digits[i:i + 9])

    return grid