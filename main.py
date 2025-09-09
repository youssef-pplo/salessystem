from flask import Flask, render_template, abort
import datetime

app = Flask(__name__)

# Mock data
products = [
    {'id': 1, 'name': 'Widget', 'price': 25.99, 'initial_stock': 100},
    {'id': 2, 'name': 'Gadget', 'price': 49.99, 'initial_stock': 50},
    {'id': 3, 'name': 'Doohickey', 'price': 9.99, 'initial_stock': 200},
]

clients = [
    {'id': 1, 'name': 'Alice Johnson', 'contact': 'alice@email.com'},
    {'id': 2, 'name': 'Bob Smith', 'contact': 'bob@email.com'},
    {'id': 3, 'name': 'Charlie Brown', 'contact': 'charlie@email.com'},
]

sales = [
    {'id': 1, 'salesperson': 'John Doe', 'product_id': 1, 'client_id': 1, 'quantity': 10, 'date': '2025-09-09'},
    {'id': 2, 'salesperson': 'Jane Roe', 'product_id': 2, 'client_id': 2, 'quantity': 5, 'date': '2025-09-08'},
    {'id': 3, 'salesperson': 'John Doe', 'product_id': 1, 'client_id': 3, 'quantity': 15, 'date': '2025-09-09'},
    {'id': 4, 'salesperson': 'Jane Roe', 'product_id': 3, 'client_id': 1, 'quantity': 20, 'date': '2025-09-09'},
    {'id': 5, 'salesperson': 'John Doe', 'product_id': 2, 'client_id': 3, 'quantity': 3, 'date': '2025-09-07'},
]

@app.route('/')
def dashboard():
    today = '2025-09-09'  # Hardcoded to match mock data; in real use, datetime.date.today().isoformat()

    # Compute KPIs
    total_sales_today = sum(
        s['quantity'] * next(p['price'] for p in products if p['id'] == s['product_id'])
        for s in sales if s['date'] == today
    )
    num_clients = len(clients)

    # Best-selling product
    sold_by_product = {}
    for s in sales:
        pid = s['product_id']
        sold_by_product[pid] = sold_by_product.get(pid, 0) + s['quantity']
    best_product = 'None'
    if sold_by_product:
        best_pid = max(sold_by_product, key=sold_by_product.get)
        best_product = next(p['name'] for p in products if p['id'] == best_pid)

    # Total remaining stock
    remaining_by_product = {}
    for p in products:
        sold = sum(s['quantity'] for s in sales if s['product_id'] == p['id'])
        remaining_by_product[p['id']] = p['initial_stock'] - sold
    total_remaining = sum(remaining_by_product.values())

    # Sales table
    sales_table = []
    for s in sales:
        p = next(p for p in products if p['id'] == s['product_id'])
        total = s['quantity'] * p['price']
        sales_table.append({
            'salesperson': s['salesperson'],
            'product': p['name'],
            'quantity': s['quantity'],
            'date': s['date'],
            'price': p['price'],
            'total': total
        })

    # Inventory table
    inventory_table = []
    for p in products:
        sold = sum(s['quantity'] for s in sales if s['product_id'] == p['id'])
        remaining = p['initial_stock'] - sold
        inventory_table.append({
            'id': p['id'],
            'product': p['name'],
            'initial_stock': p['initial_stock'],
            'units_sold': sold,
            'remaining_stock': remaining
        })

    # Clients table: last purchased product (most recent)
    client_purchases = {}
    for s in sorted(sales, key=lambda x: x['date'], reverse=True):
        cid = s['client_id']
        if cid not in client_purchases:
            p_name = next(p['name'] for p in products if p['id'] == s['product_id'])
            client_purchases[cid] = p_name
    clients_table = []
    for c in clients:
        last_product = client_purchases.get(c['id'], 'None')
        clients_table.append({
            'name': c['name'],
            'contact': c['contact'],
            'last_product': last_product
        })

    return render_template('dashboard.html',
                           total_sales_today=round(total_sales_today, 2),
                           num_clients=num_clients,
                           best_product=best_product,
                           total_remaining=total_remaining,
                           sales_table=sales_table,
                           inventory_table=inventory_table,
                           clients_table=clients_table)

@app.route('/product/<int:pid>')
def product_detail(pid):
    p = next((pr for pr in products if pr['id'] == pid), None)
    if not p:
        abort(404)

    sold = sum(s['quantity'] for s in sales if s['product_id'] == pid)
    remaining = p['initial_stock'] - sold
    revenue = sold * p['price']

    # Sales related to this product
    product_sales = []
    for s in sales:
        if s['product_id'] == pid:
            client_name = next(c['name'] for c in clients if c['id'] == s['client_id'])
            total = s['quantity'] * p['price']
            product_sales.append({
                'salesperson': s['salesperson'],
                'client': client_name,
                'quantity': s['quantity'],
                'date': s['date'],
                'total': total
            })

    # Salespeople who sold this product
    sold_salespeople = set(s['salesperson'] for s in sales if s['product_id'] == pid)
    salespeople_list = list(sold_salespeople)

    return render_template('product.html',
                           product=p,
                           sold=sold,
                           remaining=remaining,
                           revenue=round(revenue, 2),
                           product_sales=product_sales,
                           salespeople_list=salespeople_list)

if __name__ == '__main__':
    app.run(debug=True)