
import tkinter as tk
from tkinter import ttk, messagebox, font
import sqlite3
from datetime import datetime
import sys

class ShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Orinoco Shopping System")
        self.root.geometry("1200x700")
        
        # Configure styles
        self.setup_styles()
        
        # Variables
        self.shopper_id = None
        self.shopper_name = None
        self.basket_id = None
        self.conn = None
        
        # Initialize database connection
        self.create_connection()
        
        # Create main UI
        self.create_login_screen()
        
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#64adf7"
        self.secondary_color = "#05111a"
        self.success_color = "#27ae60"
        self.danger_color = "#e74c3c"
        
        self.root.configure(bg=self.bg_color)
        
        # Configure button styles
        style.configure("Primary.TButton",
                       background=self.primary_color,
                       foreground="white",
                       borderwidth=0,
                       focuscolor="none",
                       padding=(10, 8))
        style.map("Primary.TButton",
                 background=[('active', '#34495e')])
        
        style.configure("Success.TButton",
                       background=self.success_color,
                       foreground="white",
                       borderwidth=0,
                       padding=(10, 8))
        
        style.configure("Danger.TButton",
                       background=self.danger_color,
                       foreground="white",
                       borderwidth=0,
                       padding=(10, 8))
        
    def create_connection(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect('orinoco.db')
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")
            sys.exit(1)
            
    def create_login_screen(self):
        """Create login screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create login frame
        login_frame = tk.Frame(self.root, bg=self.bg_color)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(login_frame, text="Orinoco Shopping System",
                               font=title_font, bg=self.bg_color, fg=self.primary_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Login form
        tk.Label(login_frame, text="Shopper ID:", bg=self.bg_color,
                font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        self.shopper_id_entry = tk.Entry(login_frame, font=("Helvetica", 12), width=20)
        self.shopper_id_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Login button
        login_btn = ttk.Button(login_frame, text="Login", style="Primary.TButton",
                              command=self.login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Bind Enter key to login
        self.shopper_id_entry.bind('<Return>', lambda e: self.login())
        self.shopper_id_entry.focus()
        
    def login(self):
        """Handle user login"""
        try:
            shopper_id = int(self.shopper_id_entry.get())
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT shopper_first_name, shopper_surname
                FROM shoppers
                WHERE shopper_id = ?
            """, (shopper_id,))
            
            shopper = cursor.fetchone()
            if not shopper:
                messagebox.showerror("Login Failed", "Shopper ID not found")
                return
                
            self.shopper_id = shopper_id
            self.shopper_name = f"{shopper['shopper_first_name']} {shopper['shopper_surname']}"
            self.basket_id = self.get_current_basket()
            self.create_main_screen()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric ID")
            
    def get_current_basket(self):
        """Get current basket for the shopper"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT basket_id
            FROM shopper_baskets
            WHERE shopper_id = ?
            AND DATE(basket_created_date_time) = DATE('now')
            ORDER BY basket_created_date_time DESC
            LIMIT 1
        """, (self.shopper_id,))
        
        result = cursor.fetchone()
        return result['basket_id'] if result else None
        
    def create_main_screen(self):
        """Create main application screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create header
        self.create_header()
        
        # Create main content area
        self.main_content = tk.Frame(self.root, bg="white")
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Show welcome message
        self.show_welcome()
        
    def create_header(self):
        """Create header with navigation"""
        header = tk.Frame(self.root, bg=self.primary_color, height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Welcome message
        welcome_frame = tk.Frame(header, bg=self.primary_color)
        welcome_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(welcome_frame, text=f"Welcome, {self.shopper_name}!",
                font=("Helvetica", 16, "bold"), bg=self.primary_color,
                fg="white").pack(anchor='w')
        
        basket_text = f"Basket ID: {self.basket_id}" if self.basket_id else "No active basket"
        tk.Label(welcome_frame, text=basket_text,
                font=("Helvetica", 11), bg=self.primary_color,
                fg="white").pack(anchor='w')
        
        # Navigation buttons
        nav_frame = tk.Frame(header, bg=self.primary_color)
        nav_frame.pack(side=tk.RIGHT, padx=20)
        
        buttons = [
            ("Order History", self.show_order_history),
            ("Add Item", self.show_add_item),
            ("View Basket", self.show_basket),
            ("Checkout", self.checkout),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            btn = tk.Button(nav_frame, text=text, command=command,
                           bg=self.secondary_color, fg="white",
                           font=("Helvetica", 10), padx=15, pady=5,
                           relief=tk.FLAT, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=5, pady=20)
            
    def clear_content(self):
        """Clear main content area"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
    def show_welcome(self):
        """Show welcome screen"""
        self.clear_content()
        
        welcome_label = tk.Label(self.main_content,
                                text="Welcome to Orinoco Shopping System",
                                font=("Helvetica", 20, "bold"),
                                bg="white", fg=self.primary_color)
        welcome_label.pack(pady=50)
        
        info_text = """
        Please use the navigation menu above to:
        • View your order history
        • Add items to your basket
        • View and manage your basket
        • Checkout when ready
        """
        
        tk.Label(self.main_content, text=info_text,
                font=("Helvetica", 12), bg="white",
                justify=tk.LEFT).pack(pady=20)
                
    def show_order_history(self):
        """Display order history in main content"""
        self.clear_content()
        
        # Title
        tk.Label(self.main_content, text="Order History",
                font=("Helvetica", 18, "bold"), bg="white",
                fg=self.primary_color).pack(pady=10)
        
        # Create treeview for orders
        tree_frame = tk.Frame(self.main_content, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        columns = ("Order ID", "Date", "Product", "Seller", "Price", "Quantity", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                           yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        tree.column("Product", width=200)
        tree.column("Seller", width=150)
        
        # Get order data
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT o.order_id, o.order_date, p.product_description,
                   s.seller_name, op.price, op.quantity, op.ordered_product_status
            FROM shopper_orders o
            JOIN ordered_products op ON o.order_id = op.order_id
            JOIN products p ON op.product_id = p.product_id
            JOIN sellers s ON op.seller_id = s.seller_id
            WHERE o.shopper_id = ?
            ORDER BY o.order_date DESC
        """, (self.shopper_id,))
        
        orders = cursor.fetchall()
        
        if not orders:
            tk.Label(self.main_content, text="No orders found",
                    font=("Helvetica", 14), bg="white").pack(pady=20)
        else:
            for order in orders:
                tree.insert('', 'end', values=(
                    order['order_id'],
                    order['order_date'],
                    order['product_description'],
                    order['seller_name'],
                    f"£{order['price']:.2f}",
                    order['quantity'],
                    order['ordered_product_status']
                ))
        
        # Pack treeview and scrollbars
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
    def show_add_item(self):
        """Show add item interface"""
        self.clear_content()
        
        tk.Label(self.main_content, text="Add Item to Basket",
                font=("Helvetica", 18, "bold"), bg="white",
                fg=self.primary_color).pack(pady=10)
        
        # Create selection frames
        select_frame = tk.Frame(self.main_content, bg="white")
        select_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Category selection
        tk.Label(select_frame, text="Select Category:",
                font=("Helvetica", 12), bg="white").grid(row=0, column=0, sticky='w', pady=5)
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(select_frame, textvariable=self.category_var,
                                           state='readonly', width=40)
        self.category_combo.grid(row=0, column=1, pady=5, padx=10)
        self.category_combo.bind('<<ComboboxSelected>>', self.on_category_selected)
        
        # Product selection
        tk.Label(select_frame, text="Select Product:",
                font=("Helvetica", 12), bg="white").grid(row=1, column=0, sticky='w', pady=5)
        
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(select_frame, textvariable=self.product_var,
                                         state='readonly', width=40)
        self.product_combo.grid(row=1, column=1, pady=5, padx=10)
        self.product_combo.bind('<<ComboboxSelected>>', self.on_product_selected)
        
        # Seller selection
        tk.Label(select_frame, text="Select Seller:",
                font=("Helvetica", 12), bg="white").grid(row=2, column=0, sticky='w', pady=5)
        
        self.seller_var = tk.StringVar()
        self.seller_combo = ttk.Combobox(select_frame, textvariable=self.seller_var,
                                        state='readonly', width=40)
        self.seller_combo.grid(row=2, column=1, pady=5, padx=10)
        
        # Quantity
        tk.Label(select_frame, text="Quantity:",
                font=("Helvetica", 12), bg="white").grid(row=3, column=0, sticky='w', pady=5)
        
        self.quantity_var = tk.IntVar(value=1)
        quantity_spin = ttk.Spinbox(select_frame, from_=1, to=100,
                                    textvariable=self.quantity_var, width=10)
        quantity_spin.grid(row=3, column=1, pady=5, padx=10, sticky='w')
        
        # Add to basket button
        add_btn = ttk.Button(select_frame, text="Add to Basket",
                            style="Success.TButton", command=self.add_to_basket)
        add_btn.grid(row=4, column=1, pady=20, sticky='w')
        
        # Load categories
        self.load_categories()
        
    def load_categories(self):
        """Load categories into combobox"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT category_id, category_description
            FROM categories
            ORDER BY category_description
        """)
        categories = cursor.fetchall()
        
        self.category_map = {}
        category_list = []
        for cat in categories:
            self.category_map[cat['category_description']] = cat['category_id']
            category_list.append(cat['category_description'])
            
        self.category_combo['values'] = category_list
        
    def on_category_selected(self, event):
        """Handle category selection"""
        category_name = self.category_var.get()
        if category_name:
            category_id = self.category_map[category_name]
            self.load_products(category_id)
            
    def load_products(self, category_id):
        """Load products for selected category"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT product_id, product_description
            FROM products
            WHERE category_id = ?
            ORDER BY product_description
        """, (category_id,))
        products = cursor.fetchall()
        
        self.product_map = {}
        product_list = []
        for prod in products:
            self.product_map[prod['product_description']] = prod['product_id']
            product_list.append(prod['product_description'])
            
        self.product_combo['values'] = product_list
        self.product_combo.set('')
        self.seller_combo['values'] = []
        self.seller_combo.set('')
        
    def on_product_selected(self, event):
        """Handle product selection"""
        product_name = self.product_var.get()
        if product_name:
            product_id = self.product_map[product_name]
            self.load_sellers(product_id)
            
    def load_sellers(self, product_id):
        """Load sellers for selected product"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT ps.seller_id, s.seller_name, ps.price
            FROM product_sellers ps
            JOIN sellers s ON ps.seller_id = s.seller_id
            WHERE ps.product_id = ?
            ORDER BY s.seller_name
        """, (product_id,))
        sellers = cursor.fetchall()
        
        self.seller_map = {}
        seller_list = []
        for seller in sellers:
            display_text = f"{seller['seller_name']} - £{seller['price']:.2f}"
            self.seller_map[display_text] = {
                'seller_id': seller['seller_id'],
                'price': seller['price']
            }
            seller_list.append(display_text)
            
        self.seller_combo['values'] = seller_list
        self.seller_combo.set('')
        
    def add_to_basket(self):
        """Add selected item to basket"""
        # Validate selections
        if not self.product_var.get():
            messagebox.showwarning("Incomplete Selection", "Please select a product")
            return
        if not self.seller_var.get():
            messagebox.showwarning("Incomplete Selection", "Please select a seller")
            return
            
        product_id = self.product_map[self.product_var.get()]
        seller_info = self.seller_map[self.seller_var.get()]
        quantity = self.quantity_var.get()
        
        cursor = self.conn.cursor()
        
        # Create basket if needed
        if self.basket_id is None:
            cursor.execute("""
                INSERT INTO shopper_baskets (shopper_id, basket_created_date_time)
                VALUES (?, datetime('now'))
            """, (self.shopper_id,))
            self.basket_id = cursor.lastrowid
            
        # Add item to basket
        cursor.execute("""
            INSERT INTO basket_contents (basket_id, product_id, seller_id, quantity, price)
            VALUES (?, ?, ?, ?, ?)
        """, (self.basket_id, product_id, seller_info['seller_id'],
              quantity, seller_info['price']))
        
        self.conn.commit()
        
        messagebox.showinfo("Success", "Item added to basket successfully!")
        
        # Update header
        self.create_header()
        
        # Clear selections
        self.category_combo.set('')
        self.product_combo.set('')
        self.seller_combo.set('')
        self.quantity_var.set(1)
        
    def show_basket(self):
        """Display basket contents"""
        self.clear_content()
        
        tk.Label(self.main_content, text="Shopping Basket",
                font=("Helvetica", 18, "bold"), bg="white",
                fg=self.primary_color).pack(pady=10)
        
        if self.basket_id is None:
            tk.Label(self.main_content, text="Your basket is empty",
                    font=("Helvetica", 14), bg="white").pack(pady=20)
            return
            
        # Get basket contents
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT bc.product_id, bc.seller_id, p.product_description,
                   s.seller_name, bc.quantity, bc.price,
                   (bc.quantity * bc.price) as line_total
            FROM basket_contents bc
            JOIN products p ON bc.product_id = p.product_id
            JOIN sellers s ON bc.seller_id = s.seller_id
            WHERE bc.basket_id = ?
            ORDER BY p.product_description
        """, (self.basket_id,))
        
        items = cursor.fetchall()
        
        if not items:
            tk.Label(self.main_content, text="Your basket is empty",
                    font=("Helvetica", 14), bg="white").pack(pady=20)
            return
            
        # Create basket display
        basket_frame = tk.Frame(self.main_content, bg="white")
        basket_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Headers
        headers = ["Product", "Seller", "Price", "Quantity", "Total", "Actions"]
        for i, header in enumerate(headers):
            tk.Label(basket_frame, text=header, font=("Helvetica", 11, "bold"),
                    bg="white", fg=self.primary_color).grid(row=0, column=i, padx=10, pady=5)
        
        # Items
        total = 0
        self.basket_items = []
        for idx, item in enumerate(items, start=1):
            self.basket_items.append(item)
            
            tk.Label(basket_frame, text=item['product_description'],
                    bg="white").grid(row=idx, column=0, padx=10, pady=5, sticky='w')
            tk.Label(basket_frame, text=item['seller_name'],
                    bg="white").grid(row=idx, column=1, padx=10, pady=5)
            tk.Label(basket_frame, text=f"£{item['price']:.2f}",
                    bg="white").grid(row=idx, column=2, padx=10, pady=5)
            
            # Quantity with update
            qty_frame = tk.Frame(basket_frame, bg="white")
            qty_frame.grid(row=idx, column=3, padx=10, pady=5)
            
            qty_var = tk.IntVar(value=item['quantity'])
            qty_spin = ttk.Spinbox(qty_frame, from_=1, to=100,
                                  textvariable=qty_var, width=5)
            qty_spin.pack(side=tk.LEFT)
            
            update_btn = tk.Button(qty_frame, text="Update",
                                  command=lambda i=idx-1, v=qty_var: self.update_quantity(i, v.get()),
                                  bg=self.secondary_color, fg="white",
                                  font=("Helvetica", 9), padx=5, pady=2)
            update_btn.pack(side=tk.LEFT, padx=5)
            
            tk.Label(basket_frame, text=f"£{item['line_total']:.2f}",
                    bg="white").grid(row=idx, column=4, padx=10, pady=5)
            
            # Remove button
            remove_btn = tk.Button(basket_frame, text="Remove",
                                  command=lambda i=idx-1: self.remove_item(i),
                                  bg=self.danger_color, fg="white",
                                  font=("Helvetica", 9), padx=10, pady=2)
            remove_btn.grid(row=idx, column=5, padx=10, pady=5)
            
            total += item['line_total']
        
        # Total
        tk.Label(basket_frame, text="Total:", font=("Helvetica", 14, "bold"),
                bg="white", fg=self.primary_color).grid(row=len(items)+1, column=3,
                                                         padx=10, pady=10, sticky='e')
        tk.Label(basket_frame, text=f"£{total:.2f}", font=("Helvetica", 14, "bold"),
                bg="white", fg=self.success_color).grid(row=len(items)+1, column=4,
                                                         padx=10, pady=10)
        
    def update_quantity(self, item_index, new_quantity):
        """Update item quantity in basket"""
        item = self.basket_items[item_index]
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE basket_contents
            SET quantity = ?
            WHERE basket_id = ? AND product_id = ? AND seller_id = ?
        """, (new_quantity, self.basket_id, item['product_id'], item['seller_id']))
        self.conn.commit()
        
        messagebox.showinfo("Success", "Quantity updated")
        self.show_basket()
        
    def remove_item(self, item_index):
        """Remove item from basket"""
        if not messagebox.askyesno("Confirm", "Remove this item from basket?"):
            return
            
        item = self.basket_items[item_index]
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM basket_contents
            WHERE basket_id = ? AND product_id = ? AND seller_id = ?
        """, (self.basket_id, item['product_id'], item['seller_id']))
        self.conn.commit()
        
        # Check if basket is empty
        cursor.execute("""
            SELECT COUNT(*) as count FROM basket_contents WHERE basket_id = ?
        """, (self.basket_id,))
        
        if cursor.fetchone()['count'] == 0:
            self.basket_id = None
            self.create_header()
            
        self.show_basket()
        
    def checkout(self):
        """Process checkout"""
        if self.basket_id is None:
            messagebox.showinfo("Empty Basket", "Your basket is empty")
            return
            
        # Verify basket has items
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count FROM basket_contents WHERE basket_id = ?
        """, (self.basket_id,))
        
        if cursor.fetchone()['count'] == 0:
            messagebox.showinfo("Empty Basket", "Your basket is empty")
            return
            
        if not messagebox.askyesno("Confirm Checkout", 
                                   "Do you wish to proceed with the checkout?"):
            return
            
        try:
            # Begin transaction
            self.conn.execute("BEGIN TRANSACTION")
            
            # Create order
            cursor.execute("""
                INSERT INTO shopper_orders (shopper_id, order_date, order_status)
                VALUES (?, datetime('now'), 'Placed')
            """, (self.shopper_id,))
            order_id = cursor.lastrowid
            
            # Transfer basket items to order
            cursor.execute("""
                SELECT product_id, seller_id, quantity, price
                FROM basket_contents
                WHERE basket_id = ?
            """, (self.basket_id,))
            items = cursor.fetchall()
            
            for item in items:
                cursor.execute("""
                    INSERT INTO ordered_products
                    (order_id, product_id, seller_id, quantity, price, ordered_product_status)
                    VALUES (?, ?, ?, ?, ?, 'Placed')
                """, (order_id, item['product_id'], item['seller_id'],
                      item['quantity'], item['price']))
            
            # Clear basket
            cursor.execute("DELETE FROM basket_contents WHERE basket_id = ?", (self.basket_id,))
            cursor.execute("DELETE FROM shopper_baskets WHERE basket_id = ?", (self.basket_id,))
            
            self.conn.commit()
            
            self.basket_id = None
            messagebox.showinfo("Success", f"Order placed successfully!\nOrder ID: {order_id}")
            
            # Update UI
            self.create_header()
            self.show_welcome()
            
        except sqlite3.Error as e:
            self.conn.rollback()
            messagebox.showerror("Checkout Error", f"Failed to process order: {e}")
            
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.shopper_id = None
            self.shopper_name = None
            self.basket_id = None
            self.create_login_screen()
            
    def __del__(self):
        """Clean up database connection"""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

def main():
    root = tk.Tk()
    app = ShoppingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
        
        
        
        
def main():
    root = tk.Tk()
    app = OnlineShoppingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()