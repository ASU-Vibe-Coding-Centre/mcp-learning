# Challenge 1 Solutions: Custom Tool Design

This document provides complete solutions for each option in Challenge 1. Each solution demonstrates professional implementation with validation, error handling, and documentation.

## Table of Contents

1. [Option A: URL Information Tool](#option-a-url-information-tool)
2. [Option B: Password Strength Checker](#option-b-password-strength-checker)
3. [Option C: Temperature Converter](#option-c-temperature-converter)
4. [Option D: Text Statistics Tool](#option-d-text-statistics-tool)

---

## Option A: URL Information Tool

### Complete Implementation

```python
#!/usr/bin/env python3
"""URL Analysis MCP Server"""

import asyncio
from urllib.parse import urlparse, parse_qs
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("url-analyzer")


def analyze_url_string(url: str) -> dict:
    """
    Parse a URL and extract components.
    
    Args:
        url: URL string to analyze
        
    Returns:
        Dictionary with URL components
        
    Raises:
        ValueError: If URL is invalid
    """
    # Validate input
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    url = url.strip()
    if not url:
        raise ValueError("URL cannot be empty or whitespace only")
    
    # Parse the URL
    try:
        parsed = urlparse(url)
    except Exception as e:
        raise ValueError(f"Invalid URL format: {str(e)}")
    
    # Ensure we have at least a scheme and netloc
    if not parsed.scheme:
        raise ValueError("URL must include a protocol (e.g., https://)")
    
    if not parsed.netloc:
        raise ValueError("URL must include a domain")
    
    # Extract query parameters
    query_params = {}
    if parsed.query:
        query_params = {
            k: v[0] if len(v) == 1 else v 
            for k, v in parse_qs(parsed.query).items()
        }
    
    # Build result
    result = {
        "protocol": parsed.scheme,
        "domain": parsed.netloc,
        "path": parsed.path or "/",
        "query_parameters": query_params,
        "fragment": parsed.fragment or None,
        "port": parsed.port
    }
    
    return result


def format_url_analysis(analysis: dict) -> str:
    """Format URL analysis as readable text."""
    lines = ["URL Analysis:"]
    lines.append(f"  Protocol: {analysis['protocol']}")
    lines.append(f"  Domain: {analysis['domain']}")
    
    if analysis['port']:
        lines.append(f"  Port: {analysis['port']}")
    
    lines.append(f"  Path: {analysis['path']}")
    
    if analysis['query_parameters']:
        lines.append("  Query Parameters:")
        for key, value in analysis['query_parameters'].items():
            lines.append(f"    - {key}: {value}")
    else:
        lines.append("  Query Parameters: None")
    
    if analysis['fragment']:
        lines.append(f"  Fragment: #{analysis['fragment']}")
    
    return "\n".join(lines)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return available tools."""
    return [
        Tool(
            name="analyze_url",
            description="Extract and analyze components from a URL including protocol, domain, path, query parameters, and fragment",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to analyze (must include protocol)"
                    }
                },
                "required": ["url"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool invocations."""
    if name == "analyze_url":
        url = arguments.get("url")
        
        if not url:
            return [TextContent(
                type="text",
                text="Error: 'url' parameter is required"
            )]
        
        try:
            analysis = analyze_url_string(url)
            formatted = format_url_analysis(analysis)
            return [TextContent(type="text", text=formatted)]
        except ValueError as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error analyzing URL: {str(e)}"
            )]
    
    return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]


async def main():
    """Run the URL analyzer server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

### Test Cases

```python
# Valid URLs
"https://example.com/path?id=123" 
"http://example.com:8080/page"
"https://example.com/path#section"

# Invalid URLs
""  # Empty
"example.com"  # No protocol
"https://"  # No domain
```

---

## Option B: Password Strength Checker

### Complete Implementation

```python
#!/usr/bin/env python3
"""Password Strength Checker MCP Server"""

import asyncio
import re
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("password-checker")

# Common passwords list (small sample for demonstration)
COMMON_PASSWORDS = {
    "password", "123456", "password123", "qwerty", "abc123",
    "letmein", "welcome", "monkey", "dragon", "master",
    "admin", "login", "passw0rd", "Password1"
}


def check_password_strength(password: str) -> dict:
    """
    Analyze password strength.
    
    Args:
        password: Password string to check
        
    Returns:
        Dictionary with strength rating and recommendations
    """
    checks = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "numbers": bool(re.search(r'\d', password)),
        "special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        "not_common": password.lower() not in COMMON_PASSWORDS
    }
    
    # Calculate strength score
    score = sum(checks.values())
    
    # Determine strength rating
    if score <= 2:
        rating = "Weak"
    elif score <= 4:
        rating = "Moderate"
    elif score == 5:
        rating = "Strong"
    else:
        rating = "Very Strong"
    
    # Generate recommendations
    recommendations = []
    if not checks["length"]:
        recommendations.append("Use at least 8 characters")
    if not checks["uppercase"]:
        recommendations.append("Add uppercase letters")
    if not checks["lowercase"]:
        recommendations.append("Add lowercase letters")
    if not checks["numbers"]:
        recommendations.append("Add numbers")
    if not checks["special"]:
        recommendations.append("Add special characters (!@#$%^&*, etc.)")
    if not checks["not_common"]:
        recommendations.append("Avoid common passwords")
    
    return {
        "rating": rating,
        "score": score,
        "max_score": 6,
        "checks": checks,
        "recommendations": recommendations
    }


def format_strength_report(analysis: dict) -> str:
    """Format password strength analysis as readable text."""
    lines = ["Password Strength Analysis:"]
    lines.append(f"  Rating: {analysis['rating']} ({analysis['score']}/{analysis['max_score']})")
    lines.append("")
    lines.append("  Criteria:")
    
    checks = analysis['checks']
    lines.append(f"    {'✓' if checks['length'] else '✗'} Length (8+ characters)")
    lines.append(f"    {'✓' if checks['uppercase'] else '✗'} Uppercase letters")
    lines.append(f"    {'✓' if checks['lowercase'] else '✗'} Lowercase letters")
    lines.append(f"    {'✓' if checks['numbers'] else '✗'} Numbers")
    lines.append(f"    {'✓' if checks['special'] else '✗'} Special characters")
    lines.append(f"    {'✓' if checks['not_common'] else '✗'} Not a common password")
    
    if analysis['recommendations']:
        lines.append("")
        lines.append("  Recommendations:")
        for rec in analysis['recommendations']:
            lines.append(f"    - {rec}")
    else:
        lines.append("")
        lines.append("  Excellent! This password meets all criteria.")
    
    return "\n".join(lines)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return available tools."""
    return [
        Tool(
            name="check_password_strength",
            description="Evaluate password security and provide recommendations for improvement. Returns strength rating and specific feedback.",
            inputSchema={
                "type": "object",
                "properties": {
                    "password": {
                        "type": "string",
                        "description": "The password to evaluate (will not be stored or logged)"
                    }
                },
                "required": ["password"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool invocations."""
    if name == "check_password_strength":
        password = arguments.get("password")
        
        if password is None:
            return [TextContent(
                type="text",
                text="Error: 'password' parameter is required"
            )]
        
        # Handle empty password
        if not password:
            return [TextContent(
                type="text",
                text="Error: Password cannot be empty"
            )]
        
        try:
            analysis = check_password_strength(password)
            formatted = format_strength_report(analysis)
            return [TextContent(type="text", text=formatted)]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error analyzing password: {str(e)}"
            )]
    
    return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]


async def main():
    """Run the password checker server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

### Test Cases

```python
# Weak passwords
"pass"  # Too short
"password"  # Common
"abc123"  # Common

# Moderate passwords
"Password1"  # Missing special chars
"mypassword123"  # Missing uppercase

# Strong passwords
"MyP@ssw0rd!"  # Meets all criteria
"Tr0ub4dor&3"  # XKCD-style
```

---

## Option C: Temperature Converter

### Complete Implementation

```python
#!/usr/bin/env python3
"""Temperature Converter MCP Server"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("temperature-converter")

# Absolute zero in different scales
ABSOLUTE_ZERO = {
    "C": -273.15,
    "F": -459.67,
    "K": 0
}


def convert_temperature(value: float, from_scale: str, to_scale: str) -> float:
    """
    Convert temperature between scales.
    
    Args:
        value: Temperature value
        from_scale: Source scale (C, F, K)
        to_scale: Target scale (C, F, K)
        
    Returns:
        Converted temperature value
        
    Raises:
        ValueError: If scales are invalid or temperature is below absolute zero
    """
    # Normalize scale names
    from_scale = from_scale.upper()
    to_scale = to_scale.upper()
    
    # Validate scales
    valid_scales = ["C", "F", "K"]
    if from_scale not in valid_scales:
        raise ValueError(f"Invalid source scale '{from_scale}'. Must be C, F, or K")
    if to_scale not in valid_scales:
        raise ValueError(f"Invalid target scale '{to_scale}'. Must be C, F, or K")
    
    # Check for absolute zero violation
    if value < ABSOLUTE_ZERO[from_scale]:
        raise ValueError(
            f"Temperature {value}°{from_scale} is below absolute zero "
            f"({ABSOLUTE_ZERO[from_scale]}°{from_scale})"
        )
    
    # If same scale, return as-is
    if from_scale == to_scale:
        return value
    
    # Convert to Celsius first (common intermediate)
    if from_scale == "C":
        celsius = value
    elif from_scale == "F":
        celsius = (value - 32) * 5/9
    else:  # K
        celsius = value - 273.15
    
    # Convert from Celsius to target scale
    if to_scale == "C":
        result = celsius
    elif to_scale == "F":
        result = celsius * 9/5 + 32
    else:  # K
        result = celsius + 273.15
    
    return round(result, 2)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return available tools."""
    return [
        Tool(
            name="convert_temperature",
            description="Convert temperature between Celsius (C), Fahrenheit (F), and Kelvin (K) scales",
            inputSchema={
                "type": "object",
                "properties": {
                    "value": {
                        "type": "number",
                        "description": "Temperature value to convert"
                    },
                    "from_scale": {
                        "type": "string",
                        "description": "Source scale: C (Celsius), F (Fahrenheit), or K (Kelvin)"
                    },
                    "to_scale": {
                        "type": "string",
                        "description": "Target scale: C (Celsius), F (Fahrenheit), or K (Kelvin)"
                    }
                },
                "required": ["value", "from_scale", "to_scale"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool invocations."""
    if name == "convert_temperature":
        value = arguments.get("value")
        from_scale = arguments.get("from_scale")
        to_scale = arguments.get("to_scale")
        
        # Validate required parameters
        if value is None:
            return [TextContent(type="text", text="Error: 'value' parameter is required")]
        if not from_scale:
            return [TextContent(type="text", text="Error: 'from_scale' parameter is required")]
        if not to_scale:
            return [TextContent(type="text", text="Error: 'to_scale' parameter is required")]
        
        # Validate value type
        if not isinstance(value, (int, float)):
            return [TextContent(type="text", text="Error: 'value' must be a number")]
        
        try:
            result = convert_temperature(value, from_scale, to_scale)
            
            # Format scale names for display
            scale_names = {"C": "Celsius", "F": "Fahrenheit", "K": "Kelvin"}
            from_name = scale_names.get(from_scale.upper(), from_scale)
            to_name = scale_names.get(to_scale.upper(), to_scale)
            
            message = f"{value}° {from_name} = {result}° {to_name}"
            
            return [TextContent(type="text", text=message)]
        
        except ValueError as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error converting temperature: {str(e)}")]
    
    return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]


async def main():
    """Run the temperature converter server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

### Test Cases

```python
# Standard conversions
convert_temperature(0, "C", "F")  # 32
convert_temperature(32, "F", "C")  # 0
convert_temperature(273.15, "K", "C")  # 0

# Edge cases
convert_temperature(0, "C", "C")  # 0 (same scale)
convert_temperature(-273.15, "C", "K")  # 0 (absolute zero)
convert_temperature(-300, "C", "K")  # Error (below absolute zero)
```

---

## Option D: Text Statistics Tool

### Complete Implementation

See the comprehensive implementation in `challenge-2-solution.md` as this overlaps with the text tools challenge. The `text_summary` tool there provides all required statistics.

---

## Key Patterns Demonstrated

### 1. Input Validation

All solutions demonstrate thorough validation:

```python
# Check for required parameters
if not url:
    return error_response("Parameter required")

# Validate types
if not isinstance(value, (int, float)):
    return error_response("Must be a number")

# Validate values
if value < minimum:
    return error_response("Value out of range")
```

### 2. Error Handling

Specific, helpful error messages:

```python
try:
    result = process(input)
except ValueError as e:
    return error_response(str(e))
except Exception as e:
    return error_response(f"Unexpected error: {str(e)}")
```

### 3. Helper Functions

Separate concerns:

```python
def validate_input(value):
    """Validation logic"""

def process_data(value):
    """Core logic"""

def format_output(result):
    """Formatting logic"""
```

### 4. User-Friendly Output

Clear, formatted responses:

```python
def format_analysis(analysis: dict) -> str:
    """Format analysis as readable text."""
    lines = ["Analysis:"]
    for key, value in analysis.items():
        lines.append(f"  {key}: {value}")
    return "\n".join(lines)
```

## Common Improvements

All solutions can be enhanced with:

1. **Logging**: Add logging for debugging
2. **Caching**: Cache expensive operations
3. **Configuration**: Make limits/thresholds configurable
4. **Testing**: Add unit tests for helper functions
5. **Documentation**: Add more examples in docstrings

## Next Steps

After reviewing these solutions:

1. Compare to your implementation
2. Identify patterns you can apply to other tools
3. Think about how to extend each solution
4. Move on to Challenge 2 or Challenge 3

Great work completing Challenge 1!

