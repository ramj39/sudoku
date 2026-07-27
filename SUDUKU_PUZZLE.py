import streamlit as st
import random

# Sudoku generator (same as before)
def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def fill_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if fill_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)
    attempts = 40
    while attempts > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0
        attempts -= 1
    return board

# Display board with HTML table
def display_board(board):
    html = "<table style='border-collapse: collapse; margin:auto;'>"
    for i in range(9):
        html += "<tr>"
        for j in range(9):
            val = board[i][j]
            if val == 0:
                cell = f"<input type='text' maxlength='1' style='width:30px; height:30px; text-align:center; border:1px solid #555;'>"
            else:
                color = "red" if val in [1,7,9] else "blue" if val in [4,6] else "black"
                cell = f"<div style='width:30px; height:30px; text-align:center; border:1px solid #555; color:{color}; font-weight:bold'>{val}</div>"
            html += f"<td>{cell}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

def main():
    st.title("🎲 Sudoku Game")
    st.write("Fill in the blanks and play!")

    if "board" not in st.session_state:
        st.session_state.board = generate_board()

    display_board(st.session_state.board)

    if st.button("🔄 Generate New Game"):
        st.session_state.board = generate_board()
        display_board(st.session_state.board)

    if st.button("✅ Check Solution"):
        solved = True
        for i in range(9):
            for j in range(9):
                val = st.session_state.get(f"cell_{i}_{j}", st.session_state.board[i][j])
                if val != 0 and not is_valid(st.session_state.board, i, j, val):
                    solved = False
        if solved:
            st.success("🎉 Congratulations, you solved it!")
            st.snow()   # ❄️ Snowflakes animation
        else:
            st.error("❌ Some numbers are incorrect.")


if st.button("💾 Download Board"):
    output = io.StringIO()
    for row in st.session_state.board:
        output.write(" ".join(str(x) if x != 0 else "_" for x in row) + "\n")
    st.download_button("⬇️ Save as TXT", output.getvalue(), "sudoku_board.txt")

if __name__ == "__main__":
    main()
st.write("thanks for using the Suduku app-subramanian ramajayam,developed with support of Microsoft Copilot")
