from channels.generic.websocket import AsyncJsonWebsocketConsumer
from utils.scanner import find_device, get_product_by_barcode, listen_device
from asgiref.sync import sync_to_async
import serial
import asyncio

class PointOfSale(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scanner_active = False
        self.scanner_task = None

    async def connect(self):
        await self.channel_layer.group_add("pos_principal", self.channel_name)
        await self.accept()
        async def _send_code(code):
            producto = await sync_to_async(get_product_by_barcode)(code)
            await self.send_json(producto)
        self.scanner_active = True
        self.scanner_task = asyncio.create_task(
            listen_device(self, _send_code)
        )

    async def disconnect(self, close_code):
        self.scanner_active = False
        if self.scanner_task:
            self.scanner_task.cancel()
            try:
                await self.scanner_task
            except asyncio.CancelledError:
                pass
        await self.channel_layer.group_discard(
            "pos_principal",
            self.channel_name
        )

class BCScaning(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scanner_active = False
        self.scanner_task = None

    async def connect(self):
        await self.channel_layer.group_add("scan", self.channel_name)
        await self.accept()
        async def _send_code(code):
            await self.send_json(code)
        self.scanner_active = True
        self.scanner_task = asyncio.create_task(
            listen_device(self, _send_code)
        )

    async def disconnect(self, close_code):
        self.scanner_active = False
        if self.scanner_task:
            self.scanner_task.cancel()
            try:
                await self.scanner_task
            except asyncio.CancelledError:
                pass
        await self.channel_layer.group_discard(
            "scan",
            self.channel_name
        )
