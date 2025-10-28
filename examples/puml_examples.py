#!/usr/bin/env python3
"""
Example usage of PumlGenerator with different styles and detail levels.
Demonstrates how to generate PlantUML diagrams from JADN schemas.
"""

import os
from jadnutils.puml.puml_generator import PumlGenerator


def create_example_schema():
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


def generate_conceptual_diagram():
    """Generate a conceptual level PlantUML diagram."""
    schema = create_example_schema()
    
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


def generate_logical_diagram():
    """Generate a logical level PlantUML diagram."""
    schema = create_example_schema()
    
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


def generate_detailed_diagram():
    """Generate a detailed informational PlantUML diagram."""
    schema = create_example_schema()
    
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


def generate_no_links_diagram():
    """Generate a diagram without relationships."""
    schema = create_example_schema()
    
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


def save_all_examples():
    """Save all examples to files."""
    import os
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    schema = create_example_schema()
    
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


def demonstrate_png_output():
    """
    Demonstrate PNG and other image format output capabilities.
    """
    print("\n" + "=" * 50)
    print("PNG and Image Format Output Examples")
    print("=" * 50)
    
    # Create a simple schema for demonstration
    simple_schema = {
        "info": {
            "package": "http://example.com/demo",
            "title": "PNG Demo Schema",
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
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Generate URL for online viewing
    print("\n1. Online PlantUML URL Generation")
    print("-" * 35)
    try:
        url = generator.generate_url(output_format='png')
        print(f"PlantUML PNG URL: {url}")
        print("   Copy this URL to your browser to view the diagram")
    except Exception as e:
        print(f"URL generation failed: {e}")
    
    # 2. Generate PNG locally or via web service
    print("\n2. PNG Generation")
    print("-" * 17)
    try:
        png_data = generator.generate(output_format='png')
        png_file = os.path.join(output_dir, 'png_demo.png')
        with open(png_file, 'wb') as f:
            f.write(png_data)
        print(f"✓ PNG saved: {png_file} ({len(png_data):,} bytes)")
        print("  Note: Uses web service if PlantUML not locally installed")
    except Exception as e:
        print(f"✗ PNG generation failed: {e}")
    
    # 3. Generate SVG
    print("\n3. SVG Generation")
    print("-" * 17)
    try:
        svg_data = generator.generate(output_format='svg')
        svg_file = os.path.join(output_dir, 'png_demo.svg')
        with open(svg_file, 'wb') as f:
            f.write(svg_data)
        print(f"✓ SVG saved: {svg_file} ({len(svg_data):,} bytes)")
    except Exception as e:
        print(f"✗ SVG generation failed: {e}")
    
    # 4. Auto-detection from file extension
    print("\n4. Format Auto-Detection")
    print("-" * 25)
    try:
        # Save as PNG using auto-detection
        auto_png = os.path.join(output_dir, 'auto_detected.png')
        generator.save(auto_png)
        print(f"✓ Auto-detected PNG: {auto_png}")
        
        # Save as PlantUML source
        auto_puml = os.path.join(output_dir, 'auto_detected.puml')
        generator.save(auto_puml)
        print(f"✓ Auto-detected PUML: {auto_puml}")
        
    except Exception as e:
        print(f"✗ Auto-detection failed: {e}")
    
    # 5. Multiple formats comparison
    print("\n5. Multiple Format Comparison")
    print("-" * 30)
    formats = ['png', 'svg', 'txt']
    for fmt in formats:
        try:
            data = generator.generate(output_format=fmt)
            size = len(data)
            print(f"✓ {fmt.upper()}: {size:,} bytes")
        except Exception as e:
            print(f"✗ {fmt.upper()}: {e}")
    
    print(f"\nFiles saved to: {output_dir}")
    print("Tip: PNG/SVG formats work best for documentation and presentations")


if __name__ == "__main__":
    print("PlantUML Generator Examples")
    print("=" * 40)
    
    # Generate and display different diagram styles
    generate_conceptual_diagram()
    generate_logical_diagram()
    generate_detailed_diagram()
    generate_no_links_diagram()
    
    # Save examples to files
    save_all_examples()
    
    # Demonstrate new PNG output functionality
    demonstrate_png_output()
    
    print("\nExamples completed!")
    print("\nTo view the PlantUML diagrams:")
    print("1. Install PlantUML: https://plantuml.com/starting")
    print("2. Use online viewer: http://www.plantuml.com/plantuml/uml/")
    print("3. Use VS Code PlantUML extension")
    print("4. Generate images: java -jar plantuml.jar output/*.puml")
    print("5. Or use the new PNG generation: generator.generate(output_format='png')")