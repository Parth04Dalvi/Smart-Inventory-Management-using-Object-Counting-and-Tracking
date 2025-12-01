import time
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

# --- Project Configuration ---
# Simulation parameters for inventory items
INVENTORY_ITEMS = {
    1: {"name": "Laptop Box", "min_stock": 2, "current_stock": 5},
    2: {"name": "Accessory Kit", "min_stock": 5, "current_stock": 10},
    3: {"name": "Monitor Stand", "min_stock": 1, "current_stock": 3},
}
# Simulated list of recognized object IDs in the current frame
SIMULATED_DETECTED_IDS = list(INVENTORY_ITEMS.keys()) * 2 # Start with more stock

# --- Database Simulation (In-Memory) ---
class InventoryItem(BaseModel):
    id: int
    name: str
    min_stock: int
    current_stock: int
    alert_status: str # "OK", "LOW", "CRITICAL"

class Transaction(BaseModel):
    item_id: int
    item_name: str
    timestamp: str
    action: str # "ADDED", "REMOVED"
    quantity_change: int

# In-memory store for inventory state and transactions
inventory_db: Dict[int, InventoryItem] = {
    item_id: InventoryItem(id=item_id, **data, alert_status="OK")
    for item_id, data in INVENTORY_ITEMS.items()
}
transaction_history: List[Transaction] = []

# --- Core Tracking and Logic (SIMULATED) ---

def process_vision_frame():
    """
    Simulates the core YOLOv8 + DeepSORT tracking logic.
    In a real application, this function would:
    1. Read video frame.
    2. Run YOLOv8 detection.
    3. Run DeepSORT tracking to assign persistent IDs.
    4. Calculate stock change based on new vs. previous frame tracked IDs.
    """
    global inventory_db
    # 1. Simulate a random stock transaction (ADD or REMOVE)
    target_id = random.choice(SIMULATED_DETECTED_IDS)
    
    # 2. Decide on action
    action = random.choice(["ADD", "REMOVE", "NONE"]) 
    
    if action != "NONE" and random.random() < 0.3: # ~30% chance of a transaction
        item = inventory_db[target_id]
        
        # Calculate change (always change by 1 for simplicity)
        change = 1 if action == "ADD" else -1
        
        # Prevent stock from going negative in simulation
        if action == "REMOVE" and item.current_stock <= 0:
            change = 0
            action = "NONE"

        if change != 0:
            # 3. Update Inventory
            item.current_stock += change
            
            # 4. Check for Alerts
            new_status = "OK"
            if item.current_stock <= item.min_stock:
                new_status = "LOW"
            if item.current_stock == 0:
                new_status = "CRITICAL"
            
            item.alert_status = new_status
            
            # 5. Record Transaction
            transaction_history.append(Transaction(
                item_id=item.id,
                item_name=item.name,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                action=action + "ED",
                quantity_change=change
            ))
            
            print(f"[{item.name}] Stock changed by {change}. New Count: {item.current_stock}. Status: {item.alert_status}")


# --- FastAPI Application ---
app = FastAPI(
    title="Smart Inventory API",
    description="Backend for real-time inventory tracking, leveraging Computer Vision data."
)

@app.get("/inventory/status", response_model=List[InventoryItem])
async def get_inventory_status():
    """Returns the current stock level and alert status for all tracked items."""
    # Simulate processing a new frame before returning status
    process_vision_frame() 
    return list(inventory_db.values())

@app.get("/inventory/transactions", response_model=List[Transaction])
async def get_transaction_history():
    """Returns the last 10 inventory transactions."""
    return transaction_history[-10:]

# Simple root for health check
@app.get("/")
async def root():
    return {"message": "Smart Inventory API running. Access /docs for endpoints."}

# The simulation needs to be run continuously, which is not possible in this single-file setup.
# In a real environment, the vision script would run separately, updating a persistent database
# which this API would read from. The 'process_vision_frame' call within the endpoint
# is a necessary hack to demonstrate the real-time update logic.
