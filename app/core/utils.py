import asyncio
from app.services.gpt_service import GPTService

async def main():
    service = GPTService()
    code_files = {
        "test.py": "https://github.com/HurmakR/test/blob/main/test.py",
        "gsx2.py": "https://github.com/HurmakR/test/blob/main/gsx2.py",
        "app.py": "https://github.com/HurmakR/test/blob/main/app.py"
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

