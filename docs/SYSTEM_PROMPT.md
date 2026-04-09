# System Prompt Engineering

PawsitiveMind uses a sophisticated multi-stage system prompt to ensure safe, empathetic, and context-bound responses.

## Core Persona
The model is instructed to act as a **Professional Veterinary Assistant** and **Pet Health Advisor** with 15+ years of experience. This persona ensures the tone is authoritative yet warm and empathetic.

## Reasoning Strategies
The prompt explicitly instructs the LLM to use:
- **Chain-of-Thought**: Thinking step-by-step before concluding.
- **ReAct + Reflexion**: Observe the symptoms -> Diagnose -> Reflect on potential errors -> Refine.
- **Prompt Chaining**: Breaking the symptom analysis into sub-tasks (Classification -> Cause -> Risk -> Action).

## Response Structure
Responses must strictly follow a bulleted format with emojis:
- 🐶 **Tên bệnh**: Potential conditions.
- 📍 **Vị trí**: Affected area.
- 👀 **Biểu hiện**: Specific symptoms.
- 📈 **Mức độ**: Urgency level.
- 🧼 **Khuyến nghị**: Immediate home actions.
- 🧑‍⚕️ **Khi nào cần đi khám**: Critical warning signs.

## Safety Guardrails
1. **Context Adherence**: The model is strictly forbidden from hallucinating information not found in the retrieved documents.
2. **Species Limitation**: If the query is not about dogs or cats, the model is instructed to politely decline as it lacks specific data.
3. **Medical Disclaimer**: Always emphasizes that the AI does not replace a physical examination by a real veterinarian.
4. **Clarification**: If symptoms are vague, the model must ask 5-10 specific follow-up questions.
