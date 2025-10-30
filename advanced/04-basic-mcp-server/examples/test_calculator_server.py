#!/usr/bin/env python3
"""
Tests for Calculator MCP Server

This file demonstrates how to write tests for MCP servers using pytest.
These are unit tests for the helper functions and calculation logic.

To run these tests:
    pytest test_calculator_server.py
    pytest test_calculator_server.py -v  # Verbose output
    pytest test_calculator_server.py -k test_add  # Run specific test

To run with coverage:
    pytest test_calculator_server.py --cov=calculator_server
"""

import pytest
from calculator_server import (
    validate_number,
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers
)


# ============================================================================
# VALIDATION TESTS
# ============================================================================

class TestValidateNumber:
    """Tests for the validate_number function."""
    
    def test_validate_integer(self):
        """Test validation of integer values."""
        result = validate_number(42, "test")
        assert result == 42.0
        assert isinstance(result, float)
    
    def test_validate_float(self):
        """Test validation of float values."""
        result = validate_number(3.14, "test")
        assert result == 3.14
        assert isinstance(result, float)
    
    def test_validate_string_number(self):
        """Test conversion of string numbers."""
        result = validate_number("123", "test")
        assert result == 123.0
    
    def test_validate_string_float(self):
        """Test conversion of string floats."""
        result = validate_number("3.14", "test")
        assert result == 3.14
    
    def test_validate_negative_number(self):
        """Test validation of negative numbers."""
        result = validate_number(-42, "test")
        assert result == -42.0
    
    def test_validate_zero(self):
        """Test validation of zero."""
        result = validate_number(0, "test")
        assert result == 0.0
    
    def test_invalid_string(self):
        """Test rejection of non-numeric strings."""
        with pytest.raises(ValueError) as exc_info:
            validate_number("not a number", "test_param")
        assert "test_param" in str(exc_info.value)
        assert "must be a number" in str(exc_info.value)
    
    def test_invalid_type_none(self):
        """Test rejection of None."""
        with pytest.raises(ValueError) as exc_info:
            validate_number(None, "test_param")
        assert "must be a number" in str(exc_info.value)
    
    def test_invalid_type_list(self):
        """Test rejection of list."""
        with pytest.raises(ValueError):
            validate_number([1, 2, 3], "test_param")
    
    def test_invalid_type_dict(self):
        """Test rejection of dict."""
        with pytest.raises(ValueError):
            validate_number({"value": 42}, "test_param")


# ============================================================================
# ADDITION TESTS
# ============================================================================

class TestAddNumbers:
    """Tests for the add_numbers function."""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add_numbers(5, 3) == 8
    
    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert add_numbers(-5, -3) == -8
    
    def test_add_positive_and_negative(self):
        """Test adding positive and negative."""
        assert add_numbers(5, -3) == 2
        assert add_numbers(-5, 3) == -2
    
    def test_add_with_zero(self):
        """Test adding with zero."""
        assert add_numbers(0, 5) == 5
        assert add_numbers(5, 0) == 5
        assert add_numbers(0, 0) == 0
    
    def test_add_floats(self):
        """Test adding floating point numbers."""
        result = add_numbers(1.5, 2.3)
        assert abs(result - 3.8) < 0.0001  # Account for floating point precision
    
    def test_add_large_numbers(self):
        """Test adding very large numbers."""
        assert add_numbers(1e10, 1e10) == 2e10
    
    def test_add_very_small_numbers(self):
        """Test adding very small numbers."""
        result = add_numbers(0.0001, 0.0002)
        assert abs(result - 0.0003) < 1e-10


# ============================================================================
# SUBTRACTION TESTS
# ============================================================================

class TestSubtractNumbers:
    """Tests for the subtract_numbers function."""
    
    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        assert subtract_numbers(10, 3) == 7
    
    def test_subtract_to_negative(self):
        """Test subtraction resulting in negative."""
        assert subtract_numbers(3, 10) == -7
    
    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers."""
        assert subtract_numbers(-5, -3) == -2
        assert subtract_numbers(-3, -5) == 2
    
    def test_subtract_with_zero(self):
        """Test subtraction with zero."""
        assert subtract_numbers(5, 0) == 5
        assert subtract_numbers(0, 5) == -5
        assert subtract_numbers(0, 0) == 0
    
    def test_subtract_same_number(self):
        """Test subtracting a number from itself."""
        assert subtract_numbers(42, 42) == 0
    
    def test_subtract_floats(self):
        """Test subtracting floating point numbers."""
        result = subtract_numbers(5.5, 2.3)
        assert abs(result - 3.2) < 0.0001


# ============================================================================
# MULTIPLICATION TESTS
# ============================================================================

class TestMultiplyNumbers:
    """Tests for the multiply_numbers function."""
    
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        assert multiply_numbers(5, 3) == 15
    
    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        assert multiply_numbers(-5, -3) == 15
    
    def test_multiply_positive_and_negative(self):
        """Test multiplying positive and negative."""
        assert multiply_numbers(5, -3) == -15
        assert multiply_numbers(-5, 3) == -15
    
    def test_multiply_by_zero(self):
        """Test multiplication by zero."""
        assert multiply_numbers(5, 0) == 0
        assert multiply_numbers(0, 5) == 0
        assert multiply_numbers(0, 0) == 0
    
    def test_multiply_by_one(self):
        """Test multiplication by one (identity)."""
        assert multiply_numbers(42, 1) == 42
        assert multiply_numbers(1, 42) == 42
    
    def test_multiply_floats(self):
        """Test multiplying floating point numbers."""
        result = multiply_numbers(2.5, 4.0)
        assert result == 10.0
    
    def test_multiply_large_numbers(self):
        """Test multiplying large numbers."""
        assert multiply_numbers(1e6, 1e6) == 1e12


# ============================================================================
# DIVISION TESTS
# ============================================================================

class TestDivideNumbers:
    """Tests for the divide_numbers function."""
    
    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        assert divide_numbers(10, 2) == 5
    
    def test_divide_to_float(self):
        """Test division resulting in float."""
        result = divide_numbers(10, 3)
        assert abs(result - 3.333333) < 0.0001
    
    def test_divide_negative_numbers(self):
        """Test dividing negative numbers."""
        assert divide_numbers(-10, -2) == 5
    
    def test_divide_positive_by_negative(self):
        """Test dividing positive by negative."""
        assert divide_numbers(10, -2) == -5
        assert divide_numbers(-10, 2) == -5
    
    def test_divide_by_one(self):
        """Test division by one (identity)."""
        assert divide_numbers(42, 1) == 42
    
    def test_divide_by_itself(self):
        """Test dividing a number by itself."""
        assert divide_numbers(42, 42) == 1
    
    def test_divide_zero_by_number(self):
        """Test dividing zero by a number."""
        assert divide_numbers(0, 5) == 0
    
    def test_divide_by_zero(self):
        """Test division by zero raises error."""
        with pytest.raises(ValueError) as exc_info:
            divide_numbers(10, 0)
        assert "Division by zero" in str(exc_info.value)
    
    def test_divide_floats(self):
        """Test dividing floating point numbers."""
        result = divide_numbers(10.5, 2.5)
        assert abs(result - 4.2) < 0.0001
    
    def test_divide_very_small_numbers(self):
        """Test dividing very small numbers."""
        result = divide_numbers(1e-10, 1e-5)
        assert abs(result - 1e-5) < 1e-15


# ============================================================================
# PARAMETRIZED TESTS
# ============================================================================
# Pytest's parametrize feature allows testing multiple inputs efficiently

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
    (1.5, 2.5, 4.0),
])
def test_add_parametrized(a, b, expected):
    """Test addition with multiple parameter sets."""
    result = add_numbers(a, b)
    assert abs(result - expected) < 0.0001


@pytest.mark.parametrize("a,b,expected", [
    (10, 5, 2),
    (100, 10, 10),
    (1, 2, 0.5),
    (7, 2, 3.5),
])
def test_divide_parametrized(a, b, expected):
    """Test division with multiple parameter sets."""
    result = divide_numbers(a, b)
    assert abs(result - expected) < 0.0001


@pytest.mark.parametrize("invalid_input", [
    "not a number",
    "abc",
    "12.34.56",
    "",
    None,
    [],
    {},
])
def test_validate_number_invalid_inputs(invalid_input):
    """Test that validate_number rejects various invalid inputs."""
    with pytest.raises(ValueError):
        validate_number(invalid_input, "test")


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_very_large_addition(self):
        """Test addition doesn't overflow with large numbers."""
        result = add_numbers(1e308, 1e308)
        assert result > 0  # Should not raise error
    
    def test_division_precision(self):
        """Test division maintains reasonable precision."""
        # Classic floating point issue: 0.1 + 0.2 != 0.3
        result = divide_numbers(1, 3)
        # We can't expect exact equality, but should be close
        assert abs(result - 0.333333333) < 1e-6
    
    def test_negative_zero(self):
        """Test handling of negative zero."""
        result = multiply_numbers(-1, 0)
        # In Python, -0.0 == 0.0, but they're technically different
        assert result == 0
    
    def test_float_precision_limits(self):
        """Test behavior at float precision limits."""
        # Very small number
        small = 1e-100
        result = add_numbers(1.0, small)
        # Should be very close to 1
        assert result >= 1.0


# ============================================================================
# INTEGRATION-STYLE TESTS
# ============================================================================
# These test multiple operations together

class TestCalculationChains:
    """Tests for sequences of calculations."""
    
    def test_add_then_multiply(self):
        """Test chaining addition and multiplication."""
        result = add_numbers(2, 3)  # 5
        result = multiply_numbers(result, 4)  # 20
        assert result == 20
    
    def test_all_operations_chain(self):
        """Test using all operations in sequence."""
        result = add_numbers(10, 5)  # 15
        result = subtract_numbers(result, 3)  # 12
        result = multiply_numbers(result, 2)  # 24
        result = divide_numbers(result, 4)  # 6
        assert result == 6
    
    def test_order_of_operations(self):
        """Verify operations are commutative where expected."""
        # Addition is commutative
        assert add_numbers(3, 5) == add_numbers(5, 3)
        # Multiplication is commutative
        assert multiply_numbers(3, 5) == multiply_numbers(5, 3)
        # But subtraction and division are not
        assert subtract_numbers(10, 3) != subtract_numbers(3, 10)
        assert divide_numbers(10, 2) != divide_numbers(2, 10)


# ============================================================================
# TEST FIXTURES (Optional Advanced Feature)
# ============================================================================

@pytest.fixture
def sample_numbers():
    """Provide sample numbers for testing."""
    return {
        'positive': [1, 2, 5, 10, 100],
        'negative': [-1, -2, -5, -10, -100],
        'floats': [1.5, 2.7, 3.14, 0.001],
        'zero': 0
    }


def test_with_fixture(sample_numbers):
    """Example test using a fixture."""
    for num in sample_numbers['positive']:
        assert add_numbers(num, 0) == num


# ============================================================================
# RUNNING TESTS
# ============================================================================

if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])


# ============================================================================
# NOTES ON TESTING MCP SERVERS
# ============================================================================
"""
These tests focus on the business logic (calculation functions).

For testing the full MCP server (tool handlers, JSON-RPC), you would:

1. Import the server module
2. Call tool handlers directly with test arguments
3. Verify the returned TextContent objects

Example:

async def test_calculator_tool():
    from calculator_server import call_tool
    
    result = await call_tool("add", {"a": 5, "b": 3})
    
    assert len(result) == 1
    assert result[0].type == "text"
    assert "8" in result[0].text

For integration testing (testing the full server with a client):
- Use pytest-asyncio for async test support
- Mock the stdio streams
- Send JSON-RPC messages and verify responses

This is more complex and typically reserved for testing production servers.
"""

