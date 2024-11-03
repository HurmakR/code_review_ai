#import asyncio
#from app.services.gpt_service import GPTService
#
#async def main():
#    service = GPTService()
#    code_files = {
#        "test.py": "https://github.com/HurmakR/test/blob/main/test.py",
#        "gsx2.py": "https://github.com/HurmakR/test/blob/main/gsx2.py",
#        "app.py": "https://github.com/HurmakR/test/blob/main/app.py"
#    }
#    assignment_description = "Review the code for any potential improvements or issues."
#    candidate_level = "Junior Developer"
#
#    try:
#        response = await service.analyze_code(code_files, assignment_description, candidate_level)
#        print("Response from GPTService:")
#        print(type(response))
#        print(response)
#    except Exception as e:
#        print(f"An error occurred: {e}")
#
#asyncio.run(main())
#
#
import json

text = '''
{
    "comments": "The code looks rather decent but there are some issues noted that need to be improved on:\\n\\n 1. Comments are not in English - it's important to keep comments in English as programming is universally done in English.\\n\\n 2. General organization and structure of the code can be improved. The Python code should be refactored for better organization and easy navigation. For instance, the `app.py` has a `/result` route that is very long and does a lot of things, this hinders readability and testability.\\n\\n 3. Error handling - currently, the code does not handle for errors such as file not found or csv reading errors.\\n\\n 4. For the `app.py`, the use of hardcoded string is rampant and might pose a problem when these strings need to be updated or they are reused across other part of the application. You can declare them as constants at the top of your file.\\n\\n 5. Unit tests are missing - Unit tests help ensure every part of the code behaves as expected and makes debugging easier by narrowing down the list of changes that could have caused the bug.\\n\\n 6. In `gsx2.py`, the code opens a csv file `gsx = open(values['file2'], encoding='Windows-1251')` but does not ensure to close it. It's better to use `with open...` which automatically closes the file.\\n\\n 7. The application doesn't look like it can download GitHub repositories, as the task description requested.",
    "rating": "2",
    "conclusion": "The code generally needs more refinement in several areas: structure, error handling, usage of constants, closing opened files and adding unit tests. It also seems that the code's functionality does not align with the provided task description."
}
'''

data_dict = json.loads(text)
print(data_dict)
