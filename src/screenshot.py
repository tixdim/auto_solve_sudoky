from typing import TypeAlias
from dataclasses import dataclass
import time

from PIL import Image, ImageGrab
import numpy as np
import cv2

import config

Pixels: TypeAlias = int


@dataclass(frozen=True)
class SudokuBounds:
    top_left_x: Pixels
    top_left_y: Pixels
    width: Pixels
    cell_width: Pixels


@dataclass(frozen=True)
class CellCoordinates:
    x0: Pixels
    y0: Pixels
    x1: Pixels
    y1: Pixels


def capture_full_screen() -> Image:
    time.sleep(config.SCREENSHOT_DELAY)

    file = open('../full_screen.png', 'wb')
    screenshot = ImageGrab.grab()
    screenshot.save(file, 'PNG')
    file.close()

    return screenshot


def find_sudoku_bounds(screenshot: Image) -> SudokuBounds:
    gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    edges = cv2.Canny(thresh, 50, 100)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    top_left_x = 0
    top_left_y = 0
    square_width = 0
    square_threshold = 0.005

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.005 * perimeter, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = abs(w - h) / min(w, h)
            if aspect_ratio < square_threshold and w > square_width:
                roi = thresh[y:y+h, x:x+w]
                lines = cv2.HoughLinesP(roi, rho=1, theta=np.pi/180, threshold=50, minLineLength=w//2, maxLineGap=w//10)
                if lines is not None and len(lines) >= 16:
                    top_left_x, top_left_y, square_width = x, y, w

    return SudokuBounds(top_left_x, top_left_y, square_width, square_width // 9)


def crop_to_sudoku(screenshot: Image) -> Image:
    sudoku_bounds = find_sudoku_bounds(screenshot)
    y, x, image_width = sudoku_bounds.top_left_y, sudoku_bounds.top_left_x, sudoku_bounds.width
    cropped_image = np.array(screenshot)[y:y + image_width, x:x + image_width]

    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    file = open('../sudoku.png', 'wb')
    Image.fromarray(thresh).save(file, 'PNG')
    file.close()

    return Image.fromarray(thresh)


def get_sudoku_cells_coordinates(cell_width: Pixels) -> list[CellCoordinates]:
    border_offset: Pixels = 5
    cells = []

    for row in range(9):
        for col in range(9):
            x0 = col * cell_width + border_offset
            y0 = row * cell_width + border_offset
            x1 = x0 + cell_width - border_offset
            y1 = y0 + cell_width - border_offset
            cells.append(CellCoordinates(x0, y0, x1, y1))

    return cells