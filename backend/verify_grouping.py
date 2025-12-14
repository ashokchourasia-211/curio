import json
import time
import urllib.request
import sys

BASE_URL = "http://localhost:8000/api/v1"


def request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")

    if data:
        body = json.dumps(data).encode("utf-8")
        req.data = body

    try:
        with urllib.request.urlopen(req) as response:  # nosec
            if response.status >= 200 and response.status < 300:
                resp_body = response.read().decode("utf-8")
                if resp_body:
                    return json.loads(resp_body)
                return {}
    except urllib.error.HTTPError as e:
        print(f"Error {e.code} for {url}: {e.read().decode('utf-8')}")
        sys.exit(1)
    except Exception as e:
        print(f"Exception for {url}: {str(e)}")
        sys.exit(1)


def main():
    print("Starting Verification...")

    # 1. Create Session
    print("Creating Session...")
    session_data = request(
        "POST", "/sessions", {"teacher_id": "test_teacher", "subject": "Physics"}
    )
    session_id = session_data["session_id"]
    print(f"Session Created: {session_id}")

    # 2. Post Similar Questions
    q_texts = [
        "How does gravity work?",  # Q1
        "Explain gravity to me",  # Q2 (Should match Q1)
        "What is the capital of India?",  # Q3 (Different)
    ]

    print("Posting Questions...")
    for text in q_texts:
        request(
            "POST",
            "/questions",
            {"session_id": session_id, "text": text, "student_hash": "test_user"},
        )
        time.sleep(1)  # Give a little time for processing

    # 3. Check Groups
    print("Checking Groups...")
    # Give DB a moment to settle if async/eventual consistency (SQLite is sync but good practice)
    time.sleep(2)

    groups = request("GET", f"/sessions/{session_id}/groups")
    print(f"Groups Found: {len(groups)}")

    if len(groups) != 1:
        print(f"FAILURE: Expected 1 group, found {len(groups)}")
        # We might continue to debug or exit.
        # But wait, maybe the first question didn't create a group until the second one arrived?
        # Q1: No match.
        # Q2: Matches Q1. Creates Group G1. Q1 and Q2 assigned to G1.
        # Q3: No match.
        # So yes, 1 group expected.
    else:
        group = groups[0]
        count = group["question_count"]
        print(f"Group ID: {group['id']}, Count: {count}")
        if count != 2:
            print(f"FAILURE: Expected group count 2 (gravity questions), got {count}")

        # 4. Answer Group
        print("Answering Group...")
        gid = group["id"]
        answer_text = "Gravity is the curvature of spacetime."
        request("POST", f"/groups/{gid}/answer", {"answer": answer_text})

        # 5. Verify Answers
        print("Verifying Answers Update...")
        questions = request("GET", f"/questions/{session_id}")

        gravity_questions = [q for q in questions if "gravity" in q["text"].lower()]
        other_questions = [q for q in questions if "gravity" not in q["text"].lower()]

        for q in gravity_questions:
            if q.get("ai_response") != answer_text:
                # Note: ai_response might be the ORIGINAL AI response if we store teacher answer separately.
                # But in my implementation I overwrote ai_response.
                print(f"FAILURE: Question '{q['text']}' does not have updated answer.")
                print(f"Expected: {answer_text}")
                print(f"Actual: {q.get('ai_response')}")
            else:
                print(f"SUCCESS: Question '{q['text']}' updated correctly.")

        for q in other_questions:
            if q.get("ai_response") == answer_text:
                print(f"FAILURE: Question '{q['text']}' INCORRECTLY updated.")

    print("Verification Script Finished.")


if __name__ == "__main__":
    main()
