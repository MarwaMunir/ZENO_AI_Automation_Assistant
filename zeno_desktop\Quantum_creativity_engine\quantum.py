import os
import asyncio
import random
from dotenv import load_dotenv
from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler as AerSampler
from openai import AsyncOpenAI

# Load API key
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_KEY"))

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

# 🎲 Generate quantum seed using 6 qubits
def generate_quantum_seed():
    num_qubits = 6                      
    circuit = QuantumCircuit(num_qubits)
    for i in range(num_qubits):
        circuit.h(i)    #applying a hadamard gate h for superposition
    circuit.measure_all()

    sampler = AerSampler()
    job = sampler.run([circuit], shots=1000)  #simulate circuit 1000 times
    result = job.result()
    probs = result.quasi_dists[0]    #result contain probability distribution  over all 6 bits ststes
    print(probs)

    processed_probs = {
        format(state, f'0{num_qubits}b'): prob
        for state, prob in probs.items()
    }

    binary_seed = random.choices(
        population=list(processed_probs.keys()),
        weights=list(processed_probs.values()),
        k=1
    )[0]                 #pick one 6 bit seed by probability (quantum)

    return f"Creativity Seed {binary_seed} -- used to influence creative parameters."


# 🎨 Enhanced mutation logic
def mutate_prompt_by_seed(prompt, seed_str):
    seed = seed_str.replace("Creativity Seed ", "").split(" ")[0].zfill(6)

    # Segment 1: Mood / Theme
    if seed[0:2] == "00":
        prompt += "  the idea must work offline and use no mouse."
    elif seed[0:2] == "01":
        prompt += " The idea should challenge perceptions of time and sequence."
    elif seed[0:2] == "10":
        prompt += " Infuse speculative tech like brain-machine interfaces."
    else:
        prompt += " Enable the idea to run in alternate realities (AR/VR)."

    # Segment 2: Aesthetic Twist
    if seed[2:4] == "00":
        prompt += " Give it a minimalist interface with a single input field."
    elif seed[2:4] == "01":
        prompt += " Add a retro twist, inspired by 80s arcade machines."
    elif seed[2:4] == "10":
        prompt += " Make it feel like a dream, using subconscious metaphors."
    else:
        prompt += " Involve sound-based interactions or sonification."

    # Segment 3: Perspective / Usage
    if seed[4:6] == "00":
        prompt += " Imagine this idea is for children or teenagers."
    elif seed[4:6] == "01":
        prompt += " It should be used by AI agents, not just humans."
    elif seed[4:6] == "10":
        prompt += " Focus on nonverbal communication or body language."
    else:
        prompt += " Make it useful in remote, off-grid environments."

    return prompt

# 🔥 Temperature based on entropy of seed
def calculate_temperature(seed_str):
    binary = seed_str.replace("Creativity Seed ", "").split(" ")[0]
    entropy = sum(int(b) for b in binary)
    return 0.7 + (entropy / 6) * 0.1  # ~ 0.7 - 1.3   #calculate entropy(sum of 1s in seed)

# 💭 Prompt generation
def generate_prompt(mood, domain, seed, custom_thought=None):
    prompt = (
        f"Act as a inventive software architect who proposes groundbreaking, creative, extraordinary and technically feasible coding project ideas. "
        f"The user feels {mood} and is curious about {domain}. "
        f"The random creativity seed is: '{seed}'. "
    )
    if custom_thought:
        prompt += f"They are also thinking: {custom_thought}. "

    # Inject complex mutations from full seed
    prompt = mutate_prompt_by_seed(prompt, seed)

    prompt += (
        " Your generated idea MUST satisfy ALL of the above constraints from the seed exactly and fully. "
    "Do NOT ignore or loosely interpret any of the constraints. "
    "Generate a project idea that feels revolutionary or futuristic, possibly blending unusual fields or techniques. "
    "Explain the idea in clear, concise, and programmer-friendly terms. Avoid poetic or overly metaphorical language. "
    "Include details such as the user interface, how it works, what technologies or libraries might be used, and why it matters. "
    "The idea can be imaginative, something not very common in the market, but the explanation should be grounded and buildable."
    )
        
    
    return prompt

# 🤖 Async idea generator
async def get_creative_idea(user_mood=None, tech_domain=None, custom_thought=None):
    mood = user_mood or random.choice(MOODS)
    domain = tech_domain or random.choice(DOMAINS)
    seed = generate_quantum_seed()
    prompt = generate_prompt(mood, domain, seed, custom_thought)
    temperature = calculate_temperature(seed)

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
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
    
#Interface
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
        
