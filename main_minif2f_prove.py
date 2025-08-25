import lean_buff2 as lean
from datetime import datetime
# import gpt
import json
from typing import List, Dict
import prover
from pathlib import Path
import re
from tqdm import tqdm

def load_problem(path: str) -> str:
    """
    Load content from a file or all files in a directory.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"{path} does not exist.")

    if p.is_file():
        with open(p, "r", encoding='utf-8') as f:
            # Read the file content

            code = f.read()
            # Optional cleaning
            return code


    elif p.is_dir():
        raise NotImplementedError(f"Loading from directory {path} is not implemented yet.")

    else:
        raise ValueError(f"{path} is neither a file nor a directory.")



class Interaction:
    ctx : str #current proof context in lean
    code : str #current lean code
    logfile : str #name of the log file
    conversation : List[Dict[str,str]]

    def __init__(self,prefix, code, prompt) -> None:
        self.prefix = prefix
        self.code = code
        self.ctx = lean.run_code(self.prefix+ self.code)
        print(self.ctx)
        self.logfile = f"logs/conversation_{datetime.now():%Y%m%d_%H%M%S}.json"
        self.conversation = [{"role": "system", "content": prompt}]
        self.error = ""
        

    def save_log(self) -> None:
        print(f"saving log to {self.logfile}")
        with open(self.logfile, "a", encoding='utf-8') as f:
            json.dump(self.conversation, f, ensure_ascii=False, indent=4)

    def process_response(self) -> None:
        #send message to gpt
        
        ## using only current ones
        response = prover.prove(
            [
                {"role": "system", "content": prompt},
                {"role": "user", "content": self.code},
                {"role": "user", "content": f'''proof states: {self.ctx}'''},
                {"role": "user", "content": self.error}
            ]
        )
        # response = gpt.gpt(self.conversation, gpt.LeanOutput)
        self.conversation.append({"role": "assistant", "content": str(response)})
        # code = response['lean'] + '\nsorry'
        code = response
        print('-----------------------')
        print(code)
        print('-----------------------')
        #pipeline the generated code into repl
        # self.code, self.ctx = lean.fill_and_run(self.code, -1, code)
        self.code = code
        self.ctx = lean.run_code(self.prefix +self.code)
        print(self.ctx)

    def finish(self) -> None:

        self.ctx = lean.run_code(self.prefix + self.code)
        print(self.ctx)

    def retry(self, err_info) -> None:
        for _ in range(MAX_RETRY_COUNT):
            self.conversation.append({
                "role" : "user",
                "content" : f'''error: {err_info}'''
            })
            try:
                self.process_response()
                return
            except lean.LeanError as e:
                err_info = e.args[0]
                ## add e here
                self.error = str(e)

                print(f"error : {err_info}, retrying...")

        raise Exception("failed after too many retries")


    def comm(self) -> None:
        self.conversation.append({
            "role" : "user",
            "content" : f'''proof states: {self.ctx}'''
        })
        try:
            self.process_response()
        except lean.LeanError as e:
            err_info = e.args[0]
            print(f"error : {err_info}, retrying...")
            self.retry(err_info)


def remove_unused_head(content):
    remove_headers = [
        r"import Mathlib\.Algebra\.BigOperators\.Basic",
        r"import Mathlib\.Data\.Nat\.Digits",
        r"open BigOperators"
    ]

    pattern = re.compile("|".join(remove_headers))

    
    filtered_lines = []
    for line in content.splitlines():
        if not pattern.match(line.strip()):
            filtered_lines.append(line)
    filtered_content = "\n".join(filtered_lines)
    return filtered_content

if __name__ == "__main__":
    MAX_RETRY_COUNT = 2
    MAX_ROUNDS = 1

    log_file = "prove_result_438_.jsonl"
    with open("prover_prompt.txt", "r") as f:
        prompt = f.read()


            
    with open ("minif2f_lean4.json", "r") as f:
        problems = json.load(f)




    for i in  tqdm(range(438, len(problems))):
        code = problems[i].get("formal_statement", "")
        prefix = problems[i].get("header", "") 
        prefix = remove_unused_head(prefix) + "\n"

        
        print("---")
        print(prefix + "\n" + code)
        print("---")

        try:
            inter = Interaction(prefix, code, prompt)
            for _ in range(MAX_ROUNDS):
                ## in this logic, then @k, k = MAX_ROUNDS * MAX_RETRY_COUNT
                inter.comm()
            
                with open(log_file, "a", encoding='utf-8') as f:
                    f.write(str({"problem_index": i,"code": inter.code, "result": "no bug, can double check"}) + "\n")

        except Exception as e:
            print(f"Error initializing interaction: {e}")
            with open(log_file, "a", encoding='utf-8') as f:
                f.write(str({"problem_index": i,"code": inter.code, "error": str(e)}) + "\n")
            
        finally:
            inter.save_log()
            
