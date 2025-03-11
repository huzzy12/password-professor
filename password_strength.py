import re
import string
import random

# List of common passwords to blacklist
COMMON_PASSWORDS = [
    "password", "123456", "qwerty", "admin", "welcome", "password123", 
    "abc123", "letmein", "monkey", "1234567", "12345678", "12345", 
    "111111", "sunshine", "princess", "dragon", "trustno1", "iloveyou"
]

# List of common patterns to detect
COMMON_PATTERNS = [
    r"^\d+$",                  # All numbers
    r"^[a-zA-Z]+$",            # All letters
    r"^[a-z]+$",               # All lowercase
    r"^[A-Z]+$",               # All uppercase
    r"12345",                  # Sequential numbers
    r"qwerty",                 # Keyboard patterns
    r"abcdef",                 # Sequential letters
    r"(.)\1{2,}",              # Repeated characters (3 or more)
    r"(\w)\1(\w)\2",           # Repeated pairs (like "abab")
]

def check_password_strength(password):
    """
    Analyzes password strength based on multiple criteria and returns a score and feedback.
    
    Args:
        password (str): The password to analyze
        
    Returns:
        tuple: (score, feedback_list, strength_category)
    """
    score = 0
    feedback = []
    
    # Check if password is in common password list
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("❌ This is a commonly used password and can be easily guessed.")
        return 0, feedback, "Very Weak"
    
    # Length Check with graduated scoring
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
        feedback.append("⚠️ Consider using a longer password (12+ characters) for better security.")
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:'\",.<>/?]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Pattern detection (reduces score)
    pattern_detected = False
    for pattern in COMMON_PATTERNS:
        if re.search(pattern, password):
            pattern_detected = True
            score = max(0, score - 1)  # Reduce score but not below 0
            feedback.append("⚠️ Your password contains a predictable pattern.")
            break
    
    # Bonus points for length and complexity
    if len(password) >= 16 and not pattern_detected:
        score += 1
        
    if len(set(password)) >= 10:  # High character diversity
        score += 1
    
    # Determine strength category
    if score >= 6:
        strength = "Very Strong"
    elif score >= 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Moderate"
    elif score >= 1:
        strength = "Weak"
    else:
        strength = "Very Weak"
    
    # Add positive feedback for strong passwords
    if score >= 5 and not feedback:
        feedback.append("✅ Excellent password! Your password meets all security criteria.")
    elif score >= 3 and not feedback:
        feedback.append("✅ Good password, but could be improved further.")
    
    return score, feedback, strength

def generate_password(length=16, include_uppercase=True, include_digits=True, include_special=True):
    """
    Generates a strong random password based on specified criteria.
    
    Args:
        length (int): Length of the password
        include_uppercase (bool): Include uppercase letters
        include_digits (bool): Include digits
        include_special (bool): Include special characters
        
    Returns:
        str: A randomly generated password
    """
    # Ensure minimum length
    length = max(length, 8)
    
    # Define character sets
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase if include_uppercase else ""
    digit_chars = string.digits if include_digits else ""
    special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>/?" if include_special else ""
    
    # Combine all character sets
    all_chars = lowercase_chars + uppercase_chars + digit_chars + special_chars
    
    # Ensure we have at least one character from each included set
    password = []
    if lowercase_chars:
        password.append(random.choice(lowercase_chars))
    if uppercase_chars:
        password.append(random.choice(uppercase_chars))
    if digit_chars:
        password.append(random.choice(digit_chars))
    if special_chars:
        password.append(random.choice(special_chars))
    
    # Fill the rest with random characters
    remaining_length = length - len(password)
    password.extend(random.choice(all_chars) for _ in range(remaining_length))
    
    # Shuffle the password characters
    random.shuffle(password)
    
    return ''.join(password)

# Simple command-line interface for testing
if __name__ == "__main__":
    print("===== Password Professor: Password Strength Meter =====\n")
    while True:
        password = input("Enter your password (or type 'generate' for a suggestion, 'q' to quit): ")
        
        if password.lower() == 'q':
            break
        elif password.lower() == 'generate':
            generated = generate_password()
            print(f"\nGenerated password: {generated}")
            score, feedback, strength = check_password_strength(generated)
            print(f"Strength: {strength} (Score: {score}/7)\n")
            continue
        
        score, feedback, strength = check_password_strength(password)
        
        print(f"\nPassword Strength: {strength} (Score: {score}/7)")
        if feedback:
            print("Feedback:")
            for item in feedback:
                print(f"  {item}")
        print("\n" + "-"*50 + "\n")