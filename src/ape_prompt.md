# APE Function Repair Prompt

I have a Python function that's failing and needs to be fixed. Please analyze the error and rewrite ONLY the failed function to fix the issue.

## Error Details
{error_info}

## Failed Function Source
```python
{failed_function_source}
```

{context_section}

## Requirements

- This function is decorated with `@ape_managed`
- Keep the same function name and general purpose  
- Add proper error handling and validation
- Maintain any existing comments if possible
- Consider the data flow and expectations from context functions
- Return ONLY the fixed function definition (including the `@ape_managed` decorator)
- Comment your code fully, and use the phrase "🦍 FIXED" in your comment describing the function.
- If you cannot fix the function - because there is a bad setting, a missing value, or the error is not actually occurring in the function - return "🥹👉👈 I can't fix this one: ", followed by an explanation of the needed fix. This needs to to be in exactly this format.

## Important Notes

- Analyze the full call stack context to understand what this function should return
- Consider how this function fits into the larger program flow
- If the error is due to a missing dependency, suggest a working alternative
- If the error is due to invalid data, add appropriate validation
- Maintain backward compatibility with the function's expected interface

## Output Format

Please provide ONLY the corrected function code without any additional explanation. The function should be ready to replace the broken one directly.