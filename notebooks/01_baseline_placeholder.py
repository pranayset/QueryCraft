"""Python notebook companion: minimal baseline smoke test."""
from querycraft.generator import generate_cypher

if __name__ == "__main__":
    print(generate_cypher("How many movies are in the database?"))
