import requests
import json

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5MzQ0ZTY1LWJiYzktNDRkMS1hOWQwLWY5NTdiMDc5YmQwZSIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSJdLCJjbGllbnRfaWQiOiJhcHBfWDh6WTZ2VzJwUTl0UjNkRTduSzFqTDVnSCIsImV4cCI6MTc2MTE0MzIyMywiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9hdXRoIjp7ImNoYXRncHRfY29tcHV0ZV9yZXNpZGVuY3kiOiJub19jb25zdHJhaW50IiwiY2hhdGdwdF9kYXRhX3Jlc2lkZW5jeSI6Im5vX2NvbnN0cmFpbnQiLCJ1c2VyX2lkIjoidXNlci1LRkdUNFpxaWx3MHl6a3ZHaDRZV1dyR3UifSwiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9wcm9maWxlIjp7ImVtYWlsIjoiZWhkZGVqd3dAb3V0bG9vay5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImlhdCI6MTc2MDI3OTIyMiwiaXNzIjoiaHR0cHM6Ly9hdXRoLm9wZW5haS5jb20iLCJqdGkiOiJkYWFiODRlNi04YTI4LTQ2ZGEtODRhNC0yOTk3NjU3YmIyMGMiLCJuYmYiOjE3NjAyNzkyMjIsInB3ZF9hdXRoX3RpbWUiOjE3NjAyNzkyMjAwNzQsInNjcCI6WyJvcGVuaWQiLCJlbWFpbCIsInByb2ZpbGUiLCJvZmZsaW5lX2FjY2VzcyIsIm1vZGVsLnJlcXVlc3QiLCJtb2RlbC5yZWFkIiwib3JnYW5pemF0aW9uLnJlYWQiLCJvcmdhbml6YXRpb24ud3JpdGUiXSwic2Vzc2lvbl9pZCI6ImF1dGhzZXNzX1VEZTJDN29GVUdKaFUwZklQc2w1WU9ydSIsInN1YiI6IndpbmRvd3NsaXZlfDc2YjAyZWZiNjFlYTczY2EifQ.iCwpSQuiD-E4_GY9joNze5DJdI8vbJZnu2faaoGhxGLt6z-DL_jCvTr1hzBuO-qN3FtZqdkBY6NFhfM1daRvUOO6nnsBhbAx5Lg6DBT18JxPHw1uFvId_bepdRY8gXG6tMarARncF1SmatmPEhIc6uopqzUnUz4AXqfxbh5ocy187uSOmPOtXwvxSb0LGqoj2HwN8SaWlbHxu2icgmHn7qQXkoKjNMJaVF2sTHjCo2JHWOmvgeUPpZv5hS-8NQDOyh5j7nwrh0ae6uLSH9PtmyooeGz6fSLg-3URi_Rrv9Qme7ZhVWyvh7svhaDvv0y0gFyQG-EpXK-9mXgE46e9Bs__PgWG7fg9aFgQynyBmUxuzlRpZkavJA7NNNfp7tnSkwbVlbzzn2zIffi-wsaBJZSu5Vqp1e97uG9WwJSdJ0QyeweLSfH7ahIRhz3ujtCs16Jg41UMR-Ef9GLz50eEDA5Z4QEKh7s6gskcuii7ZnwyT2Y16DjHDk0AU3m2nWz9474nzwR13vLO_28bIrxGKbtn_v8VEB6oyO_jAgr0lv1JwR9iYFEk8p0R5cN9ESFltH62SjZxMrGVgf9eP2eO5gvjPN62U4YNd65RU2rhEyh7jWhxC30XLAvR6T1jDPDxoQR9xB22fIpJr3R4s8UEFyAjjU_4umBUTiCAvg6L7wk',  # 需要替換為你的AT
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'oai-language': 'zh-CN',
    'origin': 'https://chatgpt.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://chatgpt.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"140.0.7339.210"',
    'sec-ch-ua-full-version-list': '"Chromium";v="140.0.7339.210", "Not=A?Brand";v="24.0.0.0", "Google Chrome";v="140.0.7339.210"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
}

json_data = {
    'plan_name': 'chatgptteamplan',
    'team_plan_data': {
        'workspace_name': 'Fovt',
        'price_interval': 'month',
        'seat_quantity': 5,
    },
    'billing_details': {
        'country': 'JP',
        'currency': 'USD',
    },
    'cancel_url': 'https://chatgpt.com/?numSeats=5&selectedPlan=month&referrer=https%3A%2F%2Fauth.openai.com%2F#team-pricing-seat-selection',
    'promo_campaign': 'team-1-month-free',
    'checkout_ui_mode': 'redirect',
}

# 這裡設置要生成的付款鏈接數量
num_links = 5

print(f"正在生成 {num_links} 個ChatGPT Team付款鏈接...")
print("=" * 50)

for i in range(num_links):
    try:
        response = requests.post(
            'https://chatgpt.com/backend-api/payments/checkout', 
            headers=headers, 
            json=json_data
        )
        response_data = response.json()
        id = response_data["checkout_session_id"]  
        url = f"https://chatgpt.com/checkout/openai_llc/{id}"
        print(f"鏈接 {i+1}: {url}")
    except Exception as e:
        print(f"生成鏈接 {i+1} 時出錯: {str(e)}")

print("=" * 50)
print("所有鏈接已生成完畢！")
print("請依次打開這些鏈接進行付款，每成功付款一個，您的帳號將增加一個Team訂閱。")