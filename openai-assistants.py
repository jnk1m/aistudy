from openai import OpenAI
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 키 가져오기
def retrieve_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key

# OpenAI 클라이언트 초기화
def create_openai_client(api_key):
    return OpenAI(api_key=api_key)

# 어시스턴트 생성 또는 가져오기
def fetch_or_create_assistant(client):
    assistant_id =  os.environ.get('ASSISTANT_ID')
    if not assistant_id:
        assistant = client.beta.assistants.create(
            name="DineDecider",
            instructions=(
                "You are the world's best culinary recommendation system. "
                "DineDecider is tailored for recommending dishes and recipes based on the user's specific dining situation. "
                "It provides suggestions for dishes that match the occasion, number of people, cooking difficulty, and preferred cuisine style. "
                "The system then presents a selection of appropriate recipes and, upon the user's choice, delivers a detailed and widely-used recipe. "
                "Each response includes a comprehensive recipe with ingredients and step-by-step instructions."
            ),
            response_format={"type": "json"},
            tools=[{"type": "retrieval"}],
            model="gpt-3.5-turbo"
        )
        assistant_id = assistant.id
    return assistant_id

# 스레드 생성 또는 가져오기
def obtain_thread_id(client):
    thread_id = os.getenv("OPENAI_THREAD_ID")
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
    return thread_id

# 메시지 추가
def append_message(client, thread_id, content):
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

# 어시스턴트 실행 및 결과 출력
def execute_and_display_results(client, thread_id, assistant_id):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        for msg in messages.data:
            print(msg.content[0].text.value)
            print('-------')
    else:
        print(f"Current run status: {run.status}")

# 메인 함수
def main():
    api_key = retrieve_api_key()
    client = create_openai_client(api_key)
    assistant_id = fetch_or_create_assistant(client)
    thread_id = obtain_thread_id(client)

    message_content = "부모님과 함께하는 주말 저녁 식사 메뉴를 추천해줘. 만들기 쉬운 한식요리면 좋겠어."
    append_message(client, thread_id, message_content)
    
    execute_and_display_results(client, thread_id, assistant_id)

if __name__ == "__main__":
    main()
