def get_context_functions(self, failed_func_name: str, traceback_str: str) -> Dict[str, str]:
        """Get source code for all functions in the call stack for context"""
        context_functions = {}
        tb_functions = self.extract_functions_from_traceback(traceback_str)
        current_module = sys.modules[inspect.getmodule(inspect.stack()[1][0]).__name__]
        
        for name in tb_functions:
            if hasattr(current_module, name):
                func_obj = getattr(current_module, name)
                if callable(func_obj):
                    try:
                        source = inspect.getsource(func_obj)
                        context_functions[name] = source
                    except Exception as e:
                        context_functions[name] = f"# Could not retrieve source: {e}"
        
        return context_functions#!/usr/bin/env python3
"""
Agentic Python Engineer (APE) - Function Management Decorator
A decorator that allows APE to automatically fix failing functions using AI.
"""

import os
import sys
import requests
import json
import traceback
import inspect
import ast
import re
from enum import Enum
from functools import wraps
from typing import Dict, Callable, Optional, Any


class ApeMode(Enum):
    """APE operation modes"""
    FULL_BANANAS = "full_bananas"      # Auto hot-swap and retry (default)
    APE_SUPERVISED = "ape_supervised"  # Log suggestion, manual replacement
    # Future: GOING_BANANAS = "going_bananas"  # More aggressive mode


class ApeManagerError(Exception):
    """Custom exception for APE Manager related errors"""
    pass


class ApeManager:
    """Manages APE-decorated functions and their repair process"""
    
    def __init__(self):
        self.managed_functions: Dict[str, Callable] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from environment variables"""
        self.api_url = os.getenv('LLM_API_URL')
        self.api_key = os.getenv('LLM_API_KEY')
        self.model = os.getenv('LLM_MODEL', 'claude-3-sonnet-20240229')
        
        # Load mode configuration
        mode_str = os.getenv('APE_MODE', 'FULL_BANANAS').upper()
        try:
            self.mode = ApeMode(mode_str.lower())
        except ValueError:
            print(f"⚠️ Invalid APE_MODE '{mode_str}'. Using FULL_BANANAS.")
            self.mode = ApeMode.FULL_BANANAS
        
        # Load prompt template path
        self.prompt_template_path = os.getenv('APE_PROMPT_TEMPLATE', 'ape_prompt.md')
        
        if not self.api_url:
            raise ApeManagerError(
                "LLM_API_URL environment variable is required. "
                "Please set it to your LLM service endpoint (e.g., https://api.anthropic.com/v1/messages)"
            )
        
        if not self.api_key:
            raise ApeManagerError(
                "LLM_API_KEY environment variable is required. "
                "Please set it to your LLM service API key"
            )
        
        print(f"✅ APE Manager configured with endpoint: {self.api_url}")
        print(f"🐒 APE Mode: {self.mode.value.upper()}")
        print(f"📝 Prompt template: {self.prompt_template_path}")
    
    def register_function(self, func: Callable) -> None:
        """Register a function as APE-managed"""
        self.managed_functions[func.__name__] = func
    
    def get_function_source(self, func: Callable) -> Optional[str]:
        """Extract the source code of a specific function"""
        try:
            return inspect.getsource(func)
        except Exception as e:
            print(f"🤔 Couldn't get source for {func.__name__}: {e}")
            return None
    
    def extract_functions_from_traceback(self, tb_str: str) -> list:
        """Extract all function names from a traceback string"""
        function_names = []
        lines = tb_str.split('\n')
        
        for line in lines:
            if 'in ' in line and line.strip().startswith('File'):
                continue
            elif line.strip() and not line.startswith(' ') and not line.startswith('Traceback'):
                match = re.search(r'in (\w+)', line)
                if match:
                    function_names.append(match.group(1))
        
        return list(set(function_names))
    
    def load_prompt_template(self) -> str:
        """Load the prompt template from external file"""
        try:
            with open(self.prompt_template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"⚠️ Prompt template file '{self.prompt_template_path}' not found. Using fallback.")
            return self._get_fallback_prompt_template()
        except Exception as e:
            print(f"⚠️ Error loading prompt template: {e}. Using fallback.")
            return self._get_fallback_prompt_template()
    
    def _get_fallback_prompt_template(self) -> str:
        """Fallback prompt template if external file is not available"""
        return """I have a Python function that's failing. Please rewrite ONLY the failed function to fix the error.

ERROR DETAILS:
{error_info}

FAILED FUNCTION SOURCE:
```python
{failed_function_source}
```
{context_section}

REQUIREMENTS:
- This function is decorated with @ape_managed
- Keep the same function name and general purpose  
- The API endpoint might be fake/broken - you can replace it with a real one
- Add proper error handling
- Maintain any comments if possible
- Consider the data flow and expectations from context functions
- Return ONLY the fixed function definition (including the @ape_managed decorator)

Please analyze the full call stack context to understand what this function should return and how it fits into the larger program flow."""
        """Get source code for all functions in the call stack for context"""
        context_functions = {}
        tb_functions = self.extract_functions_from_traceback(traceback_str)
        current_module = sys.modules[inspect.getmodule(inspect.stack()[1][0]).__name__]
        
        for name in tb_functions:
            if hasattr(current_module, name):
                func_obj = getattr(current_module, name)
                if callable(func_obj):
                    try:
                        source = inspect.getsource(func_obj)
                        context_functions[name] = source
                    except Exception as e:
                        context_functions[name] = f"# Could not retrieve source: {e}"
        
        return context_functions
    
    def request_function_fix(self, func: Callable, error: Exception) -> Optional[str]:
        """Request APE to fix a specific function that failed"""
        failed_function_source = self.get_function_source(func._original_function)
        if not failed_function_source:
            return None
        
        full_traceback = traceback.format_exc()
        context_functions = self.get_context_functions(func.__name__, full_traceback)
        
        # Build context section
        context_section = "\nCONTEXT FUNCTIONS (from call stack):\n"
        for name, source in context_functions.items():
            if name != func.__name__:
                context_section += f"\n--- {name}() ---\n```python\n{source}\n```\n"
        
        error_info = f"Function: {func.__name__}\nError: {str(error)}\nFull Traceback:\n{full_traceback}"
        
        # Load prompt template and format it
        prompt_template = self.load_prompt_template()
        prompt = prompt_template.format(
            error_info=error_info,
            failed_function_source=failed_function_source,
            context_section=context_section
        )

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        
        payload = {
            "model": self.model,
            "max_tokens": 1500,
            "messages": [
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            fixed_code = result['content'][0]['text']
            
            # Extract function from markdown if present
            if '```python' in fixed_code:
                start = fixed_code.find('```python') + 9
                end = fixed_code.find('```', start)
                fixed_code = fixed_code[start:end].strip()
            
            return fixed_code
            
        except Exception as e:
            print(f"😅 APE API call failed: {e}")
            return None
    
    def replace_function_in_source(self, func_name: str, new_function_code: str, source_file: str) -> bool:
        """Replace a specific function in the source file with APE's fixed version"""
        try:
            # Read current source
            with open(source_file, 'r') as f:
                source_lines = f.readlines()
            
            # Parse AST to find the function
            with open(source_file, 'r') as f:
                tree = ast.parse(f.read())
            
            # Find the target function node
            target_func = None
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == func_name:
                    target_func = node
                    break
            
            if not target_func:
                print(f"❌ Couldn't locate function '{func_name}' in source")
                return False
            
            # Calculate line numbers (AST is 1-indexed)
            start_line = target_func.lineno - 1
            end_line = target_func.end_lineno
            
            # Replace the function lines
            new_source = (
                source_lines[:start_line] + 
                [new_function_code + '\n\n'] + 
                source_lines[end_line:]
            )
            
            # Create backup
            backup_filename = f"{source_file}.backup"
            with open(backup_filename, 'w') as backup:
                backup.writelines(source_lines)
            print(f"📦 Created backup at: {backup_filename}")
            
            # Write the updated source
            with open(source_file, 'w') as f:
                f.writelines(new_source)
            
            print(f"✅ Successfully replaced function '{func_name}'!")
            return True
            
        except Exception as e:
            print(f"💀 Failed to replace function: {e}")
            return False
    
    def hot_swap_function(self, func_name: str, new_function_code: str, caller_module) -> Optional[Callable]:
        """
        Hot-swap a function in memory by executing the new code and replacing the function.
        Returns the new function if successful, None otherwise.
        """
        try:
            # Prepare execution context with the caller's globals
            exec_globals = caller_module.__dict__.copy()
            exec_locals = {}
            
            # Execute the new function code
            exec(new_function_code, exec_globals, exec_locals)
            
            # Find the newly defined function
            new_func = None
            for name, obj in exec_locals.items():
                if callable(obj) and hasattr(obj, '__name__') and obj.__name__ == func_name:
                    new_func = obj
                    break
            
            if not new_func:
                print(f"❌ Could not find function '{func_name}' in executed code")
                return None
            
            # Store original function for potential rollback
            original_func = getattr(caller_module, func_name, None)
            
            # Replace the function in the module
            setattr(caller_module, func_name, new_func)
            
            # Update our registry
            if hasattr(new_func, '_original_function'):
                self.managed_functions[func_name] = new_func._original_function
            
            print(f"🔄 Hot-swapped function '{func_name}' successfully!")
            return new_func
            
        except Exception as e:
            print(f"💀 Hot-swap failed for '{func_name}': {e}")
            return None


# Global APE manager instance
try:
    _ape_manager = ApeManager()
except ApeManagerError as e:
    print(f"❌ APE Manager initialization failed: {e}")
    sys.exit(1)


def ape_managed(func: Callable) -> Callable:
    """
    Decorator that marks a function as APE-managed.
    When this function fails, APE will attempt to rewrite just this function
    and then retry the call with the same arguments.
    
    Environment variables required:
    - LLM_API_URL: The LLM service endpoint (e.g., https://api.anthropic.com/v1/messages)
    - LLM_API_KEY: Your LLM service API key
    - LLM_MODEL: (Optional) The model to use (defaults to claude-3-sonnet-20240229)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 2  # Prevent infinite loops
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                # Get the current function to call (might be updated from previous retry)
                caller_frame = inspect.currentframe().f_back
                caller_module = inspect.getmodule(caller_frame)
                current_func = getattr(caller_module, func.__name__, func)
                
                # If this is the original function, call it directly
                if retry_count == 0:
                    return func(*args, **kwargs)
                else:
                    # For retries, call the updated function
                    if hasattr(current_func, '_original_function'):
                        return current_func._original_function(*args, **kwargs)
                    else:
                        return current_func(*args, **kwargs)
                        
            except Exception as e:
                if retry_count >= max_retries:
                    print(f"🙈 Max retries ({max_retries}) reached for '{func.__name__}'. Giving up.")
                    raise e
                
                print(f"💥 @ape_managed function '{func.__name__}' failed (attempt {retry_count + 1}): {e}")
                print("Requesting APE 🦍 assistance for function repair...")
                
                # Attempt to get APE to fix just this function
                fixed_function = _ape_manager.request_function_fix(wrapper, e)
                if fixed_function:
                    if _ape_manager.mode == ApeMode.FULL_BANANAS:
                        # Full automatic mode - hot-swap and retry
                        caller_frame = inspect.currentframe().f_back
                        caller_module = inspect.getmodule(caller_frame)
                        
                        # Try hot-swapping first
                        new_func = _ape_manager.hot_swap_function(func.__name__, fixed_function, caller_module)
                        if new_func:
                            print(f"🔧 Function '{func.__name__}' has been hot-swapped!")
                            print("🔄 Retrying with the fixed function...")
                            retry_count += 1
                            continue
                        else:
                            # Fall back to file replacement
                            source_file = inspect.getfile(caller_frame)
                            if _ape_manager.replace_function_in_source(func.__name__, fixed_function, source_file):
                                print(f"🔧 Function '{func.__name__}' has been updated in source!")
                                print("🔄 Please restart the program to use the fixed version.")
                            else:
                                print(f"🥹👉👈 Both hot-swap and file update failed for '{func.__name__}'.")
                            break
                    
                    elif _ape_manager.mode == ApeMode.APE_SUPERVISED:
                        # Supervised mode - log suggestion and stop
                        print(f"🐒 APE SUPERVISED MODE - Suggested fix for '{func.__name__}':")
                        print("=" * 60)
                        print(fixed_function)
                        print("=" * 60)
                        print("📝 To apply this fix:")
                        print(f"   1. Replace the '{func.__name__}' function with the code above")
                        print("   2. Restart your program")
                        print("   3. Test the fix")
                        break
                else:
                    print(f"🥹👉👈 APE couldn't fix '{func.__name__}'. Manual intervention required.")
                    break
        
        # If we get here, all retries failed
        raise e
    
    # Register this function as APE-managed
    _ape_manager.register_function(func)
    wrapper._is_ape_managed = True
    wrapper._original_function = func
    
    return wrapper


def get_managed_functions() -> Dict[str, Callable]:
    """Get all currently APE-managed functions"""
    return _ape_manager.managed_functions.copy()


def get_manager_status() -> Dict[str, Any]:
    """Get status information about the APE manager"""
    return {
        'api_url': _ape_manager.api_url,
        'model': _ape_manager.model,
        'mode': _ape_manager.mode.value,
        'prompt_template_path': _ape_manager.prompt_template_path,
        'managed_function_count': len(_ape_manager.managed_functions),
        'managed_functions': list(_ape_manager.managed_functions.keys())
    }