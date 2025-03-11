import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import re
from password_strength import check_password_strength, generate_password

# Set page configuration
st.set_page_config(
    page_title="Password Professor",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with theme compatibility
st.markdown("""
<style>
    /* Theme-aware colors */
    :root {
        --text-color: #424242;
        --header-color: #1E88E5;
        --tip-color: #616161;
    }
    
    /* Dark theme overrides */
    [data-theme="dark"] {
        --text-color: #E0E0E0;
        --header-color: #64B5F6;
        --tip-color: #B0BEC5;
    }
    
    .main-header {
        font-size: 2.5rem;
        color: var(--header-color);
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: var(--text-color);
        margin-bottom: 1rem;
    }
    .password-meter {
        margin: 2rem 0;
    }
    .feedback-box {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    .feedback-box h3 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    /* Light mode feedback boxes */
    [data-theme="light"] .feedback-box {
        color: #212121;
    }
    [data-theme="light"] .very-weak {
        background-color: rgba(255, 87, 87, 0.15);
        border: 1px solid rgba(255, 87, 87, 0.3);
    }
    [data-theme="light"] .weak {
        background-color: rgba(255, 160, 0, 0.15);
        border: 1px solid rgba(255, 160, 0, 0.3);
    }
    [data-theme="light"] .moderate {
        background-color: rgba(255, 235, 59, 0.15);
        border: 1px solid rgba(255, 235, 59, 0.3);
    }
    [data-theme="light"] .strong {
        background-color: rgba(76, 175, 80, 0.15);
        border: 1px solid rgba(76, 175, 80, 0.3);
    }
    [data-theme="light"] .very-strong {
        background-color: rgba(33, 150, 243, 0.15);
        border: 1px solid rgba(33, 150, 243, 0.3);
    }
    /* Dark mode feedback boxes */
    [data-theme="dark"] .feedback-box {
        color: #E0E0E0;
    }
    [data-theme="dark"] .very-weak {
        background-color: rgba(255, 87, 87, 0.1);
        border: 1px solid rgba(255, 87, 87, 0.5);
    }
    [data-theme="dark"] .weak {
        background-color: rgba(255, 160, 0, 0.1);
        border: 1px solid rgba(255, 160, 0, 0.5);
    }
    [data-theme="dark"] .moderate {
        background-color: rgba(255, 235, 59, 0.1);
        border: 1px solid rgba(255, 235, 59, 0.5);
    }
    [data-theme="dark"] .strong {
        background-color: rgba(76, 175, 80, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.5);
    }
    [data-theme="dark"] .very-strong {
        background-color: rgba(33, 150, 243, 0.1);
        border: 1px solid rgba(33, 150, 243, 0.5);
    }
    .password-tip {
        font-size: 0.9rem;
        color: var(--tip-color);
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔒 Password Professor</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-header">Advanced Password Strength Analyzer</h2>', unsafe_allow_html=True)

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Password Analyzer", "Password Generator"])

# Password Analyzer Tab
with tab1:
    # Password input with toggle for visibility
    col1, col2 = st.columns([4, 1])
    with col1:
        password_visible = col2.checkbox("Show password", value=False)
        if password_visible:
            password = st.text_input("Enter your password", "", key="visible_password")
        else:
            password = st.text_input("Enter your password", "", type="password", key="hidden_password")
    
    # Analyze button
    if st.button("Analyze Password", key="analyze_btn"):
        if password:
            with st.spinner("Analyzing password strength..."):
                # Add a small delay for effect
                time.sleep(0.5)
                
                # Get password analysis
                score, feedback, strength = check_password_strength(password)
                
                # Display strength meter
                st.markdown('<div class="password-meter">', unsafe_allow_html=True)
                
                # Create a progress bar for visual representation
                if strength == "Very Weak":
                    st.progress(max(0.05, score/7))  # Minimum visibility
                    st.markdown(f'<div class="feedback-box very-weak"><h3>Password Strength: {strength} (Score: {score}/7)</h3></div>', unsafe_allow_html=True)
                elif strength == "Weak":
                    st.progress(score/7)
                    st.markdown(f'<div class="feedback-box weak"><h3>Password Strength: {strength} (Score: {score}/7)</h3></div>', unsafe_allow_html=True)
                elif strength == "Moderate":
                    st.progress(score/7)
                    st.markdown(f'<div class="feedback-box moderate"><h3>Password Strength: {strength} (Score: {score}/7)</h3></div>', unsafe_allow_html=True)
                elif strength == "Strong":
                    st.progress(score/7)
                    st.markdown(f'<div class="feedback-box strong"><h3>Password Strength: {strength} (Score: {score}/7)</h3></div>', unsafe_allow_html=True)
                else:  # Very Strong
                    st.progress(score/7)
                    st.markdown(f'<div class="feedback-box very-strong"><h3>Password Strength: {strength} (Score: {score}/7)</h3></div>', unsafe_allow_html=True)
                
                # Display feedback
                if feedback:
                    st.subheader("Feedback & Suggestions")
                    for item in feedback:
                        st.markdown(f"- {item}")
                
                # Create a radar chart for password characteristics
                st.subheader("Password Characteristics")
                
                # Define metrics for the radar chart
                categories = ['Length', 'Uppercase', 'Lowercase', 'Digits', 'Special Chars', 'Uniqueness']
                
                # Calculate values for each category
                length_score = min(1.0, len(password) / 16)  # Normalize to 0-1
                uppercase_score = 1.0 if re.search(r"[A-Z]", password) else 0.0
                lowercase_score = 1.0 if re.search(r"[a-z]", password) else 0.0
                digits_score = 1.0 if re.search(r"\d", password) else 0.0
                special_score = 1.0 if re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:'\",.<>/?]", password) else 0.0
                uniqueness_score = min(1.0, len(set(password)) / len(password))
                
                values = [length_score, uppercase_score, lowercase_score, 
                         digits_score, special_score, uniqueness_score]
                
                # Create radar chart
                fig = plt.figure(figsize=(6, 6))
                ax = fig.add_subplot(111, polar=True)
                
                # Plot the values
                angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
                values = values + [values[0]]  # Close the loop
                angles = angles + [angles[0]]  # Close the loop properly
                categories = categories + [categories[0]]  # Close the loop
                
                ax.plot(angles, values, 'o-', linewidth=2)
                ax.fill(angles, values, alpha=0.25)
                ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1])
                ax.set_ylim(0, 1)
                ax.grid(True)
                
                # Display the chart
                st.pyplot(fig)
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter a password to analyze.")
    
    # Password tips
    with st.expander("Password Security Tips"):
        st.markdown("""
        ### Tips for Creating Strong Passwords
        
        1. **Use a passphrase**: A sequence of random words is often more secure and easier to remember than a complex password.
        2. **Avoid personal information**: Don't use names, birthdays, or other personal details that could be guessed.
        3. **Don't reuse passwords**: Use a different password for each account.
        4. **Consider a password manager**: Tools like LastPass, 1Password, or Bitwarden can generate and store strong passwords.
        5. **Enable two-factor authentication**: This adds an extra layer of security beyond just your password.
        """)

# Password Generator Tab
with tab2:
    st.subheader("Generate a Strong Password")
    
    # Password generation options
    col1, col2 = st.columns(2)
    
    with col1:
        length = st.slider("Password Length", min_value=8, max_value=32, value=16, step=1)
    
    with col2:
        include_uppercase = st.checkbox("Include Uppercase Letters", value=True)
        include_digits = st.checkbox("Include Numbers", value=True)
        include_special = st.checkbox("Include Special Characters", value=True)
    
    # Generate button
    if st.button("Generate Password", key="generate_btn"):
        with st.spinner("Generating secure password..."):
            # Add a small delay for effect
            time.sleep(0.5)
            
            # Generate password
            generated_password = generate_password(
                length=length,
                include_uppercase=include_uppercase,
                include_digits=include_digits,
                include_special=include_special
            )
            
            # Get password analysis
            score, feedback, strength = check_password_strength(generated_password)
            
            # Display generated password
            st.code(generated_password, language=None)
            
            # Display strength information
            if strength == "Very Strong":
                st.success(f"Password Strength: {strength} (Score: {score}/7)")
            elif strength == "Strong":
                st.success(f"Password Strength: {strength} (Score: {score}/7)")
            elif strength == "Moderate":
                st.warning(f"Password Strength: {strength} (Score: {score}/7)")
            else:
                st.error(f"Password Strength: {strength} (Score: {score}/7)")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center;'>
<p>Created with ❤️ by Password Professor | 2025</p>
</div>
""", unsafe_allow_html=True)