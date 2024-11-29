import sys
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import Qt, QTimer, QDateTime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MPU6050 Data")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.chart_view = QChartView(self)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.chart_view)

        self.accel_series_x = QLineSeries()
        self.accel_series_x.setName("Accelerometer Data X")
        self.accel_series_y = QLineSeries()
        self.accel_series_y.setName("Accelerometer Data Y")
        self.accel_series_z = QLineSeries()
        self.accel_series_z.setName("Accelerometer Data Z")

        self.chart = QChart()
        self.chart.addSeries(self.accel_series_x)
        self.chart.addSeries(self.accel_series_y)
        self.chart.addSeries(self.accel_series_z)

        self.chart.createDefaultAxes()
        self.chart.setTitle("MPU6050 Accelerometer Data")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart_view.setChart(self.chart)

        self.chart_view.chart().axisY().setRange(-2, 2)  # Set the Y-axis range

        self.serial_port = serial.Serial('/dev/tty.usbmodem204C397F32321', 115200)  # Replace 'COMx' with your actual serial port

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(500)  # Update chart every 500 milliseconds

    def update_chart(self):
        self.serial_port.write(b'#GETMPU\n')
        line = self.serial_port.readline().decode('utf-8').strip()
        if line.startswith("ok"):
            data_str = line[3:].split(' ')
            if len(data_str) == 3:
                try:
                    accel_data = [float(val) for val in data_str]
                    timestamp = QDateTime.currentDateTime().toMSecsSinceEpoch()

                    self.accel_series_x.append(timestamp, accel_data[0])
                    self.accel_series_y.append(timestamp, accel_data[1])
                    self.accel_series_z.append(timestamp, accel_data[2])

                    # Clear previous data points to avoid cluttering the chart
                    if self.accel_series_x.count() > 120:
                        self.accel_series_x.removePoints(0, self.accel_series_x.count() - 20)
                        self.accel_series_y.removePoints(0, self.accel_series_y.count() - 20)
                        self.accel_series_z.removePoints(0, self.accel_series_z.count() - 20)

                    self.chart_view.chart().axisX().setRange(timestamp - 120000, timestamp)  # Show the last 20 seconds
                except ValueError as e:
                    print(f"Error parsing data: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

