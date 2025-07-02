from products.models import Product
from stock.models import ProductStock
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async

import serial
import websockets
import asyncio

from serial.tools import list_ports

def find_device(vid, pid):
    """Return a scanner device or none."""
    for port in list_ports.comports():
        if port.vid == vid and port.pid == pid:
            print(f"Dispositivo escaner encontrado: {port.device} - {port.description}")
            return port.device
    print("No se encontro ningún dispositivo conectado.")
    return None

def get_product_by_barcode(bar_code):
    try:
        product = Product.objects.get(bar_code=bar_code)
        try:
            pstock = ProductStock.objects.get(product=product)
            return {
                'status': 'success',
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.sell_price,
                    'stock': pstock.stock,
                    'stock_id': pstock.id
                }
            }
    
        except ObjectDoesNotExist:
            return {
                'status': 'error',
                'message': 'Producto sin seguimiento de inventario'
            }
        
    except ObjectDoesNotExist:
        return {
            'status': 'error',
            'message': 'Producto no encontrado'
        }
    

async def listen_device(self, callback):
        print("Iniciando escucha del dispositivo...")
        device = find_device(0x0483, 0x5740)
        if not device:
            return {"error": "Dispositivo no encontrado"}

        try:
            def sync_serial_read():
                with serial.Serial(device, 9600, timeout=1) as escaner:
                    bar_code = ""
                    while self.scanner_active:
                        byte = escaner.read()
                        if byte:
                            bar_code += byte.decode(errors='ignore')
                            if bar_code.endswith("\r"):
                                bar_code = bar_code.strip("\r")
                                response = bar_code
                                bar_code = ""
                                return response
                        elif byte == b"":
                            return None

            while self.scanner_active:
                code = await asyncio.to_thread(sync_serial_read)
                if code:
                    await callback(code)
                await asyncio.sleep(0.01)  # Pequeña pausa asíncrona

        except Exception as e:
            print(f"[Error]: {e}")
            return {"error": e}
