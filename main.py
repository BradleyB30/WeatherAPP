import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt

class FullScreenWeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.showFullScreen()
        self.setWindowTitle("Bradley's Weather App")  # Custom title

        self.city_label = QLabel("Enter City Name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Check Weather", self)
        self.temperature_display = QLabel(self)
        self.emoji_display = QLabel(self)
        self.weather_desc_display = QLabel(self)
        self.info_button = QPushButton("Info", self)  # Info button

        layout = QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.temperature_display)
        layout.addWidget(self.emoji_display)
        layout.addWidget(self.weather_desc_display)
        layout.addWidget(self.info_button)
        self.setLayout(layout)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_display.setAlignment(Qt.AlignCenter)
        self.emoji_display.setAlignment(Qt.AlignCenter)
        self.weather_desc_display.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QWidget{
                background-color: #1C1C1C;
                color: #FFFFFF;
            }
            QLabel, QPushButton{
                font-family: 'Arial', sans-serif;
            }
            QLabel#city_label{
                font-size: 36px;
                font-weight: 600;
                color: #00BFFF;
            }
            QLineEdit#city_input{
                font-size: 32px;
                padding: 10px;
                border: 2px solid #00BFFF;
                border-radius: 5px;
                background-color: #2C2C2C;
                color: #FFFFFF;
            }
            QPushButton#get_weather_button{
                font-size: 28px;
                padding: 10px;
                background-color: #00BFFF;
                color: #FFFFFF;
                border-radius: 5px;
                border: none;
            }
            QPushButton#get_weather_button:hover{
                background-color: #1E90FF;
            }
            QLabel#temperature_display{
                font-size: 80px;
                font-weight: 700;
                color: #FFD700;
            }
            QLabel#emoji_display{
                font-size: 100px;
                color: #FFD700;
            }
            QLabel#weather_desc_display{
                font-size: 40px;
                color: #87CEEB;
            }
            QPushButton#info_button{
                font-size: 24px;
                padding: 10px;
                background-color: #00BFFF;
                color: #FFFFFF;
                border-radius: 5px;
                border: none;
            }
            QPushButton#info_button:hover{
                background-color: #1E90FF;
            }
        """)

        self.get_weather_button.clicked.connect(self.fetch_weather_data)
        self.info_button.clicked.connect(self.show_info)  # Connect info button

    def fetch_weather_data(self):
        api_key = "af6bf75243a9cfaad959b2c22a50e9af"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()

            if weather_data["cod"] == 200:
                self.update_weather_display(weather_data)
        except requests.exceptions.RequestException as error:
            self.show_error_message(str(error))

    def update_weather_display(self, weather_data):
        temperature_kelvin = weather_data["main"]["temp"]
        temperature_fahrenheit = (temperature_kelvin * 9/5) - 459.67
        weather_code = weather_data["weather"][0]["id"]
        weather_description = weather_data["weather"][0]["description"]

        self.temperature_display.setText(f"{temperature_fahrenheit:.0f}°F")
        self.emoji_display.setText(self.get_weather_emoji(weather_code))
        self.weather_desc_display.setText(weather_description)

    def show_error_message(self, message):
        self.temperature_display.setStyleSheet("font-size: 30px;")
        self.temperature_display.setText("Error!")
        self.weather_desc_display.setText(message)
        self.emoji_display.clear()

    def get_weather_emoji(self, weather_code):
        if 200 <= weather_code <= 232:
            return "⛈️"
        elif 300 <= weather_code <= 321:
            return "🌦️"
        elif 500 <= weather_code <= 531:
            return "🌧️"
        elif 600 <= weather_code <= 622:
            return "❄️"
        elif 701 <= weather_code <= 741:
            return "🌫️"
        elif weather_code == 800:
            return "☀️"
        elif 801 <= weather_code <= 804:
            return "☁️"
        else:
            return "🌈"

    def show_info(self):
        QMessageBox.information(self, "PM Accelerator Info", 
            "The Product Manager Accelerator Program is designed to support PM professionals through every stage of their career. "
            "From students looking for entry-level jobs to Directors looking to take on a leadership role, our program has helped "
            "hundreds of students fulfill their career aspirations.\n\n"
            "Our Product Manager Accelerator community is ambitious and committed. Through our program, they have learned, honed, "
            "and developed new PM and leadership skills, giving them a strong foundation for their future endeavors.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    full_screen_app = FullScreenWeatherApp()
    full_screen_app.show()
    sys.exit(app.exec_())
