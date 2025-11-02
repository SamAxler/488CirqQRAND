#!pip install cirq
import cirq
import random
import time
import math

# Pick a qubit.
qubit = cirq.GridQubit(0, 0)

# Create a circuit
circuit = cirq.Circuit(
    cirq.X(qubit)**0.5,  # Square root of NOT.
    cirq.measure(qubit, key='m')  # Measurement.
)
print("Circuit:")
print(circuit)

# Simulate the circuit several times.
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=20)
print("Results:")
print(result)

m = result.measurements['m']
if(m.ndim == 2 and m.shape[1] == 1):
  decimal_result = 0
  for i,bit in enumerate(m.flatten(),1):
    # Cast bit to a standard Python integer to avoid OverflowError
    decimal_result += int(bit) * (2**(len(m.flatten()) - i))
  print("Decimal result:", decimal_result)



# Benchmarking Quantum RNG vs Classical RNG


# Quantum RNG Benchmark
start_q = time.perf_counter()
result_q = simulator.run(circuit, repetitions=1000)
end_q = time.perf_counter()
quantum_time = end_q - start_q
quantum_bits = result_q.measurements['m'].flatten().tolist()

# Convert every 8 bits into an integer for fair comparison
def bits_to_int(bits):
    n = 0
    for bit in bits:
        n = (n << 1) | bit
    return n

quantum_bytes = [bits_to_int(quantum_bits[i:i+8]) 
                 for i in range(0, len(quantum_bits), 8)]

# Classical RNG Benchmark
start_c = time.perf_counter()
classical_bytes = [random.getrandbits(8) for _ in range(len(quantum_bytes))]
end_c = time.perf_counter()
classical_time = end_c - start_c

# Simple entropy estimation
def entropy(data):
    freq = {b: data.count(b) / len(data) for b in set(data)}
    return -sum(p * math.log2(p) for p in freq.values())

quantum_entropy = entropy(quantum_bytes)
classical_entropy = entropy(classical_bytes)

# Print Results
print("\n--- Benchmark Results ---")
print(f"Quantum RNG time:   {quantum_time:.6f} seconds for {len(quantum_bytes)} bytes")
print(f"Classical RNG time: {classical_time:.6f} seconds for {len(classical_bytes)} bytes")

print("\n--- Randomness Entropy (bits per byte) ---")
print(f"Quantum entropy:   {quantum_entropy:.4f}")
print(f"Classical entropy: {classical_entropy:.4f}")

print("\nSample Quantum Bytes:", quantum_bytes[:10])
print("Sample Classical Bytes:", classical_bytes[:10])
