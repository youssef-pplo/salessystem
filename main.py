

from flask import Flask, render_template, abort
from collections import defaultdict
import json

app = Flask(__name__)

# Mock data (ensure you have the full list of 66 sales here)
# Mock data
products = [
    {'id': 1, 'name': 'لابتوب', 'price': 12000.00, 'initial_stock': 150},
    {'id': 2, 'name': 'هاتف ذكي', 'price': 7500.00, 'initial_stock': 300},
    {'id': 3, 'name': 'سماعات', 'price': 500.00, 'initial_stock': 500},
    {'id': 4, 'name': 'شاشة', 'price': 4000.00, 'initial_stock': 280},
    {'id': 5, 'name': 'لوحة مفاتيح', 'price': 300.00, 'initial_stock': 400},
]

clients = [
    {'id': 1, 'name': 'أحمد محمود', 'contact': 'ahmad@email.com'},
    {'id': 2, 'name': 'فاطمة علي', 'contact': 'fatima@email.com'},
    {'id': 3, 'name': 'محمد حسين', 'contact': 'mohamed@email.com'},
    {'id': 4, 'name': 'سارة إبراهيم', 'contact': 'sara@email.com'},
    {'id': 5, 'name': 'يوسف خالد', 'contact': 'youssef@email.com'},
]

sales = [
    {'id': 1, 'salesperson': 'علي حسن', 'product_id': 1, 'client_id': 1, 'quantity': 10, 'date': '2025-09-09'},
    {'id': 2, 'salesperson': 'منى صلاح', 'product_id': 2, 'client_id': 2, 'quantity': 5, 'date': '2025-09-08'},
    {'id': 3, 'salesperson': 'علي حسن', 'product_id': 1, 'client_id': 3, 'quantity': 15, 'date': '2025-09-09'},
    {'id': 4, 'salesperson': 'منى صلاح', 'product_id': 3, 'client_id': 1, 'quantity': 20, 'date': '2025-09-09'},
    {'id': 5, 'salesperson': 'علي حسن', 'product_id': 2, 'client_id': 3, 'quantity': 3, 'date': '2025-09-07'},
    {'id': 6, 'salesperson': 'خالد أمين', 'product_id': 4, 'client_id': 4, 'quantity': 8, 'date': '2025-09-09'},
    {'id': 7, 'salesperson': 'خالد أمين', 'product_id': 5, 'client_id': 5, 'quantity': 30, 'date': '2025-09-08'},
    {'id': 8, 'salesperson': 'منى صلاح', 'product_id': 4, 'client_id': 2, 'quantity': 2, 'date': '2025-09-09'},
    {'id': 9, 'salesperson': 'علي حسن', 'product_id': 3, 'client_id': 4, 'quantity': 12, 'date': '2025-09-06'},
    {'id': 10, 'salesperson': 'خالد أمين', 'product_id': 1, 'client_id': 5, 'quantity': 4, 'date': '2025-09-05'},
    {'id': 11, 'salesperson': 'منى صلاح', 'product_id': 2, 'client_id': 1, 'quantity': 7, 'date': '2025-09-09'},
    {'id': 12, 'salesperson': 'علي حسن', 'product_id': 5, 'client_id': 2, 'quantity': 25, 'date': '2025-09-04'},
    {'id': 13, 'salesperson': 'خالد أمين', 'product_id': 3, 'client_id': 3, 'quantity': 18, 'date': '2025-09-09'},
    {'id': 14, 'salesperson': 'منى صلاح', 'product_id': 1, 'client_id': 4, 'quantity': 6, 'date': '2025-09-03'},
    {'id': 15, 'salesperson': 'علي حسن', 'product_id': 4, 'client_id': 5, 'quantity': 11, 'date': '2025-09-02'},
    {'id': 16, 'salesperson': 'خالد أمين', 'product_id': 2, 'client_id': 1, 'quantity': 9, 'date': '2025-09-09'},
    {'id': 17, 'salesperson': 'منى صلاح', 'product_id': 5, 'client_id': 2, 'quantity': 22, 'date': '2025-09-01'},
    {'id': 18, 'salesperson': 'علي حسن', 'product_id': 3, 'client_id': 3, 'quantity': 14, 'date': '2025-08-31'},
    {'id': 19, 'salesperson': 'خالد أمين', 'product_id': 1, 'client_id': 4, 'quantity': 3, 'date': '2025-09-09'},
    {'id': 20, 'salesperson': 'منى صلاح', 'product_id': 4, 'client_id': 5, 'quantity': 1, 'date': '2025-08-30'},
    {'id': 21, 'salesperson': 'علي حسن', 'product_id': 2, 'client_id': 2, 'quantity': 13, 'date': '2025-09-09'},
    {'id': 22, 'salesperson': 'خالد أمين', 'product_id': 5, 'client_id': 1, 'quantity': 28, 'date': '2025-08-29'},
    {'id': 23, 'salesperson': 'منى صلاح', 'product_id': 3, 'client_id': 5, 'quantity': 16, 'date': '2025-08-28'},
    {'id': 24, 'salesperson': 'علي حسن', 'product_id': 1, 'client_id': 2, 'quantity': 8, 'date': '2025-09-09'},
    {'id': 25, 'salesperson': 'خالد أمين', 'product_id': 4, 'client_id': 3, 'quantity': 5, 'date': '2025-08-27'},
    {'id': 26, 'salesperson': 'منى صلاح', 'product_id': 2, 'client_id': 4, 'quantity': 10, 'date': '2025-08-26'},
    {'id': 27, 'salesperson': 'علي حسن', 'product_id': 5, 'client_id': 1, 'quantity': 35, 'date': '2025-09-09'},
    {'id': 28, 'salesperson': 'خالد أمين', 'product_id': 3, 'client_id': 2, 'quantity': 25, 'date': '2025-08-25'},
    {'id': 29, 'salesperson': 'منى صلاح', 'product_id': 1, 'client_id': 3, 'quantity': 2, 'date': '2025-08-24'},
    {'id': 30, 'salesperson': 'علي حسن', 'product_id': 4, 'client_id': 4, 'quantity': 7, 'date': '2025-09-09'},
    {'id': 31, 'salesperson': 'خالد أمين', 'product_id': 2, 'client_id': 5, 'quantity': 6, 'date': '2025-08-23'},
    {'id': 32, 'salesperson': 'منى صلاح', 'product_id': 5, 'client_id': 3, 'quantity': 40, 'date': '2025-08-22'},
    {'id': 33, 'salesperson': 'علي حسن', 'product_id': 3, 'client_id': 1, 'quantity': 30, 'date': '2025-09-09'},
    {'id': 34, 'salesperson': 'خالد أمين', 'product_id': 1, 'client_id': 2, 'quantity': 9, 'date': '2025-08-21'},
    {'id': 35, 'salesperson': 'منى صلاح', 'product_id': 4, 'client_id': 1, 'quantity': 3, 'date': '2025-08-20'},
    {'id': 36, 'salesperson': 'علي حسن', 'product_id': 2, 'client_id': 5, 'quantity': 11, 'date': '2025-09-09'},
    {'id': 37, 'salesperson': 'خالد أمين', 'product_id': 5, 'client_id': 4, 'quantity': 15, 'date': '2025-08-19'},
    {'id': 38, 'salesperson': 'منى صلاح', 'product_id': 3, 'client_id': 2, 'quantity': 28, 'date': '2025-08-18'},
    {'id': 39, 'salesperson': 'علي حسن', 'product_id': 1, 'client_id': 1, 'quantity': 1, 'date': '2025-09-09'},
    {'id': 40, 'salesperson': 'خالد أمين', 'product_id': 4, 'client_id': 5, 'quantity': 10, 'date': '2025-08-17'},
    {'id': 41, 'salesperson': 'منى صلاح', 'product_id': 2, 'client_id': 3, 'quantity': 14, 'date': '2025-08-16'},
    {'id': 42, 'salesperson': 'علي حسن', 'product_id': 5, 'client_id': 4, 'quantity': 18, 'date': '2025-09-09'},
    {'id': 43, 'salesperson': 'خالد أمين', 'product_id': 3, 'client_id': 1, 'quantity': 21, 'date': '2025-08-15'},
    {'id': 44, 'salesperson': 'منى صلاح', 'product_id': 1, 'client_id': 5, 'quantity': 5, 'date': '2025-08-14'},
    {'id': 45, 'salesperson': 'علي حسن', 'product_id': 4, 'client_id': 2, 'quantity': 9, 'date': '2025-09-09'},
    {'id': 46, 'salesperson': 'خالد أمين', 'product_id': 2, 'client_id': 3, 'quantity': 8, 'date': '2025-08-13'},
    {'id': 47, 'salesperson': 'منى صلاح', 'product_id': 5, 'client_id': 1, 'quantity': 33, 'date': '2025-08-12'},
    {'id': 48, 'salesperson': 'علي حسن', 'product_id': 3, 'client_id': 5, 'quantity': 24, 'date': '2025-09-09'},
    {'id': 49, 'salesperson': 'خالد أمين', 'product_id': 1, 'client_id': 3, 'quantity': 7, 'date': '2025-08-11'},
    {'id': 50, 'salesperson': 'منى صلاح', 'product_id': 4, 'client_id': 4, 'quantity': 6, 'date': '2025-08-10'},
    {'id': 51, 'salesperson': 'علي حسن', 'product_id': 2, 'client_id': 1, 'quantity': 12, 'date': '2025-09-09'},
    {'id': 52, 'salesperson': 'خالد أمين', 'product_id': 5, 'client_id': 2, 'quantity': 20, 'date': '2025-08-09'},
    {'id': 53, 'salesperson': 'منى صلاح', 'product_id': 3, 'client_id': 4, 'quantity': 26, 'date': '2025-08-08'},
    {'id': 54, 'salesperson': 'علي حسن', 'product_id': 1, 'client_id': 5, 'quantity': 11, 'date': '2025-09-09'},
    {'id': 55, 'salesperson': 'خالد أمين', 'product_id': 4, 'client_id': 1, 'quantity': 4, 'date': '2025-08-07'},
    {'id': 56, 'salesperson': 'منى صلاح', 'product_id': 2, 'client_id': 2, 'quantity': 15, 'date': '2025-08-06'},
    {'id': 57, 'salesperson': 'علي حسن', 'product_id': 5, 'client_id': 3, 'quantity': 27, 'date': '2025-09-09'},
    {'id': 58, 'salesperson': 'خالد أمين', 'product_id': 3, 'client_id': 5, 'quantity': 19, 'date': '2025-08-05'},
    {'id': 59, 'salesperson': 'منى صلاح', 'product_id': 1, 'client_id': 1, 'quantity': 10, 'date': '2025-08-04'},
    {'id': 60, 'salesperson': 'علي حسن', 'product_id': 4, 'client_id': 3, 'quantity': 12, 'date': '2025-09-09'},
    {'id': 61, 'salesperson': 'خالد أمين', 'product_id': 2, 'client_id': 4, 'quantity': 1, 'date': '2025-08-03'},
    {'id': 62, 'salesperson': 'منى صلاح', 'product_id': 5, 'client_id': 5, 'quantity': 45, 'date': '2025-08-02'},
    {'id': 63, 'salesperson': 'علي حسن', 'product_id': 3, 'client_id': 2, 'quantity': 32, 'date': '2025-09-09'},
    {'id': 64, 'salesperson': 'خالد أمين', 'product_id': 1, 'client_id': 1, 'quantity': 13, 'date': '2025-08-01'},
    {'id': 65, 'salesperson': 'منى صلاح', 'product_id': 4, 'client_id': 2, 'quantity': 14, 'date': '2025-07-31'},
    {'id': 66, 'salesperson': 'علي حسن', 'product_id': 2, 'client_id': 4, 'quantity': 16, 'date': '2025-09-09'},
]

@app.route('/')
def dashboard():
    today = '2025-09-09'

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
    best_product = 'لا يوجد'
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

    # Clients table
    client_purchases = {}
    for s in sorted(sales, key=lambda x: x['date'], reverse=True):
        cid = s['client_id']
        if cid not in client_purchases:
            p_name = next(p['name'] for p in products if p['id'] == s['product_id'])
            client_purchases[cid] = p_name
    clients_table = []
    for c in clients:
        last_product = client_purchases.get(c['id'], 'لا يوجد')
        clients_table.append({
            'name': c['name'],
            'contact': c['contact'],
            'last_product': last_product
        })

    # --- Chart Data ---
    # Sales per salesperson
    sales_by_person = defaultdict(float)
    for s in sales_table:
        sales_by_person[s['salesperson']] += s['total']
    
    # Sales per product
    sales_by_product_revenue = defaultdict(float)
    for s in sales_table:
        sales_by_product_revenue[s['product']] += s['total']

    # Daily sales trend
    sales_by_date = defaultdict(float)
    for s in sales_table:
        sales_by_date[s['date']] += s['total']
    
    sorted_dates = sorted(sales_by_date.items())
    
    chart_data = {
        "sales_by_person": {
            "labels": list(sales_by_person.keys()),
            "data": list(sales_by_person.values())
        },
        "sales_by_product": {
            "labels": list(sales_by_product_revenue.keys()),
            "data": list(sales_by_product_revenue.values())
        },
        "sales_trend": {
            "labels": [date for date, total in sorted_dates],
            "data": [total for date, total in sorted_dates]
        }
    }

    return render_template('dashboard.html',
                           total_sales_today=round(total_sales_today, 2),
                           num_clients=num_clients,
                           best_product=best_product,
                           total_remaining=total_remaining,
                           sales_table=sales_table,
                           inventory_table=inventory_table,
                           clients_table=clients_table,
                           chart_data=json.dumps(chart_data))

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

    # Salespeople stats for this product
    salespeople_stats = {}
    for s in sales:
        if s['product_id'] == pid:
            name = s['salesperson']
            if name not in salespeople_stats:
                salespeople_stats[name] = {
                    'name': name,
                    'total_quantity': 0,
                    'total_revenue': 0,
                    'last_sale_date': '1970-01-01'
                }
            
            salespeople_stats[name]['total_quantity'] += s['quantity']
            salespeople_stats[name]['total_revenue'] += s['quantity'] * p['price']
            if s['date'] > salespeople_stats[name]['last_sale_date']:
                salespeople_stats[name]['last_sale_date'] = s['date']
    
    salespeople_list = list(salespeople_stats.values())

    return render_template('product.html',
                           product=p,
                           sold=sold,
                           remaining=remaining,
                           revenue=round(revenue, 2),
                           product_sales=product_sales,
                           salespeople_list=salespeople_list)

if __name__ == '__main__':
    app.run(debug=True)