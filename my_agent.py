 from google import genai

# Apni poori 'AQ...' waali key yahan paste kijiye
client = genai.Client(api_key="YOUR_API_KEY_HERE")

print("\n--- Connection Shuru... ---\n")

# Hum direct 2.5-flash model use karenge jo is naye format ke liye valid hai
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="Give a complete 2-week MVP launch plan for 'AI Product Photo Studio for Shopify' to sell on Acquire.com."
)

print("\n--- Final Output ---")
print(response.text)  