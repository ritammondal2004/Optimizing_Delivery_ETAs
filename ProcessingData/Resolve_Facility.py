# ── Helper to find best match ───────────────────────────────
from difflib import get_close_matches
from ProcessingData.load_models import load_all

models = load_all()
name_to_code = models['name_to_code']
def resolve_facility(user_input):
    cleaned = str(user_input).lower().strip()
    
    # Exact match
    if cleaned in name_to_code:
        return name_to_code[cleaned], user_input
    
    # Check if user input is contained in any key
    # e.g. 'mumbai' found in 'mumbai hub - andheri'
    contains_matches = [
        k for k in name_to_code.keys() 
        if isinstance(k, str) and cleaned in k
    ]
    
    if contains_matches:
        print(f"\n  '{user_input}' matched these facilities:")
        for i, match in enumerate(contains_matches[:5]):
            print(f"    [{i+1}] {match.title()}")
        
        choice = input("  Enter number (or 0 to cancel): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(contains_matches[:5]):
            chosen = contains_matches[int(choice)-1]
            return name_to_code[chosen], chosen.title()
        else:
            return None, None 

    # Fuzzy match as fallback (lowered cutoff)
    valid_keys = [k for k in name_to_code.keys() if isinstance(k, str)]
    close = get_close_matches(
        cleaned, 
        valid_keys, 
        n        = 5,      # show more options
        cutoff   = 0.25    # very relaxed ← 25% matches required
    )
    
    if close:
        print(f"\n  '{user_input}' not found exactly.")
        print(f"  Did you mean one of these?")
        for i, match in enumerate(close):
            print(f"    [{i+1}] {match.title()}")
        
        choice = input("  Enter number (or 0 to cancel): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(close):
            chosen = close[int(choice)-1]
            return name_to_code[chosen], chosen.title()
        else:
            return None, None
    
    print(f"  ❌ '{user_input}' not recognized in the network.")
    print(f"  Try checking available cities with: show_available_cities('{user_input}')") 
    return None, None