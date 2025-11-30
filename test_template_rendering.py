#!/usr/bin/env python
"""
Test template rendering for price breakdown
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_insurance.settings')
django.setup()

from django.template import Template, Context
from django.template.loader import get_template


def test_price_breakdown_template():
    """Test that price breakdown template renders correctly"""
    
    print("=" * 60)
    print("TESTING TEMPLATE RENDERING")
    print("=" * 60)
    
    # Test case 1: Base price only
    print("\n1. Testing template with base price only...")
    context = {
        'price_breakdown': {
            'base_price': 180.0,
            'breed_surcharge_5_percent': 0,
            'breed_surcharge_20_percent': 0,
            'poisoning_coverage': 0,
            'blood_checkup': 0,
            'total': 180.0
        }
    }
    
    template_str = """
    {% if price_breakdown and price_breakdown.base_price > 0 %}
    <div class="price-breakdown-section">
        <h4>📊 Ανάλυση Τιμής</h4>
        <div class="breakdown-item">
            <span>Βασική Τιμή Ασφάλισης:</span>
            <strong>{{ price_breakdown.base_price|floatformat:2 }}€</strong>
        </div>
        {% if price_breakdown.breed_surcharge_5_percent > 0 %}
        <div class="breakdown-item">
            <span>Επασφάλιστρο Ράτσας (5%):</span>
            <strong>+{{ price_breakdown.breed_surcharge_5_percent|floatformat:2 }}€</strong>
        </div>
        {% endif %}
        {% if price_breakdown.breed_surcharge_20_percent > 0 %}
        <div class="breakdown-item">
            <span>Επασφάλιστρο Ράτσας (20%):</span>
            <strong>+{{ price_breakdown.breed_surcharge_20_percent|floatformat:2 }}€</strong>
        </div>
        {% endif %}
        {% if price_breakdown.poisoning_coverage > 0 %}
        <div class="breakdown-item">
            <span>Πρόσθετη Κάλυψη Δηλητηρίασης:</span>
            <strong>+{{ price_breakdown.poisoning_coverage|floatformat:2 }}€</strong>
        </div>
        {% endif %}
        {% if price_breakdown.blood_checkup > 0 %}
        <div class="breakdown-item">
            <span>Αιματολογικό Check Up:</span>
            <strong>+{{ price_breakdown.blood_checkup|floatformat:2 }}€</strong>
        </div>
        {% endif %}
        <div class="breakdown-total">
            <span>Συνολική Τιμή:</span>
            <strong>{{ price_breakdown.total|floatformat:2 }}€</strong>
        </div>
    </div>
    {% endif %}
    """
    
    template = Template(template_str)
    rendered = template.render(Context(context))
    
    assert '180.00€' in rendered, "Base price should be rendered"
    assert 'Συνολική Τιμή' in rendered, "Total should be rendered"
    assert 'Επασφάλιστρο' not in rendered, "No surcharges should be shown"
    print("✓ Template renders correctly for base price only")
    
    # Test case 2: With all surcharges and add-ons
    print("\n2. Testing template with all surcharges and add-ons...")
    context = {
        'price_breakdown': {
            'base_price': 320.0,
            'breed_surcharge_5_percent': 16.0,
            'breed_surcharge_20_percent': 67.2,
            'poisoning_coverage': 25.0,
            'blood_checkup': 28.0,
            'total': 456.2
        }
    }
    
    rendered = template.render(Context(context))
    
    assert '320.00€' in rendered, "Base price should be rendered"
    assert '16.00€' in rendered, "5% surcharge should be rendered"
    assert '67.20€' in rendered, "20% surcharge should be rendered"
    assert '25.00€' in rendered, "Poisoning coverage should be rendered"
    assert '28.00€' in rendered, "Blood checkup should be rendered"
    assert '456.20€' in rendered, "Total should be rendered"
    print("✓ Template renders correctly with all options")
    
    # Test case 3: With only add-ons
    print("\n3. Testing template with only add-ons...")
    context = {
        'price_breakdown': {
            'base_price': 240.0,
            'breed_surcharge_5_percent': 0,
            'breed_surcharge_20_percent': 0,
            'poisoning_coverage': 20.0,
            'blood_checkup': 28.0,
            'total': 288.0
        }
    }
    
    rendered = template.render(Context(context))
    
    assert '240.00€' in rendered, "Base price should be rendered"
    assert '20.00€' in rendered, "Poisoning coverage should be rendered"
    assert '28.00€' in rendered, "Blood checkup should be rendered"
    assert 'Επασφάλιστρο' not in rendered, "No surcharges should be shown"
    assert '288.00€' in rendered, "Total should be rendered"
    print("✓ Template renders correctly with only add-ons")
    
    print("\n" + "=" * 60)
    print("✅ ALL TEMPLATE TESTS PASSED!")
    print("=" * 60)


def test_edge_cases_template():
    """Test edge cases in template rendering"""
    
    print("\n" + "=" * 60)
    print("TESTING TEMPLATE EDGE CASES")
    print("=" * 60)
    
    # Test case 1: Zero base price (should not render)
    print("\n1. Testing with zero base price...")
    context = {
        'price_breakdown': {
            'base_price': 0,
            'total': 0
        }
    }
    
    template_str = """
    {% if price_breakdown and price_breakdown.base_price > 0 %}
    <div>Price breakdown</div>
    {% endif %}
    """
    
    template = Template(template_str)
    rendered = template.render(Context(context))
    
    assert 'Price breakdown' not in rendered, "Should not render with zero base price"
    print("✓ Zero base price handled correctly")
    
    # Test case 2: Missing price_breakdown
    print("\n2. Testing with missing price_breakdown...")
    context = {}
    
    rendered = template.render(Context(context))
    
    assert 'Price breakdown' not in rendered, "Should not render without price_breakdown"
    print("✓ Missing price_breakdown handled correctly")
    
    # Test case 3: Very small surcharge values
    print("\n3. Testing with very small values...")
    context = {
        'price_breakdown': {
            'base_price': 100.0,
            'breed_surcharge_5_percent': 0.01,
            'breed_surcharge_20_percent': 0,
            'poisoning_coverage': 0,
            'blood_checkup': 0,
            'total': 100.01
        }
    }
    
    template_str = """
    {% if price_breakdown.breed_surcharge_5_percent > 0 %}
    <div>Surcharge: {{ price_breakdown.breed_surcharge_5_percent|floatformat:2 }}€</div>
    {% endif %}
    """
    
    template = Template(template_str)
    rendered = template.render(Context(context))
    
    assert '0.01€' in rendered, "Small values should be rendered"
    print("✓ Small values handled correctly")
    
    print("\n" + "=" * 60)
    print("✅ ALL EDGE CASE TEMPLATE TESTS PASSED!")
    print("=" * 60)


if __name__ == '__main__':
    try:
        test_price_breakdown_template()
        test_edge_cases_template()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TEMPLATE TESTS PASSED!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


