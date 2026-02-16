# Module Summary

## Subcontractor Management Module

This Odoo module provides a comprehensive solution for managing subcontractor agreements, items, payments, and raw material consumption.

### Key Components

#### 1. Models

**Subcontractor Agreement** (`subcontractor.agreement`)
- Manages agreements with subcontractor partners
- Tracks dates, states, and financial information
- Computed fields for total value, paid amount, and balance
- Workflow states: Draft → Active → Completed/Cancelled

**Subcontractor Item** (`subcontractor.item`)
- Links product variants to agreements
- Tracks quantities, prices, and totals
- Supports automatic inventory updates on completion
- Enhanced product variant selector

**Subcontractor Payment** (`subcontractor.payment`)
- Records payments against agreements
- Automatically updates balances
- Triggers inventory updates when balance reaches zero
- Payment workflow: Draft → Confirmed/Cancelled

**Raw Material Consumption** (`raw.material.consumption`)
- Tracks materials consumed for subcontractor work
- Links to agreements and partners
- Automatic inventory deduction
- Workflow: Draft → Confirmed → Done/Cancelled

**Weekly Payment Wizard** (`weekly.payment.wizard`)
- Allows bulk payment creation
- Filters unpaid agreements by partner
- Shows detailed balance information

#### 2. Views

- Tree and form views for all models
- Editable tree views for efficient data entry
- Statusbar for workflow visualization
- Chatter integration for collaboration
- Enhanced product selectors

#### 3. Features

✅ **Agreement Management**
- Create agreements with partners
- Track multiple items per agreement
- Monitor financial status
- State management workflow

✅ **Product Variant Support**
- Enhanced selector showing variant attributes
- Search by variant attributes
- Catalog-style selection experience

✅ **Payment Tracking**
- Individual payment records
- Automatic balance calculation
- Weekly payment wizard for bulk operations
- Payment history and audit trail

✅ **Inventory Integration**
- Automatic inventory updates on completion
- Raw material consumption tracking
- Stock move generation
- Integration with Odoo stock module

✅ **Financial Tracking**
- Total agreement value calculation
- Running balance computation
- Payment history
- Cost tracking for materials

### Technical Details

**Dependencies:**
- base
- product
- stock

**Database Tables:**
- subcontractor_agreement
- subcontractor_item
- subcontractor_payment
- raw_material_consumption
- raw_material_consumption_line
- weekly_payment_wizard
- weekly_payment_wizard_line

**Sequences:**
- AGR/##### - Agreement references
- PAY/##### - Payment references
- RMC/##### - Material consumption references

**Security:**
- Access rights for all models
- Standard user permissions (read, write, create, unlink)

### Workflow

1. **Create Agreement**: Select partner, add items with variants
2. **Activate Agreement**: Move from draft to active state
3. **Record Payments**: Create payments as work progresses
4. **Track Materials**: Record raw material consumption
5. **Complete Agreement**: When balance reaches zero, inventory updates automatically
6. **Mark Complete**: Set agreement to completed state

### Files Structure

```
subcontractor_management/
├── __init__.py
├── __manifest__.py
├── README.md
├── INSTALLATION.md
├── data/
│   ├── sequence_data.xml
│   └── demo_data.xml
├── models/
│   ├── __init__.py
│   ├── subcontractor_agreement.py
│   ├── subcontractor_item.py
│   ├── subcontractor_payment.py
│   ├── raw_material_consumption.py
│   └── product_product.py
├── views/
│   ├── subcontractor_agreement_views.xml
│   ├── subcontractor_item_views.xml
│   ├── subcontractor_payment_views.xml
│   ├── raw_material_consumption_views.xml
│   └── menu_items.xml
├── wizard/
│   ├── __init__.py
│   ├── weekly_payment_wizard.py
│   └── weekly_payment_wizard_views.xml
├── security/
│   └── ir.model.access.csv
└── static/
    └── description/
        └── index.html
```

### Menu Structure

```
Subcontractors (Main Menu)
├── Agreements
├── Payments
├── Weekly Payments (Wizard)
├── Items
└── Material Consumption
```

### Future Enhancements

Potential improvements for future versions:
- Reporting and analytics dashboards
- Email notifications for payment reminders
- Integration with accounting module (when enterprise version available)
- Multi-currency support
- Document attachment management
- Advanced filtering and search options
- Gantt charts for agreement timelines
- Integration with project management

### Compatibility

- Odoo 14.0+
- Odoo 15.0+
- Odoo 16.0+
- Odoo 17.0+
- Odoo 19.0+

Note: Views have been updated to use `list` instead of `tree` for Odoo 19 compatibility.

### License

This module is provided as-is for use with Odoo.
