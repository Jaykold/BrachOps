import random

def generate_random_port():
    return random.randint(30000, 32767)  # NodePort range