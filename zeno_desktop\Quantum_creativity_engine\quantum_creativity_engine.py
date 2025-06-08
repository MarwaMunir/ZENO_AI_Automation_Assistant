import os
import asyncio
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit_aer.primitives import Sampler as AerSampler
import openai
from openai import AsyncOpenAI
from dotenv import load_dotenv
import random
import numpy as np

# Load environment variables
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_KEY"))

# Expanded moods and domains
MOODS = [
    "dreamy", "intense", "philosophical", "electric", "playful", "melancholic", "cosmic", "limitless", "fluid",
    "hypnotic", "glitchy", "immersive", "rebellious", "jaded", "focused", "flowing", "curious", "frustrated", 
    "bold", "chaotic", "lucid", "wired", "anxious", "euphoric", "obsessed", "meditative", "restless", "haunted", "empowered"
]


DOMAINS = [
    "code interfaces", "AI tools", "neurotech", "emotion-based programming", "generative AI", "future UX", 
    "web metaphors", "holographic design", "voice interaction", "gesture systems", "dream-state compilers", 
    "generative art", "semantic search engines", "self-aware IDEs", "invisible UI", "time-based version control", 
    "biofeedback systems", "synthetic empathy algorithms", "quantum programming education", "mental model visualizers", 
    "AI companions for debugging", "ambient coding environments", "zero-click UI", "neural input editors", 
    "real-time mood-aware apps", "creative developer tools", "interactive thought mapping", "AI orchestration", 
    "multi-sensory coding", "emergent system design", "AR/VR for coders", "non-linear project timelines", "introspective IDEs"
]

def binary_to_index(binary_string, max_length):
    index = int(binary_string, 2)
    return index % max_length

def mutate_prompt_by_seed(prompt, binary_seed):
    if binary_seed == "00":
        return prompt + " Add a constraint: the tool must work offline and be fully keyboard navigable."
    elif binary_seed == "01":
        return prompt + " The idea should involve temporal logic or time perception."
    elif binary_seed == "10":
        return prompt + " Inject sci-fi concepts like memory implants or holographic data."
    elif binary_seed == "11":
        return prompt + " Make the project work in AR space or use biometric data."
    return prompt

def quantum_mood_fusion(seed, moods):
    idx = int(seed, 2)
    primary = moods[idx % len(moods)]
    secondary = moods[(idx * 3) % len(moods)]
    return f"{primary} + {secondary}"

def calculate_temperature(seed):
    entropy = sum([int(bit) for bit in seed])
    return 0.6 + (entropy / 2) * 0.1



# Quantum seed generator using Qiskit for true randomness
def generate_quantum_seed():
    # Create the quantum circuit
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    # Sampler does not include measurements; it samples probabilities of states
    sampler = AerSampler()
    job = sampler.run([circuit],shots=1000)
    result = job.result()

    # Get probabilities and sample manually
    probs = result.quasi_dists[0]
    # Convert keys to binary strings if needed
    processed_probs = {}
    for state, prob in probs.items():
        binary_state = format(state, '04b') if isinstance(state, int) else str(state).zfill(4)
        processed_probs[binary_state] = prob
        #if isinstance(state, int):
            #binary_state = format(state, '02b')
        #elif isinstance(state, str):
            #binary_state = state.zfill(2)
        #elif isinstance(state, tuple):
            #binary_state = ''.join(map(str, state))
        #else:
            #continue
        #processed_probs[binary_state] = prob

    # Sample based on the true quantum distribution
    binary_seed = random.choices(
        population=list(processed_probs.keys()),
        weights=list(processed_probs.values()),
        k=1
    )[0]

    seed_description = f"Creativity Seed {binary_seed} -- used to influence creative parameters."
    return seed_description

# Generate a creative prompt
def generate_prompt(mood, domain, seed, custom_thought=None):
    prompt = (
        f"Act as a inventive software architect  who proposes groundbreaking,creative, extraordinary and  technically feasible coding project ideas,that are not common,but highly creative. "
        f"The user feels {mood} and is curious about {domain}. "
        f"The random  creativity seed is: '{seed}'. "
    )
    if custom_thought:
        prompt += f"They are also thinking: {custom_thought}. "

    # Inject seed-driven idea mutation
    binary_tail = seed[-2:]
    prompt = mutate_prompt_by_seed(prompt, binary_tail)

    prompt += (
        "Generate a project idea that feels revolutionary or futuristic, possibly blending unusual fields or techniques and is creative. "
        "Explain the idea in clear, concise, and programmer-friendly terms. Avoid poetic or overly metaphorical language. "
        "Include details such as the user interface, how it works, what technologies or libraries might be used, and why it matters. "
        "The idea can be imaginative,something not very common in the market,something that is a blend of amamzing libraries and domains,something that has not been thought about before, but the explanation should be grounded and buildable."
    )
    return prompt

# Query OpenAI's GPT-4 to generate a creative idea
async def get_creative_idea(user_mood=None, tech_domain=None, custom_thought=None):
    mood = user_mood or random.choice(MOODS)
    domain = tech_domain or random.choice(DOMAINS)
    seed = generate_quantum_seed()  # Use quantum seed for randomness
    prompt = generate_prompt(mood, domain, seed, custom_thought)

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.95,
            max_tokens=400
        )
        

        idea = response.choices[0].message.content.strip()
        return {
            "idea": idea,
            "mood": mood,
            "domain": domain,
            "seed": seed,
            "prompt": prompt
        }

    except Exception as e:
        return {"error": str(e)}

# Main function
async def main():
    print("\n🔮 Welcome to the Creativity Engine 🔮\n")

    # Display available moods
    print("Available Moods:")
    for i, mood in enumerate(MOODS, 1):
        print(f"{i}. {mood}")

    
    mood = input("🌀 Your current mood? : ").strip()

    # Display available domains
    print("\nAvailable Domains:")
    for i, domain in enumerate(DOMAINS, 1):
        print(f"{i}. {domain}")

    domain = input("💡 Tech domain you're curious about?: ").strip()
    thought = input("🧠 Any specific thought or interest? (Optional): ").strip()

    print("\n⚛️ Firing quantum seed and entangling creative fields... Please wait.\n")

    result =await get_creative_idea(
        user_mood=mood if mood else None,
        tech_domain=domain if domain else None,
        custom_thought=thought if thought else None
    )

    if "idea" in result:
        print("✨ Quantum Idea Generated ✨\n")
        print(f"🌀 Mood: {result['mood']}")
        print(f"💡 Domain: {result['domain']}")
        print(f"🌱 Quantum Seed: {result['seed']}\n")
        print(result["idea"])
    else:
        print("❌ Error:", result["error"])

if __name__ == "__main__":
    asyncio.run(main())
