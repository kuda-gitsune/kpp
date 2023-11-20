button_style = """
QPushButton {
    background-color: #E6E6E6; /* Light grey background */
    color: #0057B8; /* Blue text */
    border: 1px solid #0057B8; /* Blue border */
    padding: 10px 20px; /* Padding inside the button */
    border-radius: 15px; /* Rounded corners */
    font-size: 14px; /* Font size */
    font-weight: bold; /* Font weight */
}

QPushButton:hover {
    background-color: #CCD1D9; /* Slightly darker background on hover */
}

QPushButton:pressed {
    background-color: #B3BCC7; /* Even darker background when pressed */
}
"""
button_style = """
QPushButton {
    background-color: #E6E6E6; /* Light grey background */
    color: #0057B8; /* Blue text */
    border: 1px solid #0057B8; /* Blue border */
    padding: 10px 20px; /* Padding inside the button */
    border-radius: 15px; /* Rounded corners */
    font-size: 14px; /* Font size */
    font-weight: bold; /* Font weight */
}

QPushButton:hover {
    background-color: #CCD1D9; /* Slightly darker background on hover */
}

QPushButton:pressed {
    background-color: #B3BCC7; /* Even darker background when pressed */
}
"""

text_edit_true_style = """
QLabel {
    margin: 1px;
    padding: 8px; /* Padding inside the text edit */
    background-color: #008000; /* Green background */
    color: white; /* White text */
    border: 1px solid #008000; /* Green grey border */    
    border-radius: 4px; /* Slightly rounded corners */
    font-size: 16px; /* Font size */
}
"""
# text_edit_default_style = """
# QLabel {
#     margin: 1px;
#     padding: 8px; /* Padding inside the text edit */
#     background-color: #FFFFFF; /* White background */
#     color: #000000; /* Black text */
#     border: 1px solid #D3D3D3; /* Light grey border */
#     border-radius: 4px; /* Rounded corners */
#     padding: 4px; /* Padding inside the text edit */
#     font-size: 16px; /* Adjust font size as needed */
# }
# """
# border: 2px solid #006400; /* Darker green border */

text_edit_default_style = """
QLabel {
    margin: 1px;
    padding: 8px; /* Padding inside the text edit */
    background-color: #FFFFFF; /* Dark red background */
    color: #000000; /* White text */
    border: 1px solid #D3D3D3; /* Dark red border */
    border-radius: 4px; /* Rounded corners */
    font-size: 16px; /* Adjust font size as needed */
    /* Additional styles might be needed depending on the full requirements */
}
"""
text_edit_wrong_style = """
QLabel {
    margin: 1px;
    padding: 8px; /* Padding inside the text edit */
    background-color: #C0392B; /* Dark red background */
    color: white; /* White text */
    border: 1px solid #C0392B; /* Dark red border */
    border-radius: 4px; /* Rounded corners */
    font-size: 16px; /* Adjust font size as needed */
    /* Additional styles might be needed depending on the full requirements */
}
"""
# border: 1px solid #A93226; /* Slightly darker red border */

label_style = """
QLabel {
    margin-bottom: 8px;
    color: #000000; /* Black text */
    padding: 4px; /* Padding inside the text edit */
    font-size: 16px; /* Adjust font size as needed */
}
"""


class DefaultStyles():
    button = button_style
    label = label_style
    text_edit_default = text_edit_default_style
    text_edit_true = text_edit_true_style
    text_edit_wrong = text_edit_wrong_style
