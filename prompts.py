
def return_prompt(code, prompt_type):

    if prompt_type == "testPrompt":
        prompt1 = f"Human: I am generating a technical document from a PySpark code file. The code is: {code}. Can you generate a summary of what the code will accomplish that is readable by my executive team? Assistant:"
        return prompt1