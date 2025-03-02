import heapq
import csv
import time
import threading

# Flight class to store flight details
class Flight:
    def __init__(self, flight_id, flight_type, priority, emergency=False):
        self.flight_id = flight_id  # Unique flight identifier
        self.flight_type = flight_type  # 'arrival' or 'departure'
        self.priority = priority  # 1 (highest priority) to 10 (lowest priority)
        self.emergency = emergency  # Flag for emergency landings
        self.status = 'waiting'  # 'waiting', 'in_air', 'landed', 'departed'

    def __lt__(self, other):
        # Compare based on priority (lower number = higher priority)
        if self.priority == other.priority:
            return self.flight_id < other.flight_id  # Sort by flight_id if priority is the same
        return self.priority < other.priority

# Runway class to track runway availability
class Runway:
    def __init__(self, runway_id):
        self.runway_id = runway_id
        self.available = True  # True means available, False means occupied

    def __str__(self):
        return f"Runway {self.runway_id} is {'available' if self.available else 'occupied'}"

# Gate class to track gate availability
class Gate:
    def __init__(self, gate_id):
        self.gate_id = gate_id
        self.available = True  # True means available, False means occupied

    def __str__(self):
        return f"Gate {self.gate_id} is {'available' if self.available else 'occupied'}"

# Scheduler class to manage flight assignments
class Scheduler:
    def __init__(self):
        self.runways = []  # List of available runways
        self.gates = []    # List of available gates
        self.queue = []    # Priority queue to handle flight scheduling

    def add_runway(self, runway):
        self.runways.append(runway)

    def add_gate(self, gate):
        self.gates.append(gate)

    def add_flight(self, flight):
        # Insert the flight into the priority queue based on its priority and type (normal/emergency)
        if flight.emergency:
            flight.priority = 0  # Give highest priority for emergency landings
        heapq.heappush(self.queue, flight)

    def assign_gate(self, flight):
        # Assign an available gate to the flight
        print(f"\nAssigning Gate for Flight {flight.flight_id}...")

        # Display all gates with their availability status
        for i, gate in enumerate(self.gates):
            print(f"{i + 1}. {gate}")

        # Let the user choose an available gate
        try:
            choice = int(input("Select an available gate by number: ")) - 1
            if choice < 0 or choice >= len(self.gates):
                raise ValueError("Invalid gate selection.")
            selected_gate = self.gates[choice]
            if not selected_gate.available:
                print(f"Gate {selected_gate.gate_id} is occupied. Try again.")
                return
        except (ValueError, IndexError):
            print("Invalid input. Gate assignment aborted.")
            return

        # Assign the flight to the selected gate
        selected_gate.available = False
        print(f"Flight {flight.flight_id} assigned to Gate {selected_gate.gate_id}.")

        # Simulate the occupation of the gate for 5 seconds (could be longer in real-world systems)
        threading.Thread(target=self.free_gate, args=(selected_gate,)).start()

    def free_gate(self, gate):
        # Simulate gate being occupied for a certain period (e.g., for unloading passengers, refueling, etc.)
        print(f"Gate {gate.gate_id} is occupied.")
        time.sleep(5)  # Simulate the time for gate occupation (e.g., 5 seconds)
        gate.available = True
        print(f"Gate {gate.gate_id} is now available.")

    def schedule_flight(self):
        # Check if there are no flights to schedule
        if not self.queue:
            return "No flights in the queue."

        # Get the highest priority flight
        flight = heapq.heappop(self.queue)

        # Display all runways with their availability status
        print(f"\nFlight {flight.flight_id} ({'Emergency' if flight.emergency else 'Normal'} {flight.flight_type}) is ready to be scheduled.")

        print("Runways (with availability):")
        for i, runway in enumerate(self.runways):
            status = 'available' if runway.available else 'occupied'
            print(f"{i + 1}. Runway {runway.runway_id} is {status}")

        # Let the user choose an available runway
        try:
            choice = int(input("Select an available runway by number: ")) - 1
            if choice < 0 or choice >= len(self.runways):
                raise ValueError("Invalid runway selection.")
            selected_runway = self.runways[choice]
            if not selected_runway.available:
                print(f"Runway {selected_runway.runway_id} is occupied. Try again.")
                return
        except (ValueError, IndexError):
            print("Invalid input. Scheduling aborted.")
            return

        # Assign the flight to the selected runway
        selected_runway.available = False
        flight.status = "scheduled" if flight.flight_type == 'departure' else "landing"

        # Simulate scheduling/landing
        print(f"\nFlight {flight.flight_id} assigned to Runway {selected_runway.runway_id}.")
        time.sleep(2)  # Simulate time delay for the operation

        # Free the runway after the operation is complete
        selected_runway.available = True
        flight.status = 'landed' if flight.flight_type == 'arrival' else 'departed'
        print(f"Flight {flight.flight_id} has {flight.status}. Runway {selected_runway.runway_id} is now free.")

        # After landing, assign the flight to a gate
        if flight.flight_type == 'arrival':
            self.assign_gate(flight)

    def show_runway_status(self):
        # Print the status of all runways
        print("\nCurrent Runway Status:")
        for runway in self.runways:
            print(runway)

    def show_gate_status(self):
        # Print the status of all gates
        print("\nCurrent Gate Status:")
        for gate in self.gates:
            print(gate)

    def show_flight_queue(self):
        # Show flights currently waiting in the queue
        if not self.queue:
            print("No flights in the queue.")
        else:
            print("\nCurrent Flight Queue:")
            for flight in self.queue:
                print(f"Flight {flight.flight_id} - {flight.flight_type.upper()}, Priority: {flight.priority}, Emergency: {flight.emergency}")

# Function to load flights from CSV file
def load_flights_from_csv(filename):
    flights = []
    try:
        with open(filename, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                flight_id = row['flight_id']
                flight_type = row['flight_type'].lower()
                priority = int(row['priority'])
                emergency = True if row['emergency'].lower() == 'yes' else False
                flights.append(Flight(flight_id, flight_type, priority, emergency))
        print(f"Loaded {len(flights)} flights from {filename}.")
    except Exception as e:
        print(f"Error loading flights: {e}")
    return flights

# Main logic to simulate airport traffic control
def main():
    scheduler = Scheduler()

    # Add runways to the system
    scheduler.add_runway(Runway('A1'))
    scheduler.add_runway(Runway('B2'))
    scheduler.add_runway(Runway('C3'))

    # Add gates to the system
    scheduler.add_gate(Gate('G1'))
    scheduler.add_gate(Gate('G2'))
    scheduler.add_gate(Gate('G3'))

    # Load flights from CSV file
    filename = 'flights.csv'
    flights = load_flights_from_csv(filename)

    # Add loaded flights to the scheduler
    for flight in flights:
        scheduler.add_flight(flight)

    # Real-time interaction for scheduling and viewing status
    while True:
        print("\nRanchi Airport Traffic Control System")
        
        print("1. Schedule the next flight")
        print("2. View flight queue")
        print("3. View runway status")
        print("4. View gate status")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Schedule the next flight
            result = scheduler.schedule_flight()
            if result:
                print(result)

        elif choice == '2':
            # View flight queue
            scheduler.show_flight_queue()

        elif choice == '3':
            # View runway status
            scheduler.show_runway_status()

        elif choice == '4':
            # View gate status
            scheduler.show_gate_status()

        elif choice == '5':
            print("Exiting system.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
