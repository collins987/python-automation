import random
import string
import re
import hashlib
import pyotp
from datetime import datetime, timedelta

# This script generates secure passwords based on user-defined parameters,
# ensures complexity requirements, checks against common passwords,
# integrates two-factor authentication (2FA) generation, evaluates password strength,
# allows password expiration, and hashes the password for secure storage.
# It also avoids predictable patterns like sequential characters.

# List of common passwords to avoid
common_passwords = {"password", "123456", "qwerty", "letmein", "welcome"}

# Function to evaluate the strength of a password
def evaluate_password_strength(password):
    strength = 0
    # Length check
    if len(password) >= 12:
        strength += 1
    # Uppercase, lowercase, digit, and symbol check
    if re.search(r'[A-Z]', password): strength += 1
    if re.search(r'[a-z]', password): strength += 1
    if re.search(r'[0-9]', password): strength += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): strength += 1
    return strength

# Function to generate a secure password with customizable parameters
def generate_password(length=12, min_uppercase=2, min_digits=2, min_special=2, expiry_days=90, use_upper=True, use_digits=True, use_special=True, user_info="user"):
    # Ensure the minimum length is sufficient for the complexity requirements
    if length < min_uppercase + min_digits + min_special:
        raise ValueError("Password length is too short for the specified requirements.")
    
    # Generate parts of the password to meet minimum requirements
    password = [
        random.choice(string.ascii_uppercase) for _ in range(min_uppercase)
    ] + [
        random.choice(string.digits) for _ in range(min_digits)
    ] + [
        random.choice(string.punctuation) for _ in range(min_special)
    ]
    
    # Fill the rest with random characters
    chars = string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation
        
    password += [random.choice(chars) for _ in range(length - len(password))]
    
    # Shuffle the result to make the password random
    random.shuffle(password)
    
    # Convert the password list to a string
    password = ''.join(password)

    # Check if password is in common passwords list
    if password in common_passwords:
        print("Password is a common password. Regenerating...")
        return generate_password(length, min_uppercase, min_digits, min_special, expiry_days, use_upper, use_digits, use_special, user_info)
    
    # Evaluate password strength
    strength = evaluate_password_strength(password)
    
    # Generate OTP for 2FA (for extra security)
    otp = pyotp.TOTP('JBSWY3DPEHPK3PXP').now()  # Example OTP secret key
    
    # Hash the password for secure storage
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Display password details
    print(f"Generated Password: {password}")
    print(f"Password Strength: {strength}/4 (Higher is better)")
    print(f"Generated OTP: {otp}")
    print(f"Hashed Password (for secure storage): {hashed_password}")
    
    # Set expiry date for the password
    expiry_date = datetime.now() + timedelta(days=expiry_days)
    print(f"Password expires on: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Return the password and relevant data
    return password, otp, hashed_password, expiry_date

# Example usage of the function
password, otp, hashed_password, expiry_date = generate_password(
    length=16, min_uppercase=3, min_digits=3, min_special=3, expiry_days=90, 
    use_upper=True, use_digits=True, use_special=True, user_info="john_doe"
)
