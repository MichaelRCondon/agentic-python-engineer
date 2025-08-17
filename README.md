# 🐒 Agentic Python Engineer (APE)

**APE strong together** 🦍
---

## What is APE?

APE uses state-of-the-art artificial intelligence to make sure your Python code runs whether your functions like it or not. Through a process known as **B.A.N.A.N.A.S** (Break-Analyze-Natural language processing-Auto-fix-Never give up-And-Succeed), APE repeatedly detects failing functions, sends them to an LLM for emergency surgery, and hot-swaps the fixed code back into your running program.

To survive such an intelligent process, APE reloads individual functions in memory after each fix, allowing your program to continue executing without missing a beat.

## Installation

1. Install the package (coming soon™)
   ```bash
   pip install agentic-python-engineer
   ```
2. Set your environment variables:
   ```bash
   export LLM_API_URL="https://api.anthropic.com/v1/messages"
   export LLM_API_KEY="your-api-key-here"
   ```
3. Import and decorate your doomed functions
4. Watch the magic happen 🪄

## Usage

```python
from agentic_python_engineer import ape_managed

@ape_managed
def your_terrible_function():
    # This will probably break
    return definitely_undefined_variable * impossible_math()

# APE will automatically fix it when it fails!
result = your_terrible_function()  # Somehow this works now
```

Our tireless APE engineers will take your old and moldy bananas (broken functions) and lovingly transform them into delicious, functional banana bread 🍞. The end result might not look like your original recipe, but it'll be infinitely more edible and significantly less likely to poison your users.

## The B.A.N.A.N.A.S Process

- **B**reak - Your function crashes spectacularly
- **A**nalyze - APE examines the carnage and gathers context
- **N**atural language processing - LLM reads the error like a bedtime story
- **A**uto-fix - AI generates a working replacement
- **N**ever give up - Hot-swaps the function in memory
- **A**nd retry - Attempts the call again with same arguments
- **S**ucceed - Celebrates with digital banana dance 🍌💃

## Advanced Usage

### Status Checking
```python
from agentic_python_engineer import get_managed_functions, get_manager_status

# See which functions are under APE protection
protected_functions = get_managed_functions()

# Get APE's vital signs
status = get_manager_status()
print(f"APE is watching over {status['managed_function_count']} functions")
```

### Multiple LLM Services
APE works with any LLM service that can read Python and write jokes:

```bash
# For Claude (recommended by 9 out of 10 digital primates)
export LLM_API_URL="https://api.anthropic.com/v1/messages"
export LLM_MODEL="claude-3-sonnet-20240229"

# For OpenAI (if you must)
export LLM_API_URL="https://api.openai.com/v1/chat/completions"
export LLM_MODEL="gpt-4"
```

## Safety Features

- **Retry Limits**: APE won't get stuck in an infinite fixing loop (max 2 attempts)
- **Hot-Swapping**: Functions are fixed in memory - no restart required
- **Backup Creation**: Original source files are backed up (just in case)
- **Surgical Precision**: Only `@ape_managed` functions get the treatment

## Frequently Asked Questions

### 1) Is this a good idea?
Of course not. This is quite possibly the most reckless Python decorator ever written. But it's also kind of amazing when it works.

### 2) What happens if the LLM makes my code worse?
That's what the retry limit is for! After 2 failed attempts, APE gives up and lets you deal with your own mess.

### 3) Why "APE"?
Because monkeys, especially seated at keyboards, are known for their problem-solving abilities, and this project requires about the same level of intellectual rigor as teaching a chimp to code.

### 4) Help! I have way too much money and desperately need to give it to AI companies!
Have no fear: just keep using LLM APIs! Your wallet will be lighter in no time.

## Technical Support

- For technical issues: Submit a GitHub issue (and pray to the algorithm gods)
- For existential questions about AI fixing your code: Take a deep breath, the singularity is probably fine
- For complaints about your code becoming sentient: That's a feature, not a bug

## Contributing

1. Fork the repo
2. Write some intentionally broken code
3. Watch APE fix it
4. Submit a PR with your amazement documented

## License

MIT License with the following additional terms:

- If APE achieves sentience and starts writing better code than you, you must acknowledge its superiority
- If you use APE to fix production code, you must be prepared to explain to your team why an AI is a better programmer than they are
- The Author is not responsible for any existential crises resulting from watching AI fix your bugs faster than you can create them

## Warning

⚠️ **DANGER**: This software may cause:
- Sudden realization that AI is smarter than you
- Compulsive decoration of all functions with `@ape_managed`
- Uncontrollable urge to replace your entire dev team with monkeys
- Banana addiction

---

*Remember: APE strong together! 🐒🤝🐒*

## Fun Fact

This README was written by a human, but if it had any bugs, APE could probably fix those too.