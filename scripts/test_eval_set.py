import json
from google.adk.evaluation.eval_set import EvalSet

with open("evals/summarizer_eval_set.json", "r", encoding="utf-8") as f:
    data = json.load(f)

eval_set = EvalSet.model_validate(data)

print("OK: EvalSet valid")
print("Eval set:", eval_set.eval_set_id)
print("Cases:", len(eval_set.eval_cases))

for case in eval_set.eval_cases:
    print("-", case.eval_id)