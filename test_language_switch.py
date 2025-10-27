#!/usr/bin/env python3
"""
Test the language switching URL function
"""

def get_language_switch_url(current_path: str, current_lang: str, target_lang: str) -> str:
    """
    Generate URL for language switching.
    
    Args:
        current_path: Current URL path (e.g., '/en/talks')
        current_lang: Current language code (e.g., 'en')
        target_lang: Target language code (e.g., 'fr')
    
    Returns:
        New URL path (e.g., '/fr/talks')
    """
    # Remove the current language from the path
    if current_path.startswith(f"/{current_lang}/"):
        # Path like '/en/talks' -> '/talks'
        path_without_lang = current_path[len(f"/{current_lang}"):]
    elif current_path == f"/{current_lang}":
        # Path like '/en' -> ''
        path_without_lang = ""
    else:
        # Fallback for root or other paths
        path_without_lang = current_path
    
    # Build new URL with target language
    if path_without_lang and path_without_lang != "/":
        return f"/{target_lang}{path_without_lang}"
    else:
        return f"/{target_lang}/"

def test_language_switching():
    """Test various URL switching scenarios"""
    
    test_cases = [
        # (current_path, current_lang, target_lang, expected_result)
        ("/en/talks", "en", "fr", "/fr/talks"),
        ("/en/talks", "en", "bn", "/bn/talks"),
        ("/fr/publications", "fr", "en", "/en/publications"),
        ("/bn/blog", "bn", "fr", "/fr/blog"),
        ("/en/", "en", "fr", "/fr/"),
        ("/en", "en", "fr", "/fr/"),
        ("/fr/blog/post-1", "fr", "en", "/en/blog/post-1"),
        ("/en/notebooks/zebrafish-analysis", "en", "fr", "/fr/notebooks/zebrafish-analysis"),
    ]
    
    print("🧪 Testing Language URL Switching")
    print("=" * 50)
    
    all_passed = True
    for current_path, current_lang, target_lang, expected in test_cases:
        result = get_language_switch_url(current_path, current_lang, target_lang)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"{status} {current_path} ({current_lang} → {target_lang}) = {result}")
        if result != expected:
            print(f"     Expected: {expected}")
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All tests passed! Language switching should work correctly.")
    else:
        print("❌ Some tests failed. Check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    test_language_switching()