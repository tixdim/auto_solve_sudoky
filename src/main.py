import time
import webbrowser

import screenshot
import recognition
import sudoku
import config


def main() -> None:
    print("[INFO] Start")
    full_image = screenshot.capture_full_screen()
    print("[INFO] Get screen")
    sudoku_bounds = screenshot.find_sudoku_bounds(full_image)
    print("[INFO] Find sudoku in screen")
    sudoku_image = screenshot.crop_to_sudoku(full_image)
    print("[INFO] Crop sudoku screen")

    print("\n[INFO] Defining numbers..")
    recognized_sudoku = recognition.recognize_sudoku(sudoku_image)
    print("Recognized sudoku:")
    sudoku.print_pretty(recognized_sudoku)

    print("\n[INFO] Solving sudoku..")
    solved_sudoku = sudoku.get_solution(recognized_sudoku)
    print("Solved sudoku:")
    sudoku.print_pretty(solved_sudoku)

    print("\n[INFO] Inserting numbers..\n")
    sudoku.fill_in_gui(solved_sudoku, sudoku_bounds)


if __name__ == '__main__':
    if config.TEST == 1:
        webbrowser.open('https://sudoku.com/medium/')
        time.sleep(5)
    start = time.perf_counter()

    main()

    end = time.perf_counter()
    print(f'Time taken: {round(end - start, 2)} seconds')