import lean
from datetime import datetime
import gpt
import json
from typing import List, Dict
import prover
from pathlib import Path

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

    def __init__(self, code, prompt) -> None:
        self.code = code
        self.ctx = lean.fill_and_run(code, -1, 'sorry')
        self.logfile = f"logs/conversation_{datetime.now():%Y%m%d_%H%M%S}.json"
        self.conversation = [{"role": "system", "content": prompt}]

    def save_log(self) -> None:
        print(f"saving log to {self.logfile}")
        with open(self.logfile, "a", encoding='utf-8') as f:
            json.dump(self.conversation, f, ensure_ascii=False, indent=4)

    def process_response(self) -> None:
        #send message to gpt
        
        response = prover.prove(self.conversation)
        # response = gpt.gpt(self.conversation, gpt.LeanOutput)
        self.conversation.append({"role": "assistant", "content": str(response)})
        # code = response['lean'] + '\nsorry'
        code = response
        print('-----------------------')
        print(code)
        print('-----------------------')
        #pipeline the generated code into repl
        self.code, self.ctx = lean.fill_and_run(self.code, -1, code)

    def finish(self) -> None:
        self.code, self.ctx = lean.fill_and_run(self.code, -1, 'aesop')

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
                print(f"error : {err_info}, retrying...")

        raise Exception("failed after too many retries")


    def comm(self, uinput) -> None:
        self.conversation.append({
            "role" : "user",
            "content" : f'''proof context: {self.ctx}\n user_input: {uinput}'''
        })
        try:
            self.process_response()
        except lean.LeanError as e:
            err_info = e.args[0]
            print(f"error : {err_info}, retrying...")
            self.retry(err_info)




if __name__ == "__main__":
    MAX_RETRY_COUNT = 5
    MAX_ROUNDS = 100

    with open("prover_prompt.txt", "r") as f:
        prompt = f.read()
    # with open("input_text.txt", "r") as f:
    #     prompt += f.read()

    code = """def op {S : Type} (a : S) (b : S) : S := a

example {S : Type} (a b c : S) : op a (op b c) = op (op a b) c := by
  sorry
  
  
"""
    
    # code = load_problem("problems/p7.txt")

    inter = Interaction(code, prompt)
    try:
        for _ in range(MAX_ROUNDS):
            s = input("enter instruction ('exit' to stop, 'done' to close): \n")
            if s.lower()=="exit":
                break
            if s.lower()=="done":
                try: inter.finish(); break
                except: print("cannot finish yet"); continue
            if not s:
                print("empty instruction")
                continue
            inter.comm(s)
    finally:
        inter.save_log()
