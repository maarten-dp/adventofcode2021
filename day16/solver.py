from runner_utils import expected_test_result


def chain_multiply(p):
    value = p.sub_packets[0].resolve()
    for packet in p.sub_packets[1:]:
        value *= packet.resolve()
    return value


LITERAL_TYPE = 4
RESOLVERS = {
    0: lambda p: sum([sp.resolve() for sp in p.sub_packets]),
    1: chain_multiply,
    2: lambda p: min([sp.resolve() for sp in p.sub_packets]),
    3: lambda p: max([sp.resolve() for sp in p.sub_packets]),
    4: lambda p: p.data,
    5: lambda p: int(p.sub_packets[0].resolve() > p.sub_packets[1].resolve()),
    6: lambda p: int(p.sub_packets[0].resolve() < p.sub_packets[1].resolve()),
    7: lambda p: int(p.sub_packets[0].resolve() == p.sub_packets[1].resolve()),
}


def to_bit_stream(input):
    stream = ""
    for char in input:
        byte = f"{int(char, 16):b}".zfill(4)
        stream = f"{stream}{byte}"
    return stream


class BitStream:
    def __init__(self, stream):
        self.stream = stream
        self.index = 0

    def __bool__(self):
        has_data = self.index != len(self.stream)
        if has_data:
            return bool(int(self.stream[self.index:], 2))
        return has_data

    def consume(self, size):
        self.index += size
        return self.stream[self.index - size: self.index]


class Packet:
    def __init__(self, version, packet_type, data, sub_packets):
        self.version = version
        self.packet_type = packet_type
        self.data = data
        self.sub_packets = sub_packets

    def resolve(self):
        return RESOLVERS[self.packet_type](self)


class Decoder:
    def __init__(self, stream):
        self.stream = BitStream(stream)

    def decode(self):
        version = int(self.stream.consume(3), 2)
        packet_type = int(self.stream.consume(3), 2)
        data = None
        sub_packets = None

        if packet_type == LITERAL_TYPE:
            data = self.decode_literal_packet()
        else:
            length_type = self.stream.consume(1)
            if length_type == "1":
                sub_packets = self.decode_expected_amount_packet()
            else:
                sub_packets = self.decode_fixed_length_packet()

        return Packet(version, packet_type, data, sub_packets)

    def decode_literal_packet(self):
        is_end_packet = False
        values = []
        while not is_end_packet:
            is_end_packet = self.stream.consume(1) == "0"
            value = int(self.stream.consume(4), 2)
            values.append(value)
        return int("".join([f"{v:b}".zfill(4) for v in values]), 2)

    def decode_fixed_length_packet(self):
        packet_length = int(self.stream.consume(15), 2)
        sub_decoder = Decoder(self.stream.consume(packet_length))
        packets = []
        while sub_decoder.stream:
            packets.append(sub_decoder.decode())
        return packets

    def decode_expected_amount_packet(self):
        expected_packets = int(self.stream.consume(11), 2)
        packets = []
        for _ in range(expected_packets):
            sub_packet = self.decode()
            packets.append(sub_packet)
        return packets


@expected_test_result(12)
def solve1(input):
    def get_version_sum(packet):
        version_number =  packet.version
        if packet.sub_packets:
            for sub_packet in packet.sub_packets:
                version_number += get_version_sum(sub_packet)
        return version_number

    stream = to_bit_stream(input.replace("\n", ""))
    packet = Decoder(stream).decode()
    return get_version_sum(packet)


@expected_test_result(46)
def solve2(input):
    stream = to_bit_stream(input.replace("\n", ""))
    packet = Decoder(stream).decode()
    return packet.resolve()
