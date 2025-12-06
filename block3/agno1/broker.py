from dataclasses import dataclass
import logging
import logging.handlers
import os
 
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "./broker.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)
 


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
    
        If the user wants to limit the price with a price limit then use limit as variable. 
    """
    logging.info("sent order with %s",order)
    order_sent = False
    try:
        # do something with the order
        order_sent = True
        
    except Exception as e:
        # log exception
        order_sent = False

    return order_sent