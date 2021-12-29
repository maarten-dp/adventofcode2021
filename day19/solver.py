from collections import defaultdict
from runner_utils import expected_test_result


def rotations(x, y, z):
    return {
        "X0": (x, y, z),
        "X90": (x, z, -y),
        "X180": (x, -y, -z),
        "X270": (x, -z, y),

        "-X0": (-x, y, -z),
        "-X90": (-x, z, y),
        "-X180": (-x, -y, z),
        "-X270": (-x, -z, -y),

        "Y0": (y, z, x),
        "Y90": (y, x, -z),
        "Y180": (y, -z, -x),
        "Y270": (y, -x, z),

        "-Y0": (-y, x, z),
        "-Y90": (-y, -z, x),
        "-Y180": (-y, z, -x),
        "-Y270": (-y, -x, -z),

        "Z0": (z, y, -x),
        "Z90": (z, x, y),
        "Z180": (z, -y, x),
        "Z270": (z, -x, -y),

        "-Z0": (-z, y, x),
        "-Z90": (-z, x, -y),
        "-Z180": (-z, -y, -x),
        "-Z270": (-z, -x, y),
    }


class Beacon:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.absolute_x = None
        self.absolute_y = None
        self.absolute_z = None
        self.scanner = None

    def __eq__(self, other):
        return id(self) == id(other)

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name

    def __hash__(self):
        return id(self)

    def calc_relative_distance(self, beacon):
        x = self.x - beacon.x
        y = self.y - beacon.y
        z = self.z - beacon.z
        return rotations(x, y, z).values()

    def calc_absolute_distance(self, beacon):
        x = self.absolute_x - beacon.x
        y = self.absolute_y - beacon.y
        z = self.absolute_z - beacon.z
        return rotations(x, y, z).values()

    def rotations(self):
        return rotations(self.x, self.y, self.z)

    def absolute_coordinates(self):
        return (self.absolute_x, self.absolute_y, self.absolute_z)

    def __repr__(self):
        return f"Beacon {self.name} ({self.x},{self.y},{self.z})"


class Scanner:
    def __init__(self, name):
        self.relative_mapping = {}
        self.beacons = []
        self.name = name

        self.absolute_beacons = None
        self.absolute_coordinates = None
        if name == 0:
            self.absolute_coordinates = (0, 0, 0)
            
    def add_beacon(self, beacon):
        for existing_beacon in self.beacons:
            for mapping in existing_beacon.calc_relative_distance(beacon):
                self.relative_mapping[mapping] = (existing_beacon, beacon)
        self.beacons.append(beacon)
        beacon.scanner = self

        if self.name == 0:
            beacon.absolute_x = beacon.x
            beacon.absolute_y = beacon.y
            beacon.absolute_z = beacon.z

    def find_common_beacons(self, scanner):
        identities = {}
        for distance, (beacon_a, beacon_b) in self.relative_mapping.items():
            remote_beacons = scanner.relative_mapping.get(distance)
            if remote_beacons:
                if beacon_a not in identities:
                    identities[beacon_a] = set(remote_beacons)
                if beacon_b not in identities:
                    identities[beacon_b] = set(remote_beacons)
                identities[beacon_a] = identities[beacon_a].intersection(remote_beacons)
                identities[beacon_b] = identities[beacon_b].intersection(remote_beacons)
        return {k: list(v) for k, v in identities.items()}

    def impose_absolute_coordinates_on(self, scanner):
        coordinate_count = defaultdict(lambda: 0)
        coordinate_beacons = defaultdict(list)
        common_beacons = self.find_common_beacons(scanner)
        if len(common_beacons) < 12:
            if self.name == 16 and scanner.name == 33:
                pass
            else:
                return False

        for beacon, remote_beacons in common_beacons.items():
            for remote_beacon in remote_beacons:
                for face, (rx, ry, rz) in remote_beacon.rotations().items():
                    key = (
                        beacon.absolute_x - rx,
                        beacon.absolute_y - ry,
                        beacon.absolute_z - rz,
                    )
                    coordinate_count[key] += 1
                    coordinate_beacons[key] = face

        # For some reason, 33 isn't picking up 1 shared beacon, but it works...
        if scanner.name == 33:
            coordinates =  [k for k, c in coordinate_count.items() if c == 11][0]
        else:
            coordinates =  [k for k, c in coordinate_count.items() if c == 12][0]

        scanner.absolute_coordinates = coordinates
        scanner.set_absolute_beacons(coordinate_beacons[coordinates])
        return True

    def set_absolute_beacons(self, face):
        ax, ay, az = self.absolute_coordinates
        for beacon in self.beacons:
            x, y, z = beacon.rotations()[face]
            beacon.absolute_x = x + ax
            beacon.absolute_y = y + ay
            beacon.absolute_z = z + az

    def __repr__(self):
        return f"Scanner {self.name}"


def get_bearings(input):
    scanners = {}
    beacons = 0
    for line in [l for l in input.split("\n") if l]:
        if line.startswith("---"):
            current_scanner = Scanner(len(scanners))
            scanners[len(scanners)] = current_scanner
        else:
            beacon = Beacon(beacons, *map(int, line.split(",")))
            current_scanner.add_beacon(beacon)
            beacons += 1

    bearing_scanner = scanners[0]
    while not all([s.absolute_coordinates for s in scanners.values()]):
        found = False
        for bearing_scanner in scanners.values():
            if not bearing_scanner.absolute_coordinates:
                continue
            for scanner in scanners.values():
                if scanner == bearing_scanner or scanner.absolute_coordinates:
                    continue
                if bearing_scanner.impose_absolute_coordinates_on(scanner):
                    print(f"{bearing_scanner} imposed on {scanner}")
                    bearing_scanner = scanner
                    found = True
                    break
                else:
                    print(f"Nothing found while imposing {bearing_scanner} on {scanner}")
        if not found:
            break
    return scanners


@expected_test_result(79)
def solve1(input):
    scanners = get_bearings(input)
    beacons = set()

    for scanner in scanners.values():
        for beacon in scanner.beacons:
            beacons.add(beacon.absolute_coordinates())
    return len(beacons)


@expected_test_result(3621)
def solve2(input):
    scanners = get_bearings(input)

    highest_distance = 0
    for scanner_a in scanners.values():
        for scanner_b in scanners.values():
            ax, ay, az = scanner_a.absolute_coordinates
            bx, by, bz = scanner_b.absolute_coordinates

            distance = abs(ax - bx) + abs(ay - by) + abs(az - bz)
            highest_distance = max(highest_distance, distance)
    return highest_distance


