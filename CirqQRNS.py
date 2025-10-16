
'''pip install cirq'''
import cirq

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