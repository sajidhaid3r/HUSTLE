import requests

user_prompt="Ronaldo winning the world cup, along with the best player award, is a historic moment in football history. It showcases his exceptional talent, dedication, and leadership on the field. Ronaldo's performance throughout the tournament was outstanding, and his ability to inspire his team to victory is commendable. This achievement solidifies his legacy as one of the greatest footballers of all time."

url=f"https://image.pollinations.ai/prompt/{user_prompt}"

print(f"Generating for: {user_prompt}")

response=requests.get(url)

print(response)

if response.status_code==200:
    with open("GOAT.png","wb") as file:
        file.write(response.content)
    print("Success")
else:
    print("ERROR")