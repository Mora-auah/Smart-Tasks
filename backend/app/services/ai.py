"""OpenAI Responses API integration (phases 3-4). Not implemented yet.

Rules from the spec:
- store=False on every call; history is re-sent from chat_messages each turn.
- All outbound text goes through services.masking.mask(); responses through unmask().
- Structured output with strict JSON schemas; search_tasks is the only tool.
- Tool loop: at most 5 rounds, one retry on network/rate-limit errors.
- The model never mutates data; it only proposes actions (stored in ai_actions).
"""


def daily_summary(*args, **kwargs):
    raise NotImplementedError


def chat_turn(*args, **kwargs):
    raise NotImplementedError
