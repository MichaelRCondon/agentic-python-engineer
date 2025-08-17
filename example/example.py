#!/usr/bin/env python3
"""
Self-Healing Python Program Example
Demonstrates usage of the @ape_managed decorator.
"""

import requests
from agentic_python_engineer import ape_managed, get_managed_functions, get_manager_status

# Example configuration for demonstration
PLACEHOLDER_API_URL = "https://api.placeholder-service.com/data"

# ============================================================================
# APE-Managed Functions (These can be auto-fixed!)
# ============================================================================

@ape_managed
def fetch_important_data():
    """
    This function is marked as @ape_managed, so APE will try to fix it if it breaks.
    Currently does something that will definitely fail.
    """
    print("📡 Fetching super important data from the placeholder API...")
    
    response = requests.get(PLACEHOLDER_API_URL, timeout=5)
    response.raise_for_status()
    
    data = response.json()
    print(f"📊 Got data: {data}")
    return data


@ape_managed  
def process_data(data):
    """
    Another APE-managed function that processes the fetched data.
    Also likely to fail in creative ways.
    """
    print("⚙️ Processing the super important data...")
    
    # This will fail if data is None or doesn't have expected structure
    important_value = data['nonexistent_key']['deeply_nested_value']
    
    result = important_value * 42  # The answer to everything
    print(f"🎯 Processed result: {result}")
    return result


# ============================================================================
# Safe Functions (These won't be auto-modified)
# ============================================================================

def check_ape_managed_status():
    """
    Shows which functions are under APE management.
    This function is NOT @ape_managed, so it's safe from modification.
    """
    print("\n🛡️ APE-Managed Function Status:")
    
    managed_funcs = get_managed_functions()
    for name in managed_funcs:
        print(f"   🤖 {name}() - Under APE's protective care")
    
    print(f"\n📊 Total functions managed by APE: {len(managed_funcs)}")


def show_manager_info():
    """Display APE manager configuration and status"""
    print("\n🔧 APE Manager Configuration:")
    status = get_manager_status()
    
    print(f"   🌐 API URL: {status['api_url']}")
    print(f"   🧠 Model: {status['model']}")
    print(f"   📈 Managed Functions: {status['managed_function_count']}")


def main():
    """
    Main orchestrator function. 
    NOT @ape_managed because we don't want APE messing with our control flow!
    """
    print("\n🎪 Welcome to the Self-Healing Python Program!")
    print("🔥 Now with HOT-SWAPPING - functions are fixed and retried automatically!")
    print("🧠 APE gets full call stack context for smarter fixes!")
    
    show_manager_info()
    check_ape_managed_status()
    
    print("\n🚀 Starting the probably-doomed API adventure...")
    
    try:
        # This should fail, get fixed, and then succeed automatically
        data = fetch_important_data()
        
        # This might also fail, but APE will have context about what data should look like
        result = process_data(data)
        
        print(f"🎉 Amazing! Everything worked: {result}")
        
    except Exception as e:
        print(f"\n💔 Final failure after all retry attempts!")
        print("🔧 Check the function fixes or restart if file-based updates were made.")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()