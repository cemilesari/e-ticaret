import string
import random

def randomString(stringLength=4):
    import string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength)).upper()

def generate_password(stringLength=16):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(stringLength))

def generate_order_name():
    from main.buy_sell.models import Order
    tik = "KUID-{}-{}".format(random.randint(1547,9999), randomString(stringLength=6))
    notfound = True
    while notfound:
        try:
            g = Order.objects.get(title=str(tik))
        except Order.DoesNotExist:
            notfound = False
    return str(tik)

def generate_ticket_name():
    from main.tickets.models import Ticket
    tik = "TK-{}-{}".format(random.randint(1547,9999), randomString())
    notfound = True
    while notfound:
        try:
            g = Ticket.objects.get(ticket_name=str(tik))
        except Ticket.DoesNotExist:
            notfound = False
    return str(tik)