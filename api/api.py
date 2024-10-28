import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import asyncio
import random
from typing import Dict, List
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class Order(BaseModel):
    id: int
    status: str


orders: Dict[int, Order] = {}
active_connections: List[WebSocket] = []


async def notify_clients(order_id: int, status: str):
    for connection in active_connections:
        await connection.send_json({"orderId": order_id, "status": status})

@app.get("/test_results", response_class=HTMLResponse)
async def read_root():
    files = os.listdir('static')
    file_list_html = "<ul>" + "".join(f'<li><a href="static/{file}">{file}</a></li>' for file in files) + "</ul>"
    return HTMLResponse(content=file_list_html)

@app.get("/orders")
async def get_all_orders():
    await asyncio.sleep(random.uniform(0.1, 1))
    return list(orders.values())

@app.post("/orders")
async def create_order():
    order_id = len(orders) + 1
    order = Order(id=order_id, status="PENDING")
    orders[order_id] = order
    await notify_clients(order_id, order.status)

    await asyncio.sleep(random.uniform(3, 6))
    # CHANGE TO
    order.status = "EXECUTED"
    await notify_clients(order_id, order.status)

    return {"orderId": order_id, "status": order.status}


@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    await asyncio.sleep(random.uniform(0.1, 1))
    return orders.get(order_id)


@app.delete("/orders/{order_id}", status_code=204)
async def cancel_order(order_id: int):
    order = orders.get(order_id)
    if order:
        if order.status == "PENDING":
            order.status = "CANCELED"
            await notify_clients(order_id, order.status)
            return {}
        else:
            return {"error": "Order already completed"}
    return {"error": "Order not found"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
