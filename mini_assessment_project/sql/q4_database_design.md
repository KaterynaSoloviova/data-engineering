# Q4. Database Design 
```
Design schema for: 
1. Shipment tracking  
2. Product inventory  
3. Customer support tickets  
Requirements: 
• normalized design  
• primary keys  
• foreign keys  
• indexing recommendations  
```

## Shipment tracking
### SQL implementation
```sql
CREATE TABLE IF NOT EXISTS shipment_tracking (
	shipment_id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
 	shipment_date DATE,
 	recipient_name VARCHAR(100),
	recipient_street VARCHAR(50),
	recipient_city VARCHAR(50),
	recipient_post_index INTEGER, 
	recipient_country VARCHAR(50),
	status VARCHAR(50) CHECK (
	    status IN ('pending', 'shipped', 'in_transit', 'delivered', 'cancelled')
	)
);
```
### Indexing recommendations
Indexes on `order_id` are useful for improving joins between shipments and orders, on `status` - to help filter shipments by status, and for `shipment_date` - to help filter or sort shipments by date.

```sql
CREATE INDEX IF NOT EXISTS idx_shipment_tracking_order_id
    ON shipment_tracking(order_id);

CREATE INDEX IF NOT EXISTS idx_shipment_tracking_status
    ON shipment_tracking(status);

CREATE INDEX IF NOT EXISTS idx_shipment_tracking_shipment_date
    ON shipment_tracking(shipment_date);
```

### Normalized design (3NF)
The original table contains shipment information and recipient address information together. If a customer receives multiple shipments, their address may be repeated across multiple rows.
A normalized design can separate the data into three tables:

```sql

CREATE TABLE IF NOT EXISTS recipients (
    recipient_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    recipient_name VARCHAR(100) NOT NULL,
    recipient_street VARCHAR(100),
    recipient_city VARCHAR(50),
    recipient_post_index VARCHAR(20),
    recipient_country VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS shipment_tracking (
    shipment_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    recipient_id INTEGER NOT NULL REFERENCES recipients(recipient_id),
    shipment_date DATE,
    status VARCHAR(50)
        CHECK (status IN (
            'pending',
            'shipped',
            'in_transit',
            'delivered',
            'cancelled'
        ))
);

CREATE INDEX IF NOT EXISTS idx_shipment_order_id
    ON shipment_tracking(order_id);

CREATE INDEX IF NOT EXISTS idx_shipment_recipient_id
    ON shipment_tracking(recipient_id);

CREATE INDEX IF NOT EXISTS idx_shipment_status
    ON shipment_tracking(status);

CREATE INDEX IF NOT EXISTS idx_shipment_tracking_shipment_date
    ON shipment_tracking(shipment_date);
```
The new index on recipient_id  - to improve searches and joins involving recipients

## Product inventory
### SQL implementation

```sql
CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id INTEGER PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    location VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS inventory (
    product_id INTEGER REFERENCES products(product_id),
    warehouse_id INTEGER REFERENCES warehouses(warehouse_id),
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    PRIMARY KEY (product_id, warehouse_id)
);
```

### Indexing recommendations
Indexes on inventory.warehouse_id help retrieve inventory stored in a specific warehouse. The composite primary key on (product_id, warehouse_id) automatically creates an index that supports product lookups and joins using the leading product_id column.

```sql
CREATE INDEX IF NOT EXISTS idx_inventory_warehouse_id
    ON inventory(warehouse_id);
```

### Normalized design (3NF)
A single inventory table containing product details, warehouse details, and quantities could repeat the same information across multiple rows.
A normalized design separates the data into 2 tables:
- warehouses stores warehouse information.
- inventory stores the quantity of each product at each warehouse.

## Customer support tickets

### SQL implementation

```sql
CREATE TABLE IF NOT EXISTS support_agents (
    agent_id INTEGER PRIMARY KEY,
    agent_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL
        REFERENCES customers(customer_id),
    agent_id INTEGER
        REFERENCES support_agents(agent_id),
    subject VARCHAR(200) NOT NULL,
    status VARCHAR(50) NOT NULL
        CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
    priority VARCHAR(20) NOT NULL
        CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ticket_messages (
    message_id INTEGER PRIMARY KEY,
    ticket_id INTEGER NOT NULL
        REFERENCES tickets(ticket_id),
    sender_type VARCHAR(20) NOT NULL
        CHECK (sender_type IN ('customer', 'agent')),
    message_text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Indexing recommendations
Indexes on tickets.customer_id help retrieve tickets submitted by a particular customer. An index on tickets(agent_id, status) helps find tickets assigned to an agent by their current status. An index on tickets(status, created_at) helps filter tickets by status and sort them by creation date. An index on ticket_messages(ticket_id, created_at) helps retrieve messages for a ticket in chronological order.

```sql
CREATE INDEX IF NOT EXISTS idx_tickets_customer_id
    ON tickets(customer_id);

CREATE INDEX IF NOT EXISTS idx_tickets_agent_status
    ON tickets(agent_id, status);

CREATE INDEX IF NOT EXISTS idx_tickets_status_created_at
    ON tickets(status, created_at);

CREATE INDEX IF NOT EXISTS idx_ticket_messages_ticket_created_at
    ON ticket_messages(ticket_id, created_at);
```
### Normalized design (3NF)
If agent details, ticket information, and messages were stored in one table, customer and agent information would be repeated for every message. This would increase data duplication and make updates more difficult.

A normalized design separates the data into 3 tables:
- support_agents stores support agent information.
- tickets stores ticket details and references the customer and assigned agent.
- ticket_messages stores individual messages associated with each ticket.
