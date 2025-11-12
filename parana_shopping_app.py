import sqlite3
from datetime import datetime
import sys

# Database connection
def create_connection():
    """Create a database connection to the SQLite database"""
    try:
        conn = sqlite3.connect('orinoco.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

# Display options function
def display_options(all_options, title, type):
    """Display a numbered list of options and return the selected option"""
    option_num = 1
    option_list = []
    print(f"\n{title}\n")
    for option in all_options:
        code = option[0]
        desc = option[1]
        print(f"{option_num}.\t{desc}")
        option_num = option_num + 1
        option_list.append(code)
    
    selected_option = 0
    while selected_option > len(option_list) or selected_option == 0:
        try:
            prompt = f"Enter the number against the {type} you want to choose: "
            selected_option = int(input(prompt))
            if selected_option > len(option_list) or selected_option <= 0:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
            selected_option = 0
    
    return option_list[selected_option - 1]

# Get current basket
def get_current_basket(conn, shopper_id):
    """Get or create current basket for the shopper"""
    cursor = conn.cursor()
    
    # Check for existing basket created today
    cursor.execute("""
        SELECT basket_id
        FROM shopper_baskets
        WHERE shopper_id = ?
        AND DATE(basket_created_date_time) = DATE('now')
        ORDER BY basket_created_date_time DESC
        LIMIT 1
    """, (shopper_id,))
    
    result = cursor.fetchone()
    if result:
        return result['basket_id']
    return None

# Option 1: Display order history
def display_order_history(conn, shopper_id):
    """Display order history for the shopper"""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT o.order_id, o.order_date, p.product_description, 
               s.seller_name, op.price, op.quantity, op.ordered_product_status
        FROM shopper_orders o
        JOIN ordered_products op ON o.order_id = op.order_id
        JOIN products p ON op.product_id = p.product_id
        JOIN sellers s ON op.seller_id = s.seller_id
        WHERE o.shopper_id = ?
        ORDER BY o.order_date DESC
    """, (shopper_id,))
    
    orders = cursor.fetchall()
    
    if not orders:
        print("\nNo orders placed by this customer")
        return
    
    print("\nYour Order History:")
    print("-" * 100)
    
    current_order_id = None
    for order in orders:
        if order['order_id'] != current_order_id:
            current_order_id = order['order_id']
            print(f"\nOrder ID: {order['order_id']} - Date: {order['order_date']}")
            print("-" * 80)
        
        print(f"  {order['product_description']}")
        print(f"  Seller: {order['seller_name']} | Price: £{order['price']:.2f} | "
              f"Quantity: {order['quantity']} | Status: {order['ordered_product_status']}")

# Option 2: Add item to basket
def add_item_to_basket(conn, shopper_id, basket_id):
    """Add an item to the shopper's basket"""
    cursor = conn.cursor()
    
    # Display categories
    cursor.execute("""
        SELECT category_id, category_description
        FROM categories
        ORDER BY category_description
    """)
    categories = cursor.fetchall()
    
    category_id = display_options(categories, "Product Categories", "category")
    
    # Display products in selected category
    cursor.execute("""
        SELECT product_id, product_description
        FROM products
        WHERE category_id = ?
        ORDER BY product_description
    """, (category_id,))
    products = cursor.fetchall()
    
    product_id = display_options(products, "Available Products", "product")
    
    # Display sellers for selected product
    cursor.execute("""
        SELECT ps.seller_id, s.seller_name || ' - £' || ps.price as seller_info
        FROM product_sellers ps
        JOIN sellers s ON ps.seller_id = s.seller_id
        WHERE ps.product_id = ?
        ORDER BY s.seller_name
    """, (product_id,))
    sellers = cursor.fetchall()
    
    seller_id = display_options(sellers, "Available Sellers", "seller")
    
    # Get quantity
    quantity = 0
    while quantity <= 0:
        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("The quantity must be greater than 0")
        except ValueError:
            print("Please enter a valid number")
            quantity = 0
    
    # Get price
    cursor.execute("""
        SELECT price
        FROM product_sellers
        WHERE product_id = ? AND seller_id = ?
    """, (product_id, seller_id))
    price = cursor.fetchone()['price']
    
    # Create basket if needed
    if basket_id is None:
        cursor.execute("""
            INSERT INTO shopper_baskets (shopper_id, basket_created_date_time)
            VALUES (?, datetime('now'))
        """, (shopper_id,))
        basket_id = cursor.lastrowid
    
    # Add item to basket
    cursor.execute("""
        INSERT INTO basket_contents (basket_id, product_id, seller_id, quantity, price)
        VALUES (?, ?, ?, ?, ?)
    """, (basket_id, product_id, seller_id, quantity, price))
    
    conn.commit()
    print("\nItem added to your basket")
    return basket_id

# Option 3: View basket
def view_basket(conn, basket_id):
    """Display the current basket contents"""
    if basket_id is None:
        print("\nYour basket is empty")
        return
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT bc.product_id, bc.seller_id, p.product_description, 
               s.seller_name, bc.quantity, bc.price,
               (bc.quantity * bc.price) as line_total
        FROM basket_contents bc
        JOIN products p ON bc.product_id = p.product_id
        JOIN sellers s ON bc.seller_id = s.seller_id
        WHERE bc.basket_id = ?
        ORDER BY p.product_description
    """, (basket_id,))
    
    items = cursor.fetchall()
    
    if not items:
        print("\nYour basket is empty")
        return
    
    print("\nYour Basket:")
    print("-" * 80)
    
    total = 0
    item_no = 1
    for item in items:
        print(f"{item_no}. {item['product_description']} from {item['seller_name']}")
        print(f"   Quantity: {item['quantity']} | Price: £{item['price']:.2f} | "
              f"Total: £{item['line_total']:.2f}")
        total += item['line_total']
        item_no += 1
    
    print("-" * 80)
    print(f"Total: £{total:.2f}")

# Option 4: Change quantity
def change_quantity(conn, basket_id):
    """Change the quantity of an item in the basket"""
    if basket_id is None:
        print("\nYour basket is empty")
        return
    
    cursor = conn.cursor()
    
    # Display basket first
    view_basket(conn, basket_id)
    
    # Get basket items
    cursor.execute("""
        SELECT product_id, seller_id
        FROM basket_contents
        WHERE basket_id = ?
    """, (basket_id,))
    items = cursor.fetchall()
    
    if not items:
        return
    
    # Get item to change
    if len(items) > 1:
        item_no = 0
        while item_no < 1 or item_no > len(items):
            try:
                item_no = int(input("\nEnter the basket item no. to update: "))
                if item_no < 1 or item_no > len(items):
                    print("The basket item no. you have entered is invalid")
            except ValueError:
                print("Please enter a valid number")
                item_no = 0
    else:
        item_no = 1
    
    # Get new quantity
    new_quantity = 0
    while new_quantity <= 0:
        try:
            new_quantity = int(input("Enter new quantity: "))
            if new_quantity <= 0:
                print("The quantity must be greater than 0")
        except ValueError:
            print("Please enter a valid number")
            new_quantity = 0
    
    # Update quantity
    item = items[item_no - 1]
    cursor.execute("""
        UPDATE basket_contents
        SET quantity = ?
        WHERE basket_id = ? AND product_id = ? AND seller_id = ?
    """, (new_quantity, basket_id, item['product_id'], item['seller_id']))
    
    conn.commit()
    print("\nQuantity updated")
    view_basket(conn, basket_id)

# Option 5: Remove item
def remove_item(conn, basket_id):
    """Remove an item from the basket"""
    if basket_id is None:
        print("\nYour basket is empty")
        return
    
    cursor = conn.cursor()
    
    # Display basket first
    view_basket(conn, basket_id)
    
    # Get basket items
    cursor.execute("""
        SELECT product_id, seller_id
        FROM basket_contents
        WHERE basket_id = ?
    """, (basket_id,))
    items = cursor.fetchall()
    
    if not items:
        return
    
    # Get item to remove
    if len(items) > 1:
        item_no = 0
        while item_no < 1 or item_no > len(items):
            try:
                item_no = int(input("\nEnter the basket item no. to remove: "))
                if item_no < 1 or item_no > len(items):
                    print("The basket item no. you have entered is invalid")
            except ValueError:
                print("Please enter a valid number")
                item_no = 0
    else:
        item_no = 1
    
    # Confirm removal
    confirm = input("Are you sure you want to remove this item? (Y/N): ").upper()
    if confirm != 'Y':
        return
    
    # Remove item
    item = items[item_no - 1]
    cursor.execute("""
        DELETE FROM basket_contents
        WHERE basket_id = ? AND product_id = ? AND seller_id = ?
    """, (basket_id, item['product_id'], item['seller_id']))
    
    conn.commit()
    print("\nItem removed from basket")
    
    # Check if basket is empty
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM basket_contents
        WHERE basket_id = ?
    """, (basket_id,))
    
    if cursor.fetchone()['count'] == 0:
        print("\nYour basket is empty")
    else:
        view_basket(conn, basket_id)

# Option 6: Checkout
def checkout(conn, shopper_id, basket_id):
    """Checkout the current basket"""
    if basket_id is None:
        print("\nYour basket is empty")
        return None
    
    cursor = conn.cursor()
    
    # Check if basket has items
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM basket_contents
        WHERE basket_id = ?
    """, (basket_id,))
    
    if cursor.fetchone()['count'] == 0:
        print("\nYour basket is empty")
        return None
    
    # Display basket
    view_basket(conn, basket_id)
    
    # Confirm checkout
    confirm = input("\nDo you wish to proceed with the checkout (Y/N)? ").upper()
    if confirm != 'Y':
        return basket_id
    
    try:
        # Start transaction
        conn.execute("BEGIN TRANSACTION")
        
        # Create order
        cursor.execute("""
            INSERT INTO shopper_orders (shopper_id, order_date, order_status)
            VALUES (?, datetime('now'), 'Placed')
        """, (shopper_id,))
        order_id = cursor.lastrowid
        
        # Get basket items
        cursor.execute("""
            SELECT product_id, seller_id, quantity, price
            FROM basket_contents
            WHERE basket_id = ?
        """, (basket_id,))
        items = cursor.fetchall()
        
        # Create ordered products
        for item in items:
            cursor.execute("""
                INSERT INTO ordered_products 
                (order_id, product_id, seller_id, quantity, price, ordered_product_status)
                VALUES (?, ?, ?, ?, ?, 'Placed')
            """, (order_id, item['product_id'], item['seller_id'], 
                  item['quantity'], item['price']))
        
        # Delete basket contents
        cursor.execute("DELETE FROM basket_contents WHERE basket_id = ?", (basket_id,))
        
        # Delete basket
        cursor.execute("DELETE FROM shopper_baskets WHERE basket_id = ?", (basket_id,))
        
        # Commit transaction
        conn.commit()
        print("\nCheckout complete, your order has been placed")
        return None
        
    except sqlite3.Error as e:
        # Rollback on error
        conn.rollback()
        print(f"\nError during checkout: {e}")
        return basket_id

# Main program
def main():
    """Main program function"""
    conn = create_connection()
    
    # Get shopper ID
    shopper_id = None
    while not shopper_id:
        try:
            shopper_id = int(input("Enter your shopper ID: "))
            
            # Verify shopper exists
            cursor = conn.cursor()
            cursor.execute("""
                SELECT shopper_first_name, shopper_surname
                FROM shoppers
                WHERE shopper_id = ?
            """, (shopper_id,))
            
            shopper = cursor.fetchone()
            if not shopper:
                print("Shopper ID not found. Please try again.")
                shopper_id = None
            else:
                print(f"\nWelcome {shopper['shopper_first_name']} {shopper['shopper_surname']}!")
                
        except ValueError:
            print("Please enter a valid number.")
    
    # Get current basket
    basket_id = get_current_basket(conn, shopper_id)
    
    # Main menu loop
    while True:
        print("\n" + "="*50)
        print("Welcome TO SHOPPERS MAIN MENU")
        print("="*50)
        print("1. Display your order history")
        print("2. Add an item to your basket")
        print("3. View your basket")
        print("4. Change the quantity of an item in your basket")
        print("5. Remove an item from your basket")
        print("6. Checkout")
        print("7. Exit")
        
        try:
            choice = int(input("\nSelect an option (1-7): "))
            
            if choice == 1:
                display_order_history(conn, shopper_id)
            elif choice == 2:
                basket_id = add_item_to_basket(conn, shopper_id, basket_id)
            elif choice == 3:
                view_basket(conn, basket_id)
            elif choice == 4:
                change_quantity(conn, basket_id)
            elif choice == 5:
                remove_item(conn, basket_id)
            elif choice == 6:
                basket_id = checkout(conn, shopper_id, basket_id)
            elif choice == 7:
                print("\nThank you for shopping with us!")
                break
            else:
                print("Invalid option. Please select 1-7.")
                
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    conn.close()

if __name__ == "__main__":
    main()