import numpy as np

class EnergyNode:
    """
    Şebekedeki tek bir varlığı temsil eder (Ev, Güneş Santrali, Batarya, vb.).
    """
    def __init__(self, node_id, node_type, capacity=0.0):
        self.node_id = node_id
        self.node_type = node_type  # 'URETICI', 'TUKETICI', 'URETUKETICI' (PROSUMER)
        self.capacity = capacity
        self.current_load = 0.0        # Mevcut Yük
        self.current_generation = 0.0  # Mevcut Üretim
        self.battery_level = 0.0       # Batarya Seviyesi

    def tick(self):
        """
        Simülasyon adımı. Dahili durumu günceller (üretim/yük).
        Rastgele yürüyüş (randomwalk) kullanan yer tutucu mantık.
        """
        if self.node_type == 'URETICI':
            self.current_generation = max(0, self.current_generation + np.random.normal(0, 0.1))
        elif self.node_type == 'TUKETICI':
            self.current_load = max(0, self.current_load + np.random.normal(0, 0.1))
        
        # Net Pozisyon Hesapla (pozitif = fazla/satış, negatif = açık/alış)
        return self.current_generation - self.current_load

    def __repr__(self):
        return f"<Dugum {self.node_id}: {self.node_type} | Net: {self.current_generation - self.current_load:.2f}kW>"
