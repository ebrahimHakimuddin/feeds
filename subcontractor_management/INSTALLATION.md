# Installation and Testing Guide

## Installation Steps

### Prerequisites
- Odoo 14, 15, 16, 17, or 19 installed
- Access to Odoo addons directory
- Base, Product, and Stock modules installed

### Installation

1. **Copy the module to Odoo addons directory:**
   ```bash
   cp -r subcontractor_management /path/to/odoo/addons/
   ```

2. **Restart Odoo server:**
   ```bash
   sudo systemctl restart odoo
   # or
   ./odoo-bin -c /etc/odoo/odoo.conf
   ```

3. **Update Apps List:**
   - Log in to Odoo
   - Go to Apps menu
   - Click "Update Apps List"
   - Confirm the update

4. **Install the Module:**
   - Search for "Subcontractor Management"
   - Click "Install"

## Testing the Module

### Test 1: Create a Subcontractor Agreement

1. Go to **Subcontractors > Agreements**
2. Click **Create**
3. Fill in the details:
   - Partner: Select a partner/contact
   - Start Date: Today's date
   - End Date: One month from now
4. Click **Save**
5. Verify the agreement reference is auto-generated (e.g., AGR/00001)

### Test 2: Add Items to Agreement

1. Open the created agreement
2. Go to the **Items** tab
3. Click **Add a line**
4. Select a product variant
5. Enter:
   - Quantity: 10
   - Unit Price: 100
   - Quantity to Add on Completion: 10
6. Verify total price is calculated (1000)
7. Add another item if desired
8. Click **Save**
9. Verify the **Total Agreement Value** is updated

### Test 3: Product Variant Selector

1. When selecting a product in Items tab:
   - Type part of the product name
   - Verify variants are shown with their attributes
   - Example: "T-Shirt (Red, M)" instead of just "T-Shirt"
2. Search by variant attribute:
   - Type "Red" or "Large"
   - Verify products with those attributes appear

### Test 4: Activate Agreement

1. Click **Activate** button on the agreement
2. Verify state changes to "Active"

### Test 5: Create a Payment

1. Go to **Subcontractors > Payments**
2. Click **Create**
3. Select the agreement created earlier
4. Enter payment amount: 500
5. Click **Save** then **Confirm Payment**
6. Go back to the agreement
7. Verify:
   - Total Paid: 500
   - Balance: 500 (if total was 1000)

### Test 6: Weekly Payment Wizard

1. Go to **Subcontractors > Weekly Payments**
2. Select the subcontractor
3. Verify unpaid agreements appear with:
   - Total Value
   - Amount Paid
   - Balance
4. Enter payment amounts for one or more agreements
5. Click **Create Payments**
6. Go to **Subcontractors > Payments** to verify payments were created

### Test 7: Full Payment and Inventory Update

1. Create another payment for the remaining balance
2. Example: If balance is 500, create payment for 500
3. Click **Confirm Payment**
4. Go to **Inventory > Products**
5. Find the product from the agreement
6. Verify quantity increased by the "Quantity to Add on Completion" value
7. Check **Inventory > Operations > Stock Moves** for the move record

### Test 8: Raw Material Consumption

1. Go to **Subcontractors > Material Consumption**
2. Click **Create**
3. Fill in:
   - Consumption Date: Today
   - Partner: Select subcontractor
   - Agreement: Select an agreement (optional)
4. Add material lines:
   - Product: Select raw material
   - Quantity: 5
   - Unit Cost: 20
5. Verify Total Cost: 100
6. Click **Confirm**
7. Click **Mark as Done**
8. Check inventory for the raw material
9. Verify quantity decreased by consumed amount

### Test 9: Agreement Workflow

1. Create a new agreement in Draft state
2. Add items and verify total value
3. Activate the agreement
4. Create partial payments
5. Verify balance updates correctly
6. Create final payment to reach zero balance
7. Verify inventory updates
8. Mark agreement as Completed

### Test 10: Data Validation

1. Try to create payment greater than balance
2. Verify appropriate validation
3. Try to activate agreement without items
4. Create consumption without materials
5. Verify all computed fields update correctly

## Expected Results

After successful testing, you should be able to:

✅ Create and manage subcontractor agreements
✅ Add product variants with different attributes
✅ Track payments and calculate balances
✅ Use weekly payment wizard for bulk payments
✅ Automatically update inventory when balance reaches zero
✅ Track raw material consumption
✅ View comprehensive reports on agreements and payments

## Troubleshooting

### Module Not Appearing in Apps List
- Verify the module is in the correct addons directory
- Check Odoo config file for addons_path
- Restart Odoo server
- Update Apps List again

### Import Errors
- Check that all dependencies are installed:
  - base
  - product
  - stock
- Verify Python syntax in all .py files
- Check Odoo logs for specific error messages

### Views Not Loading
- Verify XML syntax in all view files
- Check for typos in model names
- Ensure ir.model.access.csv has correct entries
- Upgrade the module after changes

### Inventory Not Updating
- Ensure stock module is installed
- Check that products have "Storable Product" type
- Verify stock locations exist
- Check stock move records for errors

## Module Upgrade

After making changes to the module:

1. **Upgrade via UI:**
   - Go to Apps
   - Search for "Subcontractor Management"
   - Click "Upgrade"

2. **Upgrade via command line:**
   ```bash
   ./odoo-bin -c /etc/odoo/odoo.conf -u subcontractor_management -d your_database
   ```

## Support

For issues or questions:
- Check Odoo logs: `/var/log/odoo/odoo-server.log`
- Review module README.md
- Verify all prerequisites are met
