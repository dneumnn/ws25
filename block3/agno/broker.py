from dataclasses import dataclass

@dataclass
class Order:
    symbol: str
    amount: int
    action: str
    id: str = None
    timestamp: int = 0
    limit: float = 0.0
    price: float = 0.0

def sent_order_to_broker(order: Order) -> bool:
    """Sent order to brooker.
        To sent an orderto the broker the following infomation must be set:
        - symbol  stock symbol
        - amount  number of stocks to be processed
        - action  buy or sell
    
    """
    order_sent = False
    try:
        # do something with the order
        order_sent = True
        
    except Exception as e:
        # log exception
        order_sent = False

    return order_sent