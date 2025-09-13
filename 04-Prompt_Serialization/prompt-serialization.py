# When we send a prompt to an LLM, it’s not just plain text 
# it has to be serialized (converted into a structured format) depending on the API/protocol.

# 1. OpenAI / Anthropic/ Gemini Style (ChatML Format) - this is what we used by now 
# Conversation is serialized as a list of role–message pairs.

# Roles = system, user, assistant, sometimes tool.

# 
#   {"role": "system", "content": "You are a helpful assistant."},
#   {"role": "user", "content": "What is 2+2?"},
#   {"role": "assistant", "content": "2+2=4"}

# 2 Prompt Style in Alpaca

# Alpaca (and most instruction-tuned models) doesn’t use a chat schema (system, user, assistant).
# Instead, it uses a serialized single-turn instruction format:


#-> Alpaca Prompt structure

### Instructions: <SYSTEM_PROMPT>\n

### Input: <USER_QUERY>

### Response:\n

# Example :

### Instruction: You are a helpful assistant. What is 2+2?

### Input:

### Response:2+2=4


# (INST Prompting) LLaMA-2 / Vicuna / OpenOrca style models. 
# [INST] What is the tiem nowm [/INST]

# example
# begin of text
# <s> 
# [INST] 
# <<SYS>> 
# You are a helpful assistant.
# <</SYS>>
# What is 2+2?
# [/INST]
# 2+2=4 
# </s>


# most of the tech Giants are using CHATML prompting 