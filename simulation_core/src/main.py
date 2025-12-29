import time
import random
from node import EnergyNode
from grid_manager import GridManager

def main():
    print("⚡ Energy-Grid-Pulse Simülasyonu Başlatılıyor... ⚡")
    print("-" * 50)

    # 1. Grid Yöneticisini Başlat
    grid = GridManager()
    print("[SİSTEM] GridManager aktif. Hedef Frekans: 50.0 Hz")

    # 2. Düğümleri Oluştur ve Ekle
    print("[SİSTEM] Düğümler (Nodes) şebekeye bağlanıyor...")
    
    # Üreticiler (Güneş Enerjisi, Rüzgar vb.)
    producers = [
        EnergyNode(node_id=f"Gen_{i}", node_type="URETICI", capacity=100.0) 
        for i in range(3)
    ]
    
    # Tüketiciler (Evler, Sanayi)
    consumers = [
        EnergyNode(node_id=f"Cons_{i}", node_type="TUKETICI", capacity=50.0)
        for i in range(5)
    ]

    # Prosumers (Hem üreten hem tüketenler - örn. Bataryalı Evler)
    prosumers = [
        EnergyNode(node_id=f"Pro_{i}", node_type="URETUKETICI", capacity=75.0)
        for i in range(2)
    ]

    all_nodes = producers + consumers + prosumers
    for node in all_nodes:
        # Başlangıç durumu için rastgele yük/üretim ata
        if node.node_type == "URETICI":
            node.current_generation = random.uniform(50, 100)
        elif node.node_type == "TUKETICI":
            node.current_load = random.uniform(20, 50)
        grid.add_node(node)

    print(f"[SİSTEM] Toplam {len(all_nodes)} düğüm bağlandı.")
    print("-" * 50)
    time.sleep(1)

    # 3. Simülasyon Döngüsü
    tick_count = 0
    try:
        while True:
            tick_count += 1
            
            # Her düğüm bir "adım" atar (durumunu günceller)
            for node in grid.nodes:
                node.tick()
            
            # Grid analizi yap
            status = grid.analyze_stability()
            
            # Durumu görselleştir
            freq = status['frekans']
            balance_str = "DENGELİ" if status['durum'] == "STABIL" else "!!! DENGESİZLİK !!!"
            
            # Görsel Frekans Çubuğu
            bar_len = int((freq - 49.0) * 10)  # Basit görselleştirme
            bar = "|" * bar_len
            
            print(f"Adım {tick_count:03} | Frekans: {freq:.4f} Hz | {bar} | {balance_str}")
            print(f"   >>> Üretim: {status['toplam_uretim']:.2f} kW | Yük: {status['toplam_yuk']:.2f} kW")
            
            # Kritik durum uyarısı
            if status['durum'] == "KRITIK":
                print("   ⚠️  UYARI: Şebeke kararlılığı risk altında! Müdahale ediliyor...")
            
            print("-" * 20)
            time.sleep(2.0) # Okunabilirlik için bekle

    except KeyboardInterrupt:
        print("\n🛑 Simülasyon kullanıcı tarafından durduruldu.")

if __name__ == "__main__":
    main()
