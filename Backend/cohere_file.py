API_KEY = 'FfzfGriLQELxRINyB2dBDsWxFgEetEeIu3fcjhbA'



import cohere
co = cohere.ClientV2(API_KEY)
response = co.chat(
    model="command-r-plus", 
    messages=[{"role": "user", "content": "hello world!"}]
)
print(response)