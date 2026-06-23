from __future__ import annotations


def agreement_judge_prompt(user_prompt: str, candidate_resp: str, oracle_resp: str) -> str:
    return f"""You are an objective evaluator. Given the user prompt, compare Candidate and Oracle responses.
Return JSON ONLY with keys: agreement (float 0-1), notes (short string).

Prompt: {user_prompt}

Candidate Response:
{candidate_resp}

Oracle Response:
{oracle_resp}

Scoring rules:
- Start with 1.0 and deduct for: factual errors (0.5), missing required steps (0.3), hallucinated facts (0.5), wrong format (0.2).
- If responses are semantically equivalent, return agreement: 1.0.
- If candidate misses critical details present in oracle, reduce score proportionally.
- Use conservative scoring; output a float between 0.0 and 1.0.

Return:
{{"agreement": 0.95, "notes": "candidate misses budget estimate"}}
"""
