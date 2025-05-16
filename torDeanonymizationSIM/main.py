from datetime import datetime
from nodes.client import ClientNode
from nodes.relay import RelayNode
from nodes.exit import ExitNode

def format_time(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def write_log(times):
    with open("route_log.txt", "a") as f:
       f.write("Route timing:\n")
       f.write(f"Client sent at:       {format_time(times[0])}\n")
       f.write(f"Relay 1 processed at: {format_time(times[1])}\n")
       f.write(f"Relay 2 processed at: {format_time(times[2])}\n")
       f.write(f"Exit received at:     {format_time(times[3])}\n\n") 

def main():
    client = ClientNode()
    relay1 = RelayNode("Relay 1")
    relay2 = RelayNode("Relay 2")
    exit_node = ExitNode()

    message = "Hello from client"
    print("\nStarting transmission...\n")

    message, t1 = client.process_packet(message)
    message, t2 = relay1.process_packet(message)
    message, t3 = relay2.process_packet(message)
    message, t4 = exit_node.process_packet(message)

    print(f"\nRoute timing:")
    print(f"Client sent at:       {format_time(t1)}")
    print(f"Relay 1 processed at: {format_time(t2)}")
    print(f"Relay 2 processed at: {format_time(t3)}")
    print(f"Exit received at:     {format_time(t4)}")

    write_log([t1, t2, t3, t4])

if __name__ == "__main__":
    main()
