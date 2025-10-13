#!/usr/bin/env python3
"""
Test script to verify the decorator fix works.
"""

import sys
import os
import asyncio

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

async def test_decorator():
    """Test that the decorator works correctly."""
    try:
        from observability import log_command_usage
        
        # Mock context object
        class MockContext:
            def __init__(self):
                self.author = MockAuthor()
                self.guild = MockGuild()
        
        class MockAuthor:
            def __init__(self):
                self.id = "123456789"
        
        class MockGuild:
            def __init__(self):
                self.id = "987654321"
        
        # Test decorator on instance method
        class TestClass:
            @log_command_usage("test_command")
            async def test_method(self, ctx):
                return "success"
        
        # Test decorator on standalone function
        @log_command_usage("standalone_command")
        async def standalone_function(ctx):
            return "success"
        
        # Test instance method
        test_obj = TestClass()
        mock_ctx = MockContext()
        
        result1 = await test_obj.test_method(mock_ctx)
        print(f"✅ Instance method decorator works: {result1}")
        
        # Test standalone function
        result2 = await standalone_function(mock_ctx)
        print(f"✅ Standalone function decorator works: {result2}")
        
        print("🎉 All decorator tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Decorator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    print("🔧 Testing Decorator Fix")
    print("=" * 40)
    
    success = await test_decorator()
    
    if success:
        print("\n✅ Decorator fix is working correctly!")
        print("The bot should now run without the AttributeError.")
    else:
        print("\n❌ Decorator fix failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
