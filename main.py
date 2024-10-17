def parse_input(input):

    """
        Line 1: Number of slice users n(1 < n <= 10000), PortBW(Gbps)
        Line 2: number of first slice packets m1 slice bandwidth SliceBW and maximumslice delay
        tolerance UBD
        Line 3: sequence information about the first slice
        ts1, PktSize1, ts1, PktSize2, PktSize 
    """
    lines = input.split('\n')
    n, port_bw = map(int, lines[0].split())
    if ((2 * (n + 1)) != len(lines)):
        raise ValueError(f"Expected 2 * n + 1 lines = {2*n+1}, but got {len(lines)}")
    
    slices = []

    for i in range(1, 2 * n + 1, 2):
        # handle the line  , for example :            3 1 30000
        # Line 2: number of first slice packets m1 slice bandwidth SliceBW and maximumslice delay tolerance UBD
        num_packets, slice_bw, max_delay = map(int, lines[i].split())
        #bw, delay = map(int, lines[i].split()) 
        # handle the line  , for example :            0 8000 1000 16000 3000 800
        # Line 3: sequence information about the first slice ts11, PktSize11, ts12, PktSize12,...ts1m1, PktSize1m1
        #ts11, pktsize11, ts12, pktsize12, ts13, pktsize13 = map(int, lines[i + 1].split())
        sequence_information_about_the_slice = list(map(int, lines[i + 1].split())) 

        slices.append({'num_packets': num_packets, 'slice_bw': slice_bw, 'max_delay': max_delay, 'sequence_info': sequence_information_about_the_slice})
    
    # Return for example 2 ,2  , slices for input 2 2 slices
    return n, port_bw, slices

def schedule_slices(n, port_bw, slices):
    # n: number of slices
    # port_bw: bandwidth in Gbps
    # slices: a list of dictionaries, each representing a slice with its packets, bandwidth, and delay tolerance
    scheduled_packets = []
    current_time = 0
    slice_packet_indices = [0] * n  # Tracks the current packet to schedule for each slice
    
    return scheduled_packets

# Example input
n = 2
port_bw = 2  # Gbps

input = """2 2
3 1 30000
0 8000 1000 16000 3000 8000
3 1 30000
0 8000 1000 16000 3000 8000
"""
n, port_bw, slices = parse_input(input)
print(f"n: {n}, port_bw: {port_bw}, slices: {slices}")
#output = schedule_slices()

#print(output)