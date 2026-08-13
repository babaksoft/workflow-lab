GENERATOR_PROMPT = """Write exactly 4 bullet points about Python generators.

Constraints:

* Each bullet must contain exactly 10 words.
* Do not use the words "lazy", "memory", or "iterator".
"""

JUDGE_PROMPT = """Evaluate the following answer according to these requirements.

Generation requirements:

* The answer must contain exactly 4 bullet points.
* Each bullet must contain exactly 10 words.
* The words "lazy", "memory", and "iterator" must not appear.

Evaluate these rubrics:

* constraint_handling: Does the answer follow all generation requirements?
* word_counting: Does each bullet contain exactly 10 words?
* word_filtering: Does the answer avoid all forbidden words?

Return ONLY valid JSON with exactly this structure:

{{
    "constraint_handling": <integer from 1 to 10>,
    "word_counting": <integer from 1 to 10>,
    "word_filtering": <integer from 1 to 10>,
    "justification": {{
        "constraint_handling": "<short justification>",
        "word_counting": "<short justification>",
        "word_filtering": "<short justification>"
    }}
}}

Answer to judge:

{response}
"""
