import argparse

def refine_prompt(prompt, style="professional"):
    # Lógica básica de refinamiento (ejemplo)
    if style == "professional":
        return f"{prompt} in a professional tone."
    elif style == "casual":
        return f"{prompt} in a casual tone."
    return prompt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refine prompts for LLMs.")
    parser.add_argument("prompt", help="The prompt to refine")
    parser.add_argument("--style", help="Style of the prompt (professional, casual)", default="professional")
    args = parser.parse_args()

    refined_prompt = refine_prompt(args.prompt, args.style)
    print(refined_prompt)
