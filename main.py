import lean
from datetime import datetime
import gpt
import json

MAX_RETRY_COUNT = 10
MAX_ROUNDS = 100

class Interaction:
    ctx : str #current proof context in lean
    code : str #current lean code
    logfile : str #name of the log file
    conversation : list[dict[str,str]]

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
        response = gpt.gpt(self.conversation, gpt.LeanOutput)
        code = response['lean'] + '\nsorry'
        print('-----------------------')
        print(code)
        print('-----------------------')
        #pipeline the generated code into repl
        self.code, self.ctx = lean.fill_and_run(self.code, -1, code)


    def retry(self, err_info) -> None:
        for _ in range(MAX_RETRY_COUNT):
            self.conversation.append({
                "role" : "user",
                "content" : f'''error: {err_info}'''
            })
            try:
                self.process_response()
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

code = """
import Mathlib.Data.Real.Sqrt
import Mathlib.Data.Real.Irrational
open NNReal
open Classical
example (p q : Nat) (h : q ≠ 0) : ¬ ((sqrt 2 + sqrt 3 : Real) = Rat.normalize (p) (q) (h)) := by
sorry
"""


if __name__ == "__main__":
    with open("prompt.txt", "r") as f:
        prompt = f.read()
    with open("input_text.txt", "r") as f:
        prompt += f.read()

    inter = Interaction(code,prompt)
    try:
        for _ in range(MAX_ROUNDS):
            s = input("enter instruction ('exit' to stop): \n")
            if s.lower()=="exit":
                break
            if not s:
                print("empty instruction")
                continue
            inter.comm(s)
    finally:
        inter.save_log()
