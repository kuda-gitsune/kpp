from icecream import ic
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

text = '"%(),-./0123456789:;<><br>?ABCDEGHIJKLMNOPRSTUVWZabcdefghijklmnoprstuwxyz°óąćęłńśźż„'

def main():
    app = QApplication([])
    window = QWidget()

    layout = QVBoxLayout()
    window.setLayout(layout)

    label_rich = QLabel()
    label_rich.setText(text)
    layout.addWidget(label_rich)

    window.show()
    app.exec()

if __name__ == '__main__':
    main()


# while True:
# ...     try:
# ...         letter = next(it)
# ...     except StopIteration:
# ...         break
# ...     print(letter)