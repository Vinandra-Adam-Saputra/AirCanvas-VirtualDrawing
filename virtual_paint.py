import cv2
import numpy as np
import mediapipe as mp
from collections import deque

class VirtualDrawing:
    def __init__(self):
        # Inisialisasi MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Inisialisasi warna dan tools
        self.colors = {
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'red': (0, 0, 255),
            'yellow': (0, 255, 255)
        }
        self.current_color = self.colors['blue']
        self.brush_size = 5
        
        # Untuk menyimpan titik-titik gambar
        self.points = deque(maxlen=512)
        
        # Canvas untuk menggambar
        self.canvas = None
        
        # Status menggambar
        self.drawing_mode = False
        
    def check_finger_up(self, hand_landmarks):
        # Mendapatkan koordinat y dari titik-titik penting pada jari telunjuk
        tip = hand_landmarks.landmark[8].y  # Ujung jari telunjuk
        dip = hand_landmarks.landmark[7].y  # Sendi kedua dari ujung
        pip = hand_landmarks.landmark[6].y  # Sendi pertama dari ujung
        mcp = hand_landmarks.landmark[5].y  # Pangkal jari
        
        # Mendapatkan koordinat y dari titik-titik penting pada jari tengah
        middle_tip = hand_landmarks.landmark[12].y
        middle_dip = hand_landmarks.landmark[11].y
        
        # Jari telunjuk dianggap terangkat jika ujungnya lebih tinggi (y lebih kecil)
        # dari sendi-sendi di bawahnya
        index_up = tip < dip < pip < mcp
        
        # Jari tengah dianggap tertekuk jika ujungnya lebih rendah dari sendi di bawahnya
        middle_down = middle_tip > middle_dip
        
        # Mode menggambar aktif jika jari telunjuk terangkat dan jari tengah tertekuk
        return index_up and middle_down
        
    def run(self):
        cap = cv2.VideoCapture(0)
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue
                
            # Flip frame horizontal
            frame = cv2.flip(frame, 1)
            
            # Inisialisasi canvas jika belum
            if self.canvas is None:
                self.canvas = np.zeros(frame.shape, dtype=np.uint8)
            
            # Konversi frame ke RGB untuk MediaPipe
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)
            
            # Reset drawing mode di setiap frame
            self.drawing_mode = False
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Gambar landmarks tangan
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Cek apakah jari dalam posisi menggambar
                    self.drawing_mode = self.check_finger_up(hand_landmarks)
                    
                    # Dapatkan posisi telunjuk
                    index_tip = hand_landmarks.landmark[8]
                    h, w, _ = frame.shape
                    x, y = int(index_tip.x * w), int(index_tip.y * h)
                    
                    # Tambahkan point ke deque hanya jika dalam mode menggambar
                    if self.drawing_mode:
                        self.points.appendleft((x, y))
                    else:
                        self.points.appendleft(None)  # Tambahkan None untuk memutus garis
            
            # Gambar dari points yang tersimpan
            for i in range(1, len(self.points)):
                if self.points[i - 1] is None or self.points[i] is None:
                    continue
                    
                # Gambar garis antara points
                cv2.line(
                    frame,
                    self.points[i - 1],
                    self.points[i],
                    self.current_color,
                    self.brush_size
                )
                cv2.line(
                    self.canvas,
                    self.points[i - 1],
                    self.points[i],
                    self.current_color,
                    self.brush_size
                )
            
            # Tambahkan UI elements
            self._add_ui(frame)
            
            # Tampilkan status menggambar
            status = "Drawing Mode: ON" if self.drawing_mode else "Drawing Mode: OFF"
            cv2.putText(frame, status, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (255, 255, 255), 2)
            
            # Gabungkan frame dengan canvas
            result = cv2.addWeighted(frame, 1, self.canvas, 0.5, 0)
            cv2.imshow('Virtual Drawing', result)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                self.canvas = None
                self.points = deque(maxlen=512)
            elif key == ord('b'):
                self.current_color = self.colors['blue']
            elif key == ord('g'):
                self.current_color = self.colors['green']
            elif key == ord('r'):
                self.current_color = self.colors['red']
            elif key == ord('y'):
                self.current_color = self.colors['yellow']
            elif key == ord('+'):
                self.brush_size = min(self.brush_size + 1, 20)
            elif key == ord('-'):
                self.brush_size = max(self.brush_size - 1, 1)
        
        cap.release()
        cv2.destroyAllWindows()
    
    def _add_ui(self, frame):
        # Tambahkan informasi kontrol
        cv2.putText(frame, f"Brush Size: {self.brush_size}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Color palette
        colors_y = 90
        for i, (name, color) in enumerate(self.colors.items()):
            cv2.circle(frame, (30 + i*30, colors_y), 10, color, -1)
            if color == self.current_color:
                cv2.circle(frame, (30 + i*30, colors_y), 12, (255, 255, 255), 2)

if __name__ == "__main__":
    app = VirtualDrawing()
    app.run()