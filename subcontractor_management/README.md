# Subcontractor Management Module

## Overview
This Odoo module allows you to manage subcontractor agreements with contacts (partners), assign subcontracted items with product variants, and track weekly payments.

## Features

### 1. Subcontractor Agreements
- Create agreements with partners (subcontractors)
- Track start and end dates
- Monitor agreement states: Draft, Active, Completed, Cancelled
- View total agreement value, paid amount, and balance

### 2. Subcontractor Items
- Assign product variants to agreements
- Define quantity and unit price for each item
- Set quantity to add to inventory when balance reaches zero
- Support for product variants with different attributes

### 4. Raw Material Consumption
- Track raw materials consumed for subcontractor work
- Link consumption to specific agreements and partners
- Automatic inventory deduction when marked as done
- Calculate total cost of consumed materials

### 5. Payment Tracking
- Record payments against agreements
- Track payment dates and amounts
- Automatic balance calculation
- Inventory update when agreement is fully paid

### 6. Weekly Payment Wizard
- Select a subcontractor
- View all unpaid agreements with balances
- Create multiple payments at once
- Shows total value, paid amount, and balance for each agreement

## Installation

1. Copy the `subcontractor_management` folder to your Odoo addons directory
2. Update the apps list in Odoo
3. Install the "Subcontractor Management" module

## Dependencies
- base
- product
- stock

## Usage

### Creating a Subcontractor Agreement
1. Go to Subcontractors > Agreements
2. Click "Create"
3. Select a subcontractor (partner)
4. Set start date and optional end date
5. Add items in the "Items" tab
6. Click "Activate" to make the agreement active

### Adding Items to an Agreement
1. In the agreement form, go to the "Items" tab
2. Add products with their variants
3. Set quantity and unit price
4. Optionally set "Quantity to Add on Completion" for inventory updates
5. The total price is calculated automatically

### Recording Raw Material Consumption
1. Go to Subcontractors > Material Consumption
2. Click "Create"
3. Select consumption date
4. Optionally link to a subcontractor and agreement
5. Add material lines with product, quantity, and unit cost
6. Click "Confirm" to confirm the consumption
7. Click "Mark as Done" to consume materials from inventory

### Recording Payments
1. Go to Subcontractors > Payments
2. Click "Create"
3. Select an agreement
4. Enter payment date and amount
5. Click "Confirm Payment"

### Using the Weekly Payment Wizard
1. Go to Subcontractors > Weekly Payments
2. Select a subcontractor
3. The wizard shows all active agreements with unpaid balances
4. Enter payment amounts for each agreement
5. Click "Create Payments" to generate payment records

### Inventory Updates
When an agreement's balance reaches zero and a payment is confirmed:
- The system automatically updates inventory
- Products with "Quantity to Add on Completion" > 0 receive inventory
- Stock moves are created from Suppliers location to Stock location

## Technical Details

### Models
- `subcontractor.agreement`: Main agreement model
- `subcontractor.item`: Items/products in agreements
- `subcontractor.payment`: Payment records
- `raw.material.consumption`: Raw material consumption tracking
- `raw.material.consumption.line`: Lines in material consumption
- `weekly.payment.wizard`: Transient model for payment wizard
- `weekly.payment.wizard.line`: Lines in payment wizard

### Fields
Key computed fields:
- `total_value`: Sum of all item prices in agreement
- `total_paid`: Sum of all confirmed payments
- `balance`: Difference between total value and total paid

## License
This module is provided as-is for use with Odoo.
