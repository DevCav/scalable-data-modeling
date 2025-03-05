import pandas as pd
import json
import os

# Define input and output file paths
input_file = "raw_json/receipts.json"  # Replace with your actual JSON file
output_file = "seeds/receipt_items.csv"  # Output file location

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# List to hold flattened records
expanded_data = []

# Function to convert MongoDB-style timestamps
def convert_mongo_date(mongo_date):
    """Convert MongoDB-style date fields to datetime format."""
    if isinstance(mongo_date, dict) and "$date" in mongo_date:
        return pd.to_datetime(mongo_date["$date"], unit="ms")  # Convert from milliseconds
    return mongo_date

# Open file and read each line as a separate JSON object
with open(input_file, "r") as file:
    for line in file:
        try:
            receipt = json.loads(line.strip())  # Read each JSON object separately

            base_data = {
                "receipt_uuid": receipt.get("userId"),  # Assuming userId is the receipt ID
                "points_earned": float(receipt.get("pointsEarned", 0)),
                "purchase_date": convert_mongo_date(receipt.get("purchaseDate")),
                "purchased_item_count": receipt.get("purchasedItemCount", 0),
                "rewards_receipt_status": receipt.get("rewardsReceiptStatus"),
                "total_spent": float(receipt.get("totalSpent", 0)),
                "user_id": receipt.get("userId")
            }

            # If there are items in the rewardsReceiptItemList, expand them
            if "rewardsReceiptItemList" in receipt and isinstance(receipt["rewardsReceiptItemList"], list):
                for item in receipt["rewardsReceiptItemList"]:
                    expanded_row = base_data.copy()  # Copy base receipt details
                    expanded_row.update({
                        "barcode": item.get("barcode"),
                        "description": item.get("description"),
                        "final_price": float(item.get("finalPrice", 0)),
                        "item_price": float(item.get("itemPrice", 0)),
                        "needs_fetch_review": item.get("needsFetchReview", False),
                        "partner_item_id": item.get("partnerItemId"),
                        "prevent_target_gap_points": item.get("preventTargetGapPoints", False),
                        "quantity_purchased": item.get("quantityPurchased", 1),
                        "user_flagged_barcode": item.get("userFlaggedBarcode"),
                        "user_flagged_new_item": item.get("userFlaggedNewItem", False),
                        "user_flagged_price": float(item.get("userFlaggedPrice", 0)),
                        "user_flagged_quantity": item.get("userFlaggedQuantity", 1)
                    })
                    expanded_data.append(expanded_row)  # Add row for each item
            else:
                # No items, still include the receipt-level row
                expanded_data.append(base_data)

        except json.JSONDecodeError as e:
            print(f"Skipping invalid JSON line: {e}")

# Convert to DataFrame
df = pd.DataFrame(expanded_data)

# Save to CSV
df.to_csv(output_file, index=False)

print(f"✅ Expanded JSON data saved to: {output_file}")
