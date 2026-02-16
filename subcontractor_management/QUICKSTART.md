# Quick Start Guide

## Installation (5 minutes)

1. **Copy module to Odoo**
   ```bash
   cp -r subcontractor_management /path/to/odoo/addons/
   ```

2. **Restart Odoo**
   ```bash
   sudo systemctl restart odoo
   ```

3. **Install from UI**
   - Apps → Update Apps List
   - Search "Subcontractor Management"
   - Click Install

## First Use (10 minutes)

### 1. Create Your First Agreement

1. Go to **Subcontractors > Agreements**
2. Click **Create**
3. Fill in:
   - **Partner**: Select a subcontractor
   - **Start Date**: Today
4. Click **Save**

### 2. Add Items

1. Go to **Items** tab
2. Click **Add a line**
3. Select **Product** (try searching by variant attributes!)
4. Enter **Quantity** and **Unit Price**
5. Set **Quantity to Add on Completion** (optional)
6. Notice total is calculated automatically

### 3. Activate Agreement

1. Click **Activate** button
2. Note the state changes to "Active"

### 4. Record a Payment

**Option A: Direct Payment**
1. Go to **Subcontractors > Payments**
2. Click **Create**
3. Select agreement
4. Enter amount
5. Click **Confirm Payment**

**Option B: Weekly Payment Wizard** (Recommended)
1. Go to **Subcontractors > Weekly Payments**
2. Select subcontractor
3. See all unpaid agreements with balances
4. Enter payment amounts
5. Click **Create Payments**
6. Go to Payments menu and confirm them

### 5. Complete the Agreement

1. Pay the remaining balance
2. When you confirm the final payment:
   - Balance becomes 0
   - Inventory automatically updated!
3. Check **Inventory > Products** to verify

### 6. Track Material Consumption

1. Go to **Subcontractors > Material Consumption**
2. Click **Create**
3. Select partner and agreement (optional)
4. Add material lines
5. Click **Confirm** then **Mark as Done**
6. Materials deducted from inventory automatically

## Common Tasks

### View All Agreements for a Subcontractor
- Subcontractors > Agreements
- Filter by partner name

### Check Payment History
- Open an agreement
- Go to **Payments** tab
- See all payments with dates and amounts

### Find Products by Variant
When adding items:
- Type product name OR variant attribute
- Example: Search "Red" to find all red products

### Weekly Payment Processing
1. Weekly Payments wizard
2. Select subcontractor
3. See all open balances
4. Pay multiple agreements at once

## Tips & Tricks

💡 **Use the Weekly Payment Wizard** for faster processing

💡 **Set "Quantity to Add on Completion"** to auto-update inventory

💡 **Search products by variant attributes** for easier selection

💡 **Use Notes fields** to track additional information

💡 **Monitor balances** from the Agreements list view

## Menu Structure

```
Subcontractors
├── Agreements        (View/create agreements)
├── Payments          (View/create payments)
├── Weekly Payments   (Bulk payment wizard)
├── Items             (View all items)
└── Material Consumption (Track materials)
```

## Troubleshooting

**Module not appearing?**
- Check addons path in Odoo config
- Restart Odoo server
- Update Apps List

**Can't see inventory updates?**
- Ensure products are "Storable Product" type
- Check stock moves in Inventory

**Balance not updating?**
- Make sure payment is **Confirmed**
- Draft/Cancelled payments don't count

## Need Help?

📖 Read **INSTALLATION.md** for detailed testing guide
📖 Check **README.md** for feature overview
📖 See **DATA_MODEL.md** for how it works

---

**Happy Subcontractor Managing! 🎉**
