import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import sqlite3
from datetime import datetime
#from reportlab.lib.pagesizes import letter     #will be used in future versions
#from reportlab.pdfgen import canvas
#from reportlab.lib import colors
#from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
#from reportlab.lib.units import inch

class OnlineShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Shopping Application V2")
        self.root.geometry("1300x700")
        
        # Configure styles
        self.setup_styles()
        
        # Variables
        self.shopper_id = None
        self.shopper_details = {}
        self.basket_id = None
        self.is_admin = False
        self.conn = None
        
        # Initialize database connection
        self.create_connection()
        
        # Create initial screen with login/register options
        self.create_welcome_screen()
        
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.success_color = "#27ae60"
        self.danger_color = "#e74c3c"
        self.info_color = "#9b59b6"
        
        self.root.configure(bg=self.bg_color)
        
        style.configure("Primary.TButton",
                       background=self.primary_color,
                       foreground="white",
                       borderwidth=0,
                       focuscolor="none",
                       padding=(10, 8))
        
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
        
        style.configure("Info.TButton",
                       background=self.info_color,
                       foreground="white",
                       borderwidth=0,
                       padding=(10, 8))
        
    def create_connection(self):
        """Establish database connection and ensure tables exist"""
        try:
            self.conn = sqlite3.connect('shopping_app.db')
            self.conn.row_factory = sqlite3.Row
            self.show_connection_status()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect: {e}")
            
    def show_connection_status(self):
        """Display connection successful message"""
        status_label = tk.Label(self.root, 
                               text="✓ Database Connection Successful", 
                               fg="green", 
                               font=("Arial", 10, "bold"),
                               bg=self.bg_color)
        status_label.pack(pady=5)
        self.root.after(2000, status_label.destroy)
        
    def create_welcome_screen(self):
        """Create welcome screen with login and register options"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title_font = font.Font(family="Helvetica", size=28, weight="bold")
        title_label = tk.Label(main_frame, text="Orinoco Shopping System V2",
                               font=title_font, bg=self.bg_color, fg=self.primary_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=30)
        
        subtitle_label = tk.Label(main_frame, text="Your One-Stop Shopping Solution",
                                 font=("Helvetica", 14), bg=self.bg_color, fg="#7f8c8d")
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.grid(row=2, column=0, columnspan=2)
        
        login_btn = tk.Button(button_frame, text="Login", 
                             command=self.show_login_screen,
                             bg=self.primary_color, fg="white",
                             font=("Helvetica", 12, "bold"),
                             padx=40, pady=15,
                             relief=tk.FLAT, cursor="hand2")
        login_btn.grid(row=0, column=0, padx=20)
        
        register_btn = tk.Button(button_frame, text="Register New Customer", 
                                command=self.show_register_screen,
                                bg=self.success_color, fg="white",
                                font=("Helvetica", 12, "bold"),
                                padx=25, pady=15,
                                relief=tk.FLAT, cursor="hand2")
        register_btn.grid(row=0, column=1, padx=20)
        
        admin_btn = tk.Button(main_frame, text="Admin Login", 
                             command=self.show_admin_login,
                             bg=self.info_color, fg="white",
                             font=("Helvetica", 10),
                             padx=20, pady=8,
                             relief=tk.FLAT, cursor="hand2")
        admin_btn.grid(row=3, column=0, columnspan=2, pady=30)
        
    def show_login_screen(self):
        """Show login screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        login_frame = tk.Frame(self.root, bg=self.bg_color)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(login_frame, text="Customer Login",
                               font=title_font, bg=self.bg_color, fg=self.primary_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(login_frame, text="Email:", bg=self.bg_color,
                font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        self.login_email_entry = tk.Entry(login_frame, font=("Helvetica", 12), width=25)
        self.login_email_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(login_frame, text="Password:", bg=self.bg_color,
                font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        
        self.login_password_entry = tk.Entry(login_frame, font=("Helvetica", 12), width=25, show="*")
        self.login_password_entry.grid(row=2, column=1, padx=10, pady=10)
        
        button_frame = tk.Frame(login_frame, bg=self.bg_color)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        login_btn = ttk.Button(button_frame, text="Login", style="Primary.TButton",
                              command=self.login)
        login_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = ttk.Button(button_frame, text="Back", 
                             command=self.create_welcome_screen)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        self.login_email_entry.bind('<Return>', lambda e: self.login())
        self.login_password_entry.bind('<Return>', lambda e: self.login())
        self.login_email_entry.focus()
        
    def show_admin_login(self):
        """Show admin login screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        login_frame = tk.Frame(self.root, bg=self.bg_color)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(login_frame, text="Admin Login",
                               font=title_font, bg=self.bg_color, fg=self.info_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(login_frame, text="Admin Code:", bg=self.bg_color,
                font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        self.admin_code_entry = tk.Entry(login_frame, font=("Helvetica", 12), width=25, show="*")
        self.admin_code_entry.grid(row=1, column=1, padx=10, pady=10)
        
        button_frame = tk.Frame(login_frame, bg=self.bg_color)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        login_btn = ttk.Button(button_frame, text="Login", style="Info.TButton",
                              command=self.admin_login)
        login_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = ttk.Button(button_frame, text="Back", 
                             command=self.create_welcome_screen)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        self.admin_code_entry.bind('<Return>', lambda e: self.admin_login())
        self.admin_code_entry.focus()
        
    def admin_login(self):
        """Process admin login"""
        admin_code = self.admin_code_entry.get()
        
        if admin_code == "ADMIN2024":
            self.is_admin = True
            self.show_admin_panel()
        else:
            messagebox.showerror("Error", "Invalid admin code")
            
    def show_admin_panel(self):
        """Show admin control panel"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        header = tk.Frame(self.root, bg=self.info_color, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_label = tk.Label(header, text="Admin Control Panel",
                               font=("Helvetica", 20, "bold"),
                               bg=self.info_color, fg="white")
        header_label.pack(pady=20)
        
        logout_btn = tk.Button(header, text="Logout", command=self.logout,
                              bg=self.danger_color, fg="white",
                              font=("Helvetica", 10), padx=15, pady=5,
                              relief=tk.FLAT, cursor="hand2")
        logout_btn.place(relx=0.95, rely=0.5, anchor='e')
        
        content = tk.Frame(self.root, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        options_frame = tk.Frame(content, bg="white")
        options_frame.pack(pady=30)
        
        add_product_btn = tk.Button(options_frame, text="Add New Product",
                                   command=self.show_add_product_form,
                                   bg=self.success_color, fg="white",
                                   font=("Helvetica", 14, "bold"),
                                   padx=30, pady=20,
                                   relief=tk.FLAT, cursor="hand2",
                                   width=20)
        add_product_btn.grid(row=0, column=0, padx=20, pady=10)
        
        view_products_btn = tk.Button(options_frame, text="View All Products",
                                     command=self.show_all_products,
                                     bg=self.primary_color, fg="white",
                                     font=("Helvetica", 14, "bold"),
                                     padx=30, pady=20,
                                     relief=tk.FLAT, cursor="hand2",
                                     width=20)
        view_products_btn.grid(row=0, column=1, padx=20, pady=10)
        
        view_customers_btn = tk.Button(options_frame, text="View All Customers",
                                      command=self.show_all_customers,
                                      bg=self.secondary_color, fg="white",
                                      font=("Helvetica", 14, "bold"),
                                      padx=30, pady=20,
                                      relief=tk.FLAT, cursor="hand2",
                                      width=20)
        view_customers_btn.grid(row=1, column=0, padx=20, pady=10)
        
        view_orders_btn = tk.Button(options_frame, text="View All Orders",
                                   command=self.show_all_orders_admin,
                                   bg=self.info_color, fg="white",
                                   font=("Helvetica", 14, "bold"),
                                   padx=30, pady=20,
                                   relief=tk.FLAT, cursor="hand2",
                                   width=20)
        view_orders_btn.grid(row=1, column=1, padx=20, pady=10)
        
    def show_add_product_form(self):
        """Show form to add new product"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Product")
        add_window.geometry("500x600")
        add_window.configure(bg="white")
        
        tk.Label(add_window, text="Add New Product",
                font=("Helvetica", 18, "bold"), bg="white",
                fg=self.primary_color).pack(pady=20)
        
        form_frame = tk.Frame(add_window, bg="white")
        form_frame.pack(padx=30, pady=20)
        
        fields = [
            ("Product Description:", "product_desc"),
            ("Category:", "category"),
            ("Seller:", "seller"),
            ("Price (£):", "price")
        ]
        
        entries = {}
        
        for i, (label, field) in enumerate(fields):
            tk.Label(form_frame, text=label, bg="white").grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field] = entry
        
        def save_product():
            messagebox.showinfo("Success", "Product saved successfully!")
            add_window.destroy()
        
        save_btn = tk.Button(add_window, text="Save Product",
                            command=save_product,
                            bg=self.success_color, fg="white",
                            font=("Helvetica", 12, "bold"),
                            padx=20, pady=10,
                            relief=tk.FLAT, cursor="hand2")
        save_btn.pack(pady=20)
        
    def show_all_products(self):
        """Display all products for admin"""
        products_window = tk.Toplevel(self.root)
        products_window.title("All Products")
        products_window.geometry("900x600")
        products_window.configure(bg="white")
        
        tk.Label(products_window, text="All Products",
                font=("Helvetica", 18, "bold"), bg="white",
                fg=self.primary_color).pack(pady=10)
        
        tree_frame = tk.Frame(products_window, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        columns = ("ID", "Description", "Category", "Sellers", "Price Range")
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                           yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.column("Description", width=250)
        
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
    def show_all_customers(self):
        """Display all customers for admin"""
        customers_window = tk.Toplevel(self.root)
        customers_window.title("All Customers")
        customers_window.geometry("1000x600")
        customers_window.configure(bg="white")
        
        tk.Label(customers_window, text="All Customers",
                font=("Helvetica", 18, "bold"), bg="white",
                fg=self.primary_color).pack(pady=10)
        
        tree_frame = tk.Frame(customers_window, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        columns = ("ID", "Name", "Email", "Phone", "Address", "Total Orders")
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                           yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.column("Email", width=200)
        tree.column("Address", width=250)
        
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
    def show_all_orders_admin(self):
        """Display all orders for admin"""
        orders_window = tk.Toplevel(self.root)
        orders_window.title("All Orders")
        orders_window.geometry("1100x600")
        orders_window.configure(bg="white")
        
        tk.Label(orders_window, text="All Orders",
                font=("Helvetica", 18, "bold"), bg="white",
                fg=self.primary_color).pack(pady=10)
        
        tree_frame = tk.Frame(orders_window, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        columns = ("Order ID", "Customer", "Date", "Total Items", "Total Value", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                           yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        tree.column("Customer", width=200)
        
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
    def show_register_screen(self):
        """Show registration screen for new customers"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        canvas = tk.Canvas(self.root, bg=self.bg_color)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        register_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        register_frame.pack(pady=30)
        
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(register_frame, text="Customer Registration",
                               font=title_font, bg=self.bg_color, fg=self.primary_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        fields = [
            ("First Name:", "first_name", False),
            ("Last Name:", "surname", False),
            ("Email:", "email", False),
            ("Password:", "password", True),
            ("Confirm Password:", "confirm_password", True),
            ("Phone:", "phone", False),
            ("Address:", "address", False)
        ]
        
        self.register_entries = {}
        
        for i, (label, field, is_password) in enumerate(fields, start=1):
            tk.Label(register_frame, text=label, bg=self.bg_color).grid(row=i, column=0, sticky='e', padx=10, pady=10)
            entry = tk.Entry(register_frame, width=30, show="*" if is_password else "")
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.register_entries[field] = entry
        
        button_frame = tk.Frame(register_frame, bg=self.bg_color)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        register_btn = ttk.Button(button_frame, text="Register", style="Success.TButton",
                                 command=self.register_customer)
        register_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = ttk.Button(button_frame, text="Back", 
                             command=self.create_welcome_screen)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def register_customer(self):
        """Process customer registration"""
        try:
            data = {field: self.register_entries[field].get().strip() for field in self.register_entries}
            
            if not all([data['first_name'], data['email'], data['password']]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            if data['password'] != data['confirm_password']:
                messagebox.showerror("Error", "Passwords don't match")
                return
            
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.create_welcome_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
            
    def login(self):
        """Handle user login"""
        email = self.login_email_entry.get().strip()
        password = self.login_password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter email and password")
            return
        
        self.shopper_id = 1
        self.shopper_details = {
            'first_name': 'John',
            'surname': 'Doe',
            'email': email,
            'phone': '01234567890',
            'address': '123 Main Street'
        }
        
        self.basket_id = 1
        self.create_main_screen()
        
    def get_current_basket(self):
        """Get current basket for the shopper"""
        return 1
        
    def create_main_screen(self):
        """Create main application screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.create_header()
        
        profile_frame = tk.Frame(self.root, bg="white", relief=tk.RAISED, bd=1)
        profile_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(profile_frame, text="Customer Profile",
                font=("Helvetica", 14, "bold"), bg="white",
                fg=self.primary_color).pack(pady=10)
        
        details_frame = tk.Frame(profile_frame, bg="white")
        details_frame.pack(padx=20, pady=10)
        
        profile_info = [
            ("Name:", f"{self.shopper_details['first_name']} {self.shopper_details['surname']}"),
            ("Email:", self.shopper_details['email']),
            ("Phone:", self.shopper_details['phone'] or 'Not provided'),
            ("Address:", self.shopper_details['address'] or 'Not provided')
        ]
        
        for i, (label, value) in enumerate(profile_info):
            tk.Label(details_frame, text=label, font=("Helvetica", 11, "bold"), bg="white").grid(row=i, column=0, sticky='e', padx=10)
            tk.Label(details_frame, text=value, bg="white").grid(row=i, column=1, sticky='w', padx=10)
        
        self.main_content = tk.Frame(self.root, bg="white")
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.show_welcome()
        
    def create_header(self):
        """Create header with navigation"""
        header = tk.Frame(self.root, bg=self.primary_color, height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        welcome_frame = tk.Frame(header, bg=self.primary_color)
        welcome_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(welcome_frame, 
                text=f"Welcome, {self.shopper_details['first_name']}!",
                font=("Helvetica", 16, "bold"), bg=self.primary_color,
                fg="white").pack(anchor='w')
        
        basket_text = f"Basket ID: {self.basket_id}" if self.basket_id else "No active basket"
        tk.Label(welcome_frame, text=basket_text,
                font=("Helvetica", 11), bg=self.primary_color,
                fg="white").pack(anchor='w')
        
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
                           font=("Helvetica", 10), padx=10, pady=5,
                           relief=tk.FLAT, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=5)
            
    def show_welcome(self):
        """Show welcome message"""
        self.main_content.destroy()
        self.main_content = tk.Frame(self.root, bg="white")
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        welcome_label = tk.Label(self.main_content, text="Welcome to Shopping System",
                                font=("Helvetica", 18, "bold"), bg="white")
        welcome_label.pack(pady=30)
        
    def show_order_history(self):
        """Show order history"""
        messagebox.showinfo("Order History", "Your order history will be displayed here")
        
    def show_add_item(self):
        """Show add item to basket"""
        messagebox.showinfo("Add Item", "Add item to basket functionality coming soon")
        
    def show_basket(self):
        """Show basket contents"""
        messagebox.showinfo("View Basket", "Your basket contents will be displayed here")
        
    def checkout(self):
        """Process checkout"""
        messagebox.showinfo("Checkout", "Checkout functionality coming soon")
        
    def logout(self):
        """Logout user"""
        self.shopper_id = None
        self.shopper_details = {}
        self.is_admin = False
        self.create_welcome_screen()
        
    def __del__(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

def main():
    root = tk.Tk()
    app = OnlineShoppingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()