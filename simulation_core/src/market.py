class EnergyMarket:
    """
    P2P ticaret oturumlarını yönetir.
    """
    def __init__(self):
        self.bids = []  # Alıcılar (Bids)
        self.asks = []  # Satıcılar (Asks)
        self.clearing_price = 0.0

    def submit_bid(self, node_id, amount, max_price):
        """Alış teklifi sun"""
        self.bids.append({'node_id': node_id, 'amount': amount, 'price': max_price})

    def submit_ask(self, node_id, amount, min_price):
        """Satış teklifi sun"""
        self.asks.append({'node_id': node_id, 'amount': amount, 'price': min_price})

    def match(self):
        """
        Basit takas motoru.
        Alışları azalan, satışları artan fiyata göre sıralar.
        Kesişimi bulur.
        """
        # Sırala
        self.bids.sort(key=lambda x: x['price'], reverse=True)
        self.asks.sort(key=lambda x: x['price'], reverse=False)

        transactions = []
        
        # Gösterim için naif eşleştirme
        while self.bids and self.asks:
            best_bid = self.bids[0]
            best_ask = self.asks[0]

            if best_bid['price'] >= best_ask['price']:
                # EŞLEŞME! (MATCH)
                price = (best_bid['price'] + best_ask['price']) / 2
                amount = min(best_bid['amount'], best_ask['amount'])
                
                transactions.append({
                    "alici": best_bid['node_id'],
                    "satici": best_ask['node_id'],
                    "miktar": amount,
                    "fiyat": price
                })
                
                # Güncelle/Kaldır
                if best_bid['amount'] > amount:
                    best_bid['amount'] -= amount
                    self.asks.pop(0) # Satış tamamen doldu
                elif best_ask['amount'] > amount:
                    best_ask['amount'] -= amount
                    self.bids.pop(0) # Alış tamamen doldu
                else:
                    self.bids.pop(0)
                    self.asks.pop(0)
            else:
                break
        
        return transactions
