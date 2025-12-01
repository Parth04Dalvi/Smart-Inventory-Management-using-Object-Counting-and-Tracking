import time
import random
import json
from typing import Dict, List, Optional

# --- Configuration and Data Structure Definitions ---

# In a real application, this state would be fetched from and written to a persistent DB (e.g., PostgreSQL).
# For this demonstration, we'll use a JSON file simulation.
INVENTORY_FILE = "inventory_state.json" 
# How often the vision processor should update the inventory (simulate frame processing speed)
PROCESSING_INTERVAL_SECONDS = 1 

# Initial configuration of items and their stock/min_stock
INITIAL_INVENTORY_CONFIG = {
    1: {"name": "Laptop Box", "min_stock": 2, "current_stock": 5},
    2: {"name": "Accessory Kit", "min_stock": 5, "current_stock": 10},
    3: {"name": "Monitor Stand", "min_stock": 1, "current_stock": 3},
}

# Define the data structure for type hinting and clarity
InventoryState = Dict[int, Dict]
Transaction = Dict[str, str]

# --- Simulated Database Interaction Functions ---

def load_inventory_state() -> InventoryState:
    """Loads the current inventory state from a simulated JSON file."""
    try:
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[{INVENTORY_FILE}] not found. Initializing with default config.")
        return {
            id: {**data, "alert_status": "OK"} 
            for id, data in INITIAL_INVENTORY_CONFIG.items()
        }
    except json.JSONDecodeError:
        print(f"Error decoding [{INVENTORY_FILE}]. Initializing with default config.")
        return {
            id: {**data, "alert_status": "OK"} 
            for id, data in INITIAL_INVENTORY_CONFIG.items()
        }

def save_inventory_state(state: InventoryState):
    """Saves the current inventory state to the simulated JSON file."""
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(state, f, indent=4)

# Note: In a real environment, transaction history would be appended to a separate 
# collection/table in the database, but we skip that file interaction for simplicity here.

# --- Core Vision Simulation Logic ---

def generate_simulated_tracked_objects(current_state: InventoryState) -> List[int]:
    """
    Simulates the output of the DeepSORT tracker.
    Returns a list of IDs currently seen on the shelf.
    """
    
    # 1. Determine what IDs should be 'present' based on current stock
    present_ids = []
    for item_id, data in current_state.items():
        # Represent stock count by a list of that many IDs (simulating distinct boxes/items)
        present_ids.extend([item_id] * data["current_stock"])

    # 2. Simulate random real-world movement/change (The core business logic)
    
    # Simulate a "change" event (ADD or REMOVE) happening 30% of the time
    if random.random() < 0.3:
        action = random.choice(["ADD", "REMOVE"])
        target_id = random.choice(list(current_state.keys())) # Which item is affected

        if action == "ADD":
            # Simulate a new item appearing in the frame
            # Add one instance of the item ID to the 'present' list
            present_ids.append(target_id)
            print(f"[Sim] Simulating: Item {target_id} ({current_state[target_id]['name']}) was added.")
        
        elif action == "REMOVE" and target_id in present_ids:
            # Simulate an item being taken off the shelf
            # Remove one instance of the item ID from the 'present' list
            present_ids.remove(target_id)
            print(f"[Sim] Simulating: Item {target_id} ({current_state[target_id]['name']}) was removed.")
            
    # The 'present_ids' list represents the new detected count.
    return present_ids

def process_frame_update(current_state: InventoryState, tracked_ids: List[int]) -> (InventoryState, Optional[Transaction]):
    """
    Compares the newly tracked IDs against the current state to determine stock change.
    """
    new_state = {id: data.copy() for id, data in current_state.items()}
    transaction = None
    
    # Count the new occurrences of each ID
    new_counts = {item_id: tracked_ids.count(item_id) for item_id in new_state.keys()}

    for item_id, item_data in new_state.items():
        old_count = item_data["current_stock"]
        new_count = new_counts.get(item_id, 0) # Should always be present, but safer
        
        if new_count != old_count:
            change = new_count - old_count
            
            # 1. Update Inventory State
            item_data["current_stock"] = new_count
            
            # 2. Check for Alerts
            new_status = "OK"
            if item_data["current_stock"] <= item_data["min_stock"]:
                new_status = "LOW"
            if item_data["current_stock"] == 0:
                new_status = "CRITICAL"
            
            item_data["alert_status"] = new_status
            
            # 3. Record Transaction (Only record the first change per frame for simplicity)
            if transaction is None:
                action = "ADDED" if change > 0 else "REMOVED"
                transaction = {
                    "item_id": str(item_id), # Use string for JSON/API compatibility
                    "item_name": item_data["name"],
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "action": action,
                    "quantity_change": abs(change)
                }
                
            print(f"[{item_data['name']}] Stock changed by {change}. New Count: {item_data['current_stock']}. Status: {item_data['alert_status']}")

    return new_state, transaction

# --- Main Application Loop ---

def vision_processor_main():
    """
    The main loop that continuously processes video frames and updates the inventory.
    """
    print("--- Smart Inventory Vision Processor Started ---")
    print(f"Reading and writing inventory state to: {INVENTORY_FILE}")
    
    while True:
        try:
            # 1. Load the current state from the 'database'
            current_state = load_inventory_state()
            
            # 2. Run the detection and tracking simulation (YOLOv8 + DeepSORT)
            # This generates the list of object IDs seen in the current 'frame'
            tracked_ids = generate_simulated_tracked_objects(current_state)
            
            # 3. Process the results and determine changes
            new_state, transaction = process_frame_update(current_state, tracked_ids)
            
            # 4. Persist the updated state (and transactions, if using a real DB)
            save_inventory_state(new_state)
            
            # Print transaction to console (optional logging)
            if transaction:
                print(f"Transaction recorded: {transaction}")
            
            # 5. Wait for the next frame
            time.sleep(PROCESSING_INTERVAL_SECONDS)
            
        except KeyboardInterrupt:
            print("\nProcessor stopped by user.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Retrying in 5 seconds.")
            time.sleep(5)

# Example command to run the script: python vision_processor.py
# if __name__ == "__main__":
#     vision_processor_main()

# NOTE: The actual execution line is commented out as the environment runs the FastAPI app.
# The core logic is preserved and highly commented to demonstrate the intended flow.
