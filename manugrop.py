import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem
from sklearn.linear_model import LinearRegression  #ส่วนโมเดลที่ไช้
import numpy as np
import pandas as pd

class TreeHeightPredictionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.age_label = QLabel('อายุของต้นไม้:')
        self.height_label = QLabel('ความสูงของต้นไม้:')
        self.weight_label = QLabel('น้ำหนักของต้นไม้:')         #ส่วนกำหนดตัวหนังสือ
        self.root_radius_label = QLabel('รัศมีโคนของต้นไม้:')
        self.num_leaves_label = QLabel('จำนวนใบของต้นไม้:')
        
        self.age_input = QLineEdit()
        self.height_input = QLineEdit()
        self.weight_input = QLineEdit()                     #ส่วนที่ไช้กรอก
        self.root_radius_input = QLineEdit()
        self.num_leaves_input = QLineEdit()
        
        self.train_button = QPushButton('เพิ่มข้อมูลฝึกฝน')
        self.load_csv_button = QPushButton('โหลดข้อมูลจาก CSV')  #ส่วนกำหนดปุ่มบนหน้าจอ
        self.predict_button = QPushButton('คาดการณ์ความสูง')
        
        self.result_label = QLabel('ผลลัพธ์:')

        self.table_label = QLabel('ข้อมูลจาก CSV:')
        self.csv_table = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_input)
        layout.addWidget(self.root_radius_label)
        layout.addWidget(self.root_radius_input)
        layout.addWidget(self.num_leaves_label)
        layout.addWidget(self.num_leaves_input)
        layout.addWidget(self.train_button)
        layout.addWidget(self.load_csv_button)
        layout.addWidget(self.predict_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.table_label)
        layout.addWidget(self.csv_table)

        self.setLayout(layout)

        self.train_data = {'age': [], 'height': [], 'weight': [], 'root_radius': [], 'num_leaves': []}


        self.train_button.clicked.connect(self.add_training_data)
        self.load_csv_button.clicked.connect(self.load_data_from_csv)
        self.predict_button.clicked.connect(self.train_and_predict)

        self.setGeometry(300, 300, 600, 400)  #ส่วนกำหนดขนาด
        self.setWindowTitle('ทำนายต้นไม้')     #ส่วนกำหนดหัวชื่อ
        self.show()

    def add_training_data(self):  #ส่วนฟังชั่นการเทรนข้อมูล
        try:
            age = float(self.age_input.text())
            height = float(self.height_input.text())
            weight = float(self.weight_input.text())
            root_radius = float(self.root_radius_input.text())
            num_leaves = float(self.num_leaves_input.text())

            self.train_data['age'].append(age)
            self.train_data['height'].append(height)
            self.train_data['weight'].append(weight)           
            self.train_data['root_radius'].append(root_radius)
            self.train_data['num_leaves'].append(num_leaves)

           


            self.age_input.clear()
            self.height_input.clear()
            self.weight_input.clear()                 #ส่วนลบข้อมูลในช่องรับข้อมูล
            self.root_radius_input.clear()
            self.num_leaves_input.clear()

            self.result_label.setText('ข้อมูลถูกเพิ่มเข้าสู่ข้อมูลฝึกฝน')  

            # เพิ่มข้อมูลใน QTableWidget ทันทีที่ข้อมูลถูกเพิ่ม
            self.add_data_to_table(age, height, weight, root_radius, num_leaves)

        except ValueError:
            self.result_label.setText('กรุณาใส่ค่าอายุและความสูงให้ถูกต้อง')

    def load_data_from_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "เลือกไฟล์ CSV", "", "CSV Files (*.csv);;All Files (*)", options=options) #ส่วนOpenFileName

        if file_name:
            try:
                df = pd.read_csv(file_name)
                self.train_data['age'] += df['อายุ'].tolist()
                self.train_data['height'] += df['ความสูง'].tolist()

                self.result_label.setText('ข้อมูลถูกโหลดจากไฟล์ CSV')

                # แสดงข้อมูลจาก CSV ใน QTableWidget
                self.show_data_in_table(df)

            except Exception as e:
                self.result_label.setText(f'เกิดข้อผิดพลาดในการโหลดไฟล์ CSV: {str(e)}')

    def show_data_in_table(self, df):
        self.csv_table.setRowCount(df.shape[0])
        self.csv_table.setColumnCount(df.shape[1])
        self.csv_table.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.csv_table.setItem(i, j, item)

    def add_data_to_table(self, age, height, weight, root_radius, num_leaves):  #ฟังชั่นเเสดงตาราง
        row_position = self.csv_table.rowCount()
        self.csv_table.insertRow(row_position)

        age_item = QTableWidgetItem(str(age))
        height_item = QTableWidgetItem(str(height))
        weight_item = QTableWidgetItem(str(weight))
        root_radius_item = QTableWidgetItem(str(root_radius))   
        num_leaves_item = QTableWidgetItem(str(num_leaves))

        self.csv_table.setItem(row_position, 0, age_item)
        self.csv_table.setItem(row_position, 1, height_item)
        self.csv_table.setItem(row_position, 2, weight_item)  # ส่วนการเรียงลำดับ
        self.csv_table.setItem(row_position, 3, root_radius_item)
        self.csv_table.setItem(row_position, 4, num_leaves_item)
        
    def train_and_predict(self):
        try:
            X = np.array(self.train_data['age']).reshape(-1, 1)
            y = np.array(self.train_data['height'])

            model = LinearRegression()
            model.fit(X, y)

            age_to_predict = float(self.age_input.text())
            height_prediction = model.predict([[age_to_predict]])

            self.result_label.setText(f'คาดการณ์ความสูง: {height_prediction[0]:.2f} เมตร')

        except ValueError:
            self.result_label.setText('กรุณาใส่ค่าอายุให้ถูกต้อง')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TreeHeightPredictionApp()
    sys.exit(app.exec_())
