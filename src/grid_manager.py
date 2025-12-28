class GridManager:
    """
    Şebeke kararlılığını izleyen Merkezi veya Dağıtık varlık.
    """
    def __init__(self):
        self.nodes = []
        self.grid_frequency = 50.0  # Hz
    
    def add_node(self, node):
        self.nodes.append(node)

    def analyze_stability(self):
        """
        Toplam arzı toplam talebe karşı kontrol eder.
        Arz > Talep ise, frekans ARTAR.
        Arz < Talep ise, frekans AZALIR.
        """
        total_gen = sum(n.current_generation for n in self.nodes)
        total_load = sum(n.current_load for n in self.nodes)
        
        balance = total_gen - total_load
        
        # Basitleştirilmiş droop kontrol simülasyonu
        self.grid_frequency += balance * 0.01
        
        return {
            "toplam_uretim": total_gen,
            "toplam_yuk": total_load,
            "frekans": self.grid_frequency,
            "durum": "STABIL" if 49.5 < self.grid_frequency < 50.5 else "KRITIK"
        }
