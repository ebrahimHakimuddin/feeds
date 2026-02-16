# Data Model Relationships

## Entity Relationship Overview

```
┌─────────────────────┐
│   res.partner       │
│   (Subcontractor)   │
└──────────┬──────────┘
           │
           │ 1:N
           ▼
┌─────────────────────────────┐
│  subcontractor.agreement    │
│  ─────────────────────────  │
│  - name                     │
│  - partner_id               │
│  - date_start/date_end      │
│  - state                    │
│  - total_value (computed)   │
│  - total_paid (computed)    │
│  - balance (computed)       │
└──────────┬──────────────────┘
           │
           ├──────────┐
           │          │
           │ 1:N      │ 1:N
           ▼          ▼
┌──────────────────┐  ┌──────────────────────────┐
│subcontractor.item│  │ subcontractor.payment    │
│──────────────────│  │ ──────────────────────── │
│- product_id      │  │ - name                   │
│- quantity        │  │ - payment_date           │
│- unit_price      │  │ - amount                 │
│- total_price     │  │ - state                  │
│- quantity_to_add │  │                          │
└────┬─────────────┘  └──────────────────────────┘
     │
     │ N:1
     ▼
┌──────────────────┐
│ product.product  │
│ (with variants)  │
└──────────────────┘


┌─────────────────────────────┐
│ raw.material.consumption    │
│ ─────────────────────────── │
│ - name                      │
│ - consumption_date          │
│ - agreement_id (optional)   │
│ - partner_id                │
│ - state                     │
│ - total_cost (computed)     │
└──────────┬──────────────────┘
           │
           │ 1:N
           ▼
┌──────────────────────────────────┐
│raw.material.consumption.line     │
│──────────────────────────────────│
│- product_id                      │
│- quantity                        │
│- unit_cost                       │
│- total_cost (computed)           │
└──────────┬───────────────────────┘
           │
           │ N:1
           ▼
┌──────────────────┐
│ product.product  │
│ (raw materials)  │
└──────────────────┘
```

## Model Descriptions

### Core Models

#### 1. subcontractor.agreement
**Purpose**: Main container for a subcontractor agreement

**Key Fields**:
- `partner_id`: Link to the subcontractor (res.partner)
- `item_ids`: One2many to subcontractor.item
- `payment_ids`: One2many to subcontractor.payment
- `total_value`: Computed sum of all item total_prices
- `total_paid`: Computed sum of all payment amounts
- `balance`: Computed as total_value - total_paid

**States**: draft → active → completed (or cancelled)

**Business Logic**:
- Total value automatically calculated from items
- Balance updated automatically when payments are added
- When balance reaches 0, triggers inventory update

#### 2. subcontractor.item
**Purpose**: Line items in an agreement with product variants

**Key Fields**:
- `agreement_id`: Link to parent agreement
- `product_id`: Link to product.product (variant)
- `quantity`: Quantity of this item
- `unit_price`: Price per unit
- `total_price`: Computed as quantity × unit_price
- `quantity_to_add`: Qty to add to inventory when complete

**Business Logic**:
- Automatically suggests product's standard price
- Total price computed automatically
- When agreement balance reaches 0, quantity_to_add is added to inventory

#### 3. subcontractor.payment
**Purpose**: Payment transactions against agreements

**Key Fields**:
- `agreement_id`: Link to the agreement being paid
- `amount`: Payment amount
- `payment_date`: When payment was made
- `state`: draft/confirmed/cancelled

**States**: draft → confirmed (or cancelled)

**Business Logic**:
- Updates agreement's total_paid when confirmed
- Checks if balance reaches 0 and triggers inventory update
- Creates stock moves for completed items

#### 4. raw.material.consumption
**Purpose**: Track raw materials consumed for work

**Key Fields**:
- `partner_id`: Subcontractor who used materials
- `agreement_id`: Optional link to specific agreement
- `line_ids`: One2many to consumption lines
- `total_cost`: Computed sum of line costs

**States**: draft → confirmed → done (or cancelled)

**Business Logic**:
- When marked as "done", creates stock moves to consume materials
- Materials moved from stock to production/scrapped location

#### 5. raw.material.consumption.line
**Purpose**: Individual material items consumed

**Key Fields**:
- `product_id`: The material product
- `quantity`: Quantity consumed
- `unit_cost`: Cost per unit
- `total_cost`: Computed as quantity × unit_cost

### Helper Models

#### 6. weekly.payment.wizard
**Purpose**: Transient model for bulk payment creation

**Key Fields**:
- `partner_id`: Filter by subcontractor
- `agreement_line_ids`: Lines showing unpaid agreements

**Business Logic**:
- Loads all active agreements with balance > 0
- Allows entering payment amounts for multiple agreements
- Creates payment records in batch

#### 7. weekly.payment.wizard.line
**Purpose**: Lines in the payment wizard

**Key Fields**:
- `agreement_id`: The agreement
- `total_value`, `total_paid`, `balance`: Read-only display
- `payment_amount`: User-entered amount to pay

### Extended Models

#### 8. product.product (inherited)
**Purpose**: Enhanced product selection for variants

**Enhancements**:
- Custom name_get showing variant attributes clearly
- Enhanced search to find products by variant attributes
- Context-aware display for subcontractor views

## Computed Fields Flow

```
Item 1: qty=10, price=100 → total_price=1000
Item 2: qty=5,  price=200 → total_price=1000
                              ↓
                    Agreement.total_value = 2000

Payment 1: amount=500
Payment 2: amount=700
           ↓
    Agreement.total_paid = 1200

Agreement.balance = total_value - total_paid
                  = 2000 - 1200
                  = 800
```

## Inventory Update Flow

```
1. Agreement has balance > 0
2. Payment created and confirmed
3. Agreement.balance recalculated
4. If balance <= 0.01:
   For each item with quantity_to_add > 0:
     - Create stock.move
     - Source: Suppliers location
     - Destination: Stock location
     - Quantity: item.quantity_to_add
     - Confirm and execute move
```

## Material Consumption Flow

```
1. Create consumption record
2. Add material lines
3. Confirm consumption
4. Mark as Done
5. For each line:
   - Create stock.move
   - Source: Stock location
   - Destination: Production/Scrapped location
   - Quantity: line.quantity
   - Confirm and execute move
```

## Access Control

All models accessible to `base.group_user` with full permissions:
- Read
- Write
- Create
- Unlink

## Sequences

- `subcontractor.agreement`: AGR/00001, AGR/00002, ...
- `subcontractor.payment`: PAY/00001, PAY/00002, ...
- `raw.material.consumption`: RMC/00001, RMC/00002, ...

## Inheritance

Models using `mail.thread` and `mail.activity.mixin`:
- subcontractor.agreement
- subcontractor.payment
- raw.material.consumption

This provides:
- Message/comment threads
- Activity tracking
- Follower management
- Email integration
