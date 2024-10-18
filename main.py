from dataclasses import dataclass, field
from typing import List, Optional
import sys

@dataclass
class Packet:
    arrival_time: int
    size: int
    slice_id: int
    packet_id: int
    scheduled_time: Optional[int] = None
    departure_time: Optional[int] = None

@dataclass
class Slice:
    num_packets: int
    bandwidth: int
    max_delay: int
    packets: List[Packet] = field(default_factory=list)

@dataclass
class NetworkConfiguration:
    num_slices: int
    port_bandwidth: int
    slices: List[Slice]


def round_robin_scheduler(network_config: NetworkConfiguration) -> List[Packet]:
    scheduled_packets = []
    current_time = 0
    slice_queues = [slice.packets.copy() for slice in network_config.slices]
    
    while any(slice_queues):
        for slice_id, queue in enumerate(slice_queues):
            if queue:
                packet = queue.pop(0)
                if packet.arrival_time <= current_time:
                    # Calculate minimum transmission time based on port bandwidth
                    min_transmission_time = (packet.size * 1e9) / (network_config.port_bandwidth * 1e9)  # Convert to ns
                    
                    # Ensure current_time is an integer
                    current_time = max(int(current_time), packet.arrival_time)
                    
                    # Set scheduled_time and calculate departure_time
                    packet.scheduled_time = current_time
                    packet.departure_time = current_time + int(min_transmission_time)
                    
                    # Update current_time for next packet
                    current_time = packet.departure_time
                    
                    scheduled_packets.append(packet)
                else:
                    queue.insert(0, packet)
                    current_time = max(current_time, packet.arrival_time)
    
    return scheduled_packets
def print_output(scheduled_packets: List[Packet]):
    print(len(scheduled_packets))
    output = " ".join([f"{int(packet.departure_time)} {packet.slice_id} {packet.packet_id}" for packet in scheduled_packets])
    print(output)
def parse_input()->NetworkConfiguration:

    """
    Parse the input string into structured data.

    Args:
    input_str (str): The input string to parse.

    Returns:
    tuple: (num_slices, port_bandwidth, slices)
        num_slices (int): Number of slice users
        port_bandwidth (int): Port Bandwidth in Gbps
        slices (list): List of dictionaries, each representing a slice
    """
    lines = [line.strip() for line in sys.stdin if line.strip()]
    
    num_slices, port_bandwidth = map(float, lines[0].split())
    num_slices = int(num_slices)
    
    slices = []
    i = 1
    while i < len(lines):
        slice_info = list(map(float, lines[i].split()))
        num_packets, slice_bandwidth, max_delay = slice_info
        num_packets = int(num_packets)
        
        i += 1
        packet_info = list(map(float, lines[i].split()))
        
        packets = [
            Packet(arrival_time=int(packet_info[j]), size=int(packet_info[j+1]), slice_id=len(slices), packet_id=j//2)
            for j in range(0, len(packet_info), 2)
        ]
        slices.append(Slice(num_packets=num_packets, bandwidth=slice_bandwidth, max_delay=int(max_delay), packets=packets))
        i += 1
    
    return NetworkConfiguration(num_slices=num_slices, port_bandwidth=port_bandwidth, slices=slices)
input_str = """2 2
3 1 30000
0 8000 1000 16000 3000 8000
3 1 30000
0 8000 1000 16000 3000 8000"""


def main():
    try:
        network_config = parse_input()
        scheduled_packets = round_robin_scheduler(network_config)
        print_output(scheduled_packets)
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
