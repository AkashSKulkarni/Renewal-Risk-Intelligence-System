from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto"
)


def ask_model(prompt):

    messages = [
        {
            "role": "system",
            "content":
            (
             "You are a precise assistant. "
             "Return valid JSON only when asked. "
             "Never use markdown code fences."
            )
        },

        {
            "role":"user",
            "content":prompt
        }
    ]


    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        [text],
        return_tensors="pt"
    ).to(model.device)


    output_ids = model.generate(
        **inputs,
        max_new_tokens=600,
        do_sample=False
    )


    generated_ids = [
        out[len(inp):]
        for inp, out in zip(
            inputs.input_ids,
            output_ids
        )
    ]


    response = tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    return response



def analyze_csm_notes(notes):

    prompt = f"""
Return ONLY valid JSON.

[
 {{
   "account_id":1000,
   "sentiment":"negative",
   "churn_intent":true,
   "risk_signals":[
      "competitor evaluation"
   ]
 }}
]

No markdown.
No explanation.

Notes:
{notes}
"""

    return ask_model(prompt)



def analyze_changelog(changelog):

    prompt = f"""
Return ONLY valid JSON.

{{
 "sdk_deprecated": true,
 "editor_migration_risk": true,
 "breaking_api_risk": true
}}

No markdown.

Changelog:
{changelog}
"""

    return ask_model(prompt)



def generate_explanation(features):

    prompt = f"""
Return ONLY valid JSON.

{{
  "risk_summary": "string",
  "key_reasons": ["string"],
  "recommended_actions": ["string"]
}}

Rules:
- Be specific and actionable
- Actions must be practical for Customer Success teams
- No markdown, no explanation outside JSON

Data:
{features}
"""

    return ask_model(prompt)
