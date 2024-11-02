import asyncio
from app.services.gpt_service import GPTService

async def main():
    service = GPTService()
    code_files = {
        "file1.py": "def add(a, b): return a + b",
        "file2.py": "def subtract(a, b): return a - b"
    }
    assignment_description = "Review the code for any potential improvements or issues."
    candidate_level = "Junior Developer"

    try:
        response = await service.analyze_code(code_files, assignment_description, candidate_level)
        print("Response from GPTService:")
        print(type(response))
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(main())