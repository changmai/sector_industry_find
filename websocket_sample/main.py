import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt

# 분리한 파일들 불러오기
from data_worker import WebSocketWorker, TARGET_CODE
from ui_widgets import FootprintTable, TickListTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"LS증권 Footprint Pro - {TARGET_CODE}")
        self.resize(1200, 900)
        self.setStyleSheet("background-color: #2b2b2b;")

        self.init_ui()
        self.start_worker()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # === [좌측] Footprint ===
        left_layout = QVBoxLayout()
        left_label = QLabel("📊 Price Footprint (누적)")
        left_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        left_layout.addWidget(left_label)

        # ui_widgets.py에서 만든 클래스 사용
        self.fp_table = FootprintTable()
        left_layout.addWidget(self.fp_table)

        # === [우측] Realtime Ticks ===
        right_layout = QVBoxLayout()
        right_label = QLabel("⚡ Realtime Ticks (실시간)")
        right_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        right_layout.addWidget(right_label)

        # ui_widgets.py에서 만든 클래스 사용
        self.tick_table = TickListTable()
        right_layout.addWidget(self.tick_table)

        # 레이아웃 배치 (6:4)
        main_layout.addLayout(left_layout, 60)
        main_layout.addLayout(right_layout, 40)

        # 하단 상태바
        self.status_label = QLabel("시스템 준비 완료")
        self.status_label.setStyleSheet("color: #00ff00; padding: 5px; background-color: #222;")
        self.statusBar().addWidget(self.status_label)

    def start_worker(self):
        # data_worker.py의 워커 실행
        self.worker = WebSocketWorker()
        self.worker.data_signal.connect(self.on_data_received)
        self.worker.log_signal.connect(self.on_log_received)
        self.worker.start()

    def on_log_received(self, msg):
        self.status_label.setText(msg)
        print(msg)

    def on_data_received(self, body):
        """데이터를 받아서 좌/우 테이블로 분배"""
        try:
            # 공통 파싱
            price = int(str(body.get("price", "0")).strip())
            vol = int(str(body.get("cvolume", "0")).strip())
            gubun = body.get("cgubun", "").strip()
            raw_time = body.get('chetime', '')

            if price == 0: return

            is_buy = (gubun == "+" or str(gubun) == "1")
            time_str = f"{raw_time[:2]}:{raw_time[2:4]}:{raw_time[4:]}" if len(raw_time) == 6 else raw_time

            # 1. 좌측 테이블 업데이트 (누적 로직은 저쪽 클래스 안에 있음)
            self.fp_table.update_data(price, vol, is_buy)

            # 2. 우측 테이블 업데이트 (리스트 추가 로직은 저쪽 클래스 안에 있음)
            self.tick_table.add_tick(time_str, price, vol, is_buy)

            # 상태바 업데이트
            side_str = "🔴매수" if is_buy else "🔵매도"
            self.status_label.setText(f"[수신] {time_str} | {price:,}원 | {side_str} {vol:,}주")

        except Exception as e:
            print(f"Main Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())