#!/usr/bin/env python3
"""
Example usage of PumlGenerator with different styles and detail levels.
Demonstrates how to generate PlantUML diagrams from JADN schemas.
"""

import os
from jadnutils.puml.puml_generator import PumlGenerator


def test_create_example_schema():
    """Create an example JADN schema for demonstration."""
    return {
        "meta": {
            "title": "E-Commerce System",
            "module": "ecommerce",
            "version": "1.0",
            "description": "Schema for an e-commerce system",
            "roots": ["Order", "Customer"]
        },
        "types": [
            ["Customer", "Record", [], "Customer information", [
                [1, "id", "String", [], "Customer ID"],
                [2, "name", "String", [], "Customer name"],
                [3, "email", "String", [], "Email address"],
                [4, "addresses", "Address-List", ["[0..*]"], "Customer addresses"],
                [5, "status", "CustomerStatus", [], "Customer status"]
            ]],
            
            ["Order", "Record", [], "Order information", [
                [1, "id", "String", [], "Order ID"],
                [2, "customer_id", "String", [], "Customer ID"],
                [3, "items", "OrderItem-List", ["[1..*]"], "Order items"],
                [4, "total", "Number", [], "Order total"],
                [5, "status", "OrderStatus", [], "Order status"],
                [6, "shipping_address", "Address", [], "Shipping address"],
                [7, "payment", "Payment", [], "Payment information"]
            ]],
            
            ["OrderItem", "Record", [], "Individual order item", [
                [1, "product_id", "String", [], "Product ID"],
                [2, "quantity", "Integer", ["[1..*]"], "Quantity ordered"],
                [3, "price", "Number", [], "Unit price"],
                [4, "product", "Product", [], "Product details"]
            ]],
            
            ["Product", "Record", [], "Product information", [
                [1, "id", "String", [], "Product ID"],
                [2, "name", "String", [], "Product name"],
                [3, "description", "String", ["[0..1]"], "Product description"],
                [4, "price", "Number", [], "Product price"],
                [5, "category", "Category", [], "Product category"],
                [6, "tags", "String-List", ["[0..*]"], "Product tags"]
            ]],
            
            ["Address", "Record", [], "Address information", [
                [1, "street", "String", [], "Street address"],
                [2, "city", "String", [], "City"],
                [3, "state", "String", [], "State/Province"],
                [4, "zip", "String", [], "ZIP/Postal code"],
                [5, "country", "String", [], "Country"]
            ]],
            
            ["Payment", "Choice", [], "Payment method", [
                [1, "credit_card", "CreditCard", [], "Credit card payment"],
                [2, "bank_transfer", "BankTransfer", [], "Bank transfer payment"],
                [3, "digital_wallet", "DigitalWallet", [], "Digital wallet payment"]
            ]],
            
            ["CreditCard", "Record", [], "Credit card information", [
                [1, "number", "String", [], "Card number"],
                [2, "expiry", "String", [], "Expiry date"],
                [3, "cvv", "String", [], "CVV code"],
                [4, "holder_name", "String", [], "Cardholder name"]
            ]],
            
            ["BankTransfer", "Record", [], "Bank transfer information", [
                [1, "account_number", "String", [], "Account number"],
                [2, "routing_number", "String", [], "Routing number"],
                [3, "bank_name", "String", [], "Bank name"]
            ]],
            
            ["DigitalWallet", "Record", [], "Digital wallet information", [
                [1, "wallet_id", "String", [], "Wallet ID"],
                [2, "provider", "WalletProvider", [], "Wallet provider"]
            ]],
            
            # Container types
            ["Address-List", "ArrayOf", ["*Address"], "List of addresses"],
            ["OrderItem-List", "ArrayOf", ["*OrderItem"], "List of order items"],
            ["String-List", "ArrayOf", ["*String"], "List of strings"],
            
            # Enumerations
            ["CustomerStatus", "Enumerated", [], "Customer status values", [
                [1, "active", "Active customer"],
                [2, "inactive", "Inactive customer"],
                [3, "suspended", "Suspended customer"]
            ]],
            
            ["OrderStatus", "Enumerated", [], "Order status values", [
                [1, "pending", "Pending order"],
                [2, "confirmed", "Confirmed order"],
                [3, "shipped", "Shipped order"],
                [4, "delivered", "Delivered order"],
                [5, "cancelled", "Cancelled order"]
            ]],
            
            ["Category", "Enumerated", [], "Product categories", [
                [1, "electronics", "Electronics"],
                [2, "clothing", "Clothing"],
                [3, "books", "Books"],
                [4, "home", "Home & Garden"],
                [5, "sports", "Sports & Outdoors"]
            ]],
            
            ["WalletProvider", "Enumerated", [], "Digital wallet providers", [
                [1, "paypal", "PayPal"],
                [2, "apple_pay", "Apple Pay"],
                [3, "google_pay", "Google Pay"],
                [4, "venmo", "Venmo"]
            ]]
        ]
    }


def test_generate_conceptual_diagram():
    """Generate a conceptual level PlantUML diagram."""
    schema = test_create_example_schema()
    
    style = {
        'detail': PumlGenerator.CONCEPTUAL,
        'show_links': True,
        'theme': 'blueprint',
        'title': 'E-Commerce System - Conceptual View',
        'class_style': 'class'
    }
    
    generator = PumlGenerator(schema, style)
    puml_source = generator.generate()
    
    print("=== CONCEPTUAL DIAGRAM ===")
    print(puml_source)
    print("\n" + "="*50 + "\n")
    
    return puml_source


def test_generate_logical_diagram():
    """Generate a logical level PlantUML diagram."""
    schema = test_create_example_schema()
    
    style = {
        'detail': PumlGenerator.LOGICAL,
        'show_links': True,
        'show_multiplicity': False,
        'theme': 'aws-orange',
        'title': 'E-Commerce System - Logical View',
        'class_style': 'entity'
    }
    
    generator = PumlGenerator(schema, style)
    puml_source = generator.generate()
    
    print("=== LOGICAL DIAGRAM ===")
    print(puml_source)
    print("\n" + "="*50 + "\n")
    
    return puml_source


def test_generate_detailed_diagram():
    """Generate a detailed informational PlantUML diagram."""
    schema = test_create_example_schema()
    
    style = {
        'detail': PumlGenerator.INFORMATIONAL,
        'show_links': True,
        'show_multiplicity': True,
        'title': 'E-Commerce System - Detailed View',
        'note_position': 'top',
        'relationship_style': '-->'
    }
    
    generator = PumlGenerator(schema, style)
    puml_source = generator.generate()
    
    print("=== DETAILED DIAGRAM ===")
    print(puml_source)
    print("\n" + "="*50 + "\n")
    
    return puml_source


def test_generate_no_links_diagram():
    """Generate a diagram without relationships."""
    schema = test_create_example_schema()
    
    style = {
        'detail': PumlGenerator.LOGICAL,
        'show_links': False,
        'title': 'E-Commerce System - Types Only',
        'class_style': 'interface',
        'theme': 'cerulean'
    }
    
    generator = PumlGenerator(schema, style)
    puml_source = generator.generate()
    
    print("=== NO LINKS DIAGRAM ===")
    print(puml_source)
    print("\n" + "="*50 + "\n")
    
    return puml_source


def test_save_all_examples():
    """Save all examples to files."""
    import os
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    schema = test_create_example_schema()
    
    examples = [
        ("conceptual", PumlGenerator.CONCEPTUAL, {'theme': 'blueprint'}),
        ("logical", PumlGenerator.LOGICAL, {'theme': 'aws-orange', 'class_style': 'entity'}),
        ("detailed", PumlGenerator.INFORMATIONAL, {'show_multiplicity': True}),
        ("no_links", PumlGenerator.LOGICAL, {'show_links': False, 'theme': 'cerulean'})
    ]
    
    for name, detail, extra_style in examples:
        style = {
            'detail': detail,
            'title': f'E-Commerce System - {name.title()} View'
        }
        style.update(extra_style)
        
        generator = PumlGenerator(schema, style)
        filename = os.path.join(output_dir, f"ecommerce_{name}.puml")
        generator.save(filename)
        print(f"Saved {filename}")


def test_demonstrate_png_output():
    """
    Demonstrate PlantUML source code generation capabilities.
    """
    print("\n" + "=" * 50)
    print("PlantUML Source Code Generation Examples")
    print("=" * 50)
    
    # Create a simple schema for demonstration
    simple_schema = {
        "info": {
            "package": "http://example.com/demo",
            "title": "Demo Schema",
            "version": "1.0"
        },
        "types": [
            ["User", "Record", [], "User information", [
                [1, "id", "String", [], "User ID"],
                [2, "name", "String", [], "Full name"],
                [3, "email", "String", [], "Email address"],
                [4, "profile", "UserProfile", ["[0..1]"], "User profile"]
            ]],
            ["UserProfile", "Record", [], "User profile details", [
                [1, "bio", "String", ["[0..1]"], "Biography"],
                [2, "avatar_url", "String", ["[0..1]"], "Avatar image URL"],
                [3, "preferences", "UserPreferences", [], "User preferences"]
            ]],
            ["UserPreferences", "Record", [], "User preferences", [
                [1, "theme", "String", [], "UI theme"],
                [2, "notifications", "Boolean", [], "Email notifications enabled"]
            ]]
        ]
    }
    
    generator = PumlGenerator(simple_schema)
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Generate PlantUML source
    print("\n1. PlantUML Source Generation")
    print("-" * 30)
    try:
        puml_source = generator.generate()
        print(f"✓ Generated {len(puml_source)} characters of PlantUML source")
        print("First few lines:")
        lines = puml_source.split('\n')
        for i, line in enumerate(lines[:5]):
            print(f"  {line}")
        print("  ...")
    except Exception as e:
        print(f"✗ Source generation failed: {e}")
    
    # 2. Save PlantUML source to file
    print("\n2. Save to File")
    print("-" * 15)
    try:
        puml_file = os.path.join(output_dir, 'demo.puml')
        generator.save(puml_file)
        print(f"✓ PlantUML source saved: {puml_file}")
    except Exception as e:
        print(f"✗ File save failed: {e}")
    
    # 3. Test different detail levels
    print("\n3. Different Detail Levels")
    print("-" * 26)
    detail_levels = [
        (PumlGenerator.CONCEPTUAL, "Conceptual"),
        (PumlGenerator.LOGICAL, "Logical"), 
        (PumlGenerator.INFORMATIONAL, "Informational")
    ]
    
    for detail, name in detail_levels:
        try:
            style = {'detail': detail, 'theme': None}
            gen = PumlGenerator(simple_schema, style)
            source = gen.generate()
            line_count = len(source.split('\n'))
            print(f"✓ {name}: {line_count} lines")
        except Exception as e:
            print(f"✗ {name}: {e}")
    
    # 4. Test with themes
    print("\n4. Theme Examples")
    print("-" * 15)
    themes = ['aws-orange', 'blueprint', 'cerulean', None]
    for theme in themes:
        try:
            style = {'theme': theme}
            gen = PumlGenerator(simple_schema, style)
            source = gen.generate()
            theme_name = theme or "No theme"
            print(f"✓ {theme_name}: Generated successfully")
        except Exception as e:
            theme_name = theme or "No theme"
            print(f"✗ {theme_name}: {e}")
    
    print(f"\nFiles saved to: {output_dir}")
    print("Tip: Use PlantUML tools to render the .puml files to images")
    print("Example: plantuml demo.puml")
    print("Or view online at: http://www.plantuml.com/plantuml/uml/")


if __name__ == "__main__":
    print("PlantUML Generator Examples")
    print("=" * 40)
    
    # Generate and display different diagram styles
    test_generate_conceptual_diagram()
    test_generate_logical_diagram()
    test_generate_detailed_diagram()
    test_generate_no_links_diagram()
    
    # Save examples to files
    test_save_all_examples()
    
    # Demonstrate PlantUML source generation functionality
    test_demonstrate_png_output()
    
    print("\nExamples completed!")
    print("\nTo view the PlantUML diagrams:")
    print("1. Install PlantUML: https://plantuml.com/starting")
    print("2. Use online viewer: http://www.plantuml.com/plantuml/uml/")
    print("3. Use VS Code PlantUML extension")
    print("4. Generate images: java -jar plantuml.jar output/*.puml")
    print("5. Copy .puml content to PlantUML online editor")