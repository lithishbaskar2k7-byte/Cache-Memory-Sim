class CacheLine:
    def __init__(self):
        self.valid = False
        self.tag = None
        self.block = None
        self.data = None
        self.last_used = 0
        self.inserted_at = 0


class Cache:
    def __init__(
        self,
        memory_size,
        cache_size,
        block_size,
        mapping="Direct Mapping",
        replacement="LRU",
        associativity=2
    ):

        self.memory_size = memory_size
        self.cache_size = cache_size
        self.block_size = block_size
        self.mapping = mapping
        self.replacement = replacement
        self.associativity = associativity

        if memory_size <= 0:
            raise ValueError("Memory size must be greater than 0.")

        if cache_size <= 0:
            raise ValueError("Cache size must be greater than 0.")

        if block_size <= 0:
            raise ValueError("Block size must be greater than 0.")

        if cache_size % block_size != 0:
            raise ValueError(
                "Cache size must be divisible by block size."
            )

        if memory_size % block_size != 0:
            raise ValueError(
                "Memory size must be divisible by block size."
            )

        self.num_lines = cache_size // block_size
        self.num_memory_blocks = memory_size // block_size

        if mapping == "Set Associative":

            if associativity < 1:
                raise ValueError(
                    "Associativity must be at least 1."
                )

            if self.num_lines % associativity != 0:
                raise ValueError(
                    "Cache lines must be divisible by associativity."
                )

            self.num_sets = self.num_lines // associativity

        else:
            self.num_sets = self.num_lines

        self.lines = [
            CacheLine()
            for _ in range(self.num_lines)
        ]

        self.access_counter = 0

        self.hits = 0
        self.misses = 0

        # Main memory
        self.memory = list(range(memory_size))

    # ================================================
    # RESET CACHE
    # ================================================

    def reset(self):

        self.lines = [
            CacheLine()
            for _ in range(self.num_lines)
        ]

        self.access_counter = 0

        self.hits = 0
        self.misses = 0

    # ================================================
    # ADDRESS INFORMATION
    # ================================================

    def get_address_info(self, address):

        if address < 0 or address >= self.memory_size:

            raise ValueError(
                f"Address must be between 0 and "
                f"{self.memory_size - 1}."
            )

        block_address = address // self.block_size

        offset = address % self.block_size

        if self.mapping == "Direct Mapping":

            index = block_address % self.num_lines

            tag = block_address // self.num_lines

        elif self.mapping == "Set Associative":

            index = block_address % self.num_sets

            tag = block_address // self.num_sets

        else:

            index = None

            tag = block_address

        return {
            "address": address,
            "block": block_address,
            "offset": offset,
            "index": index,
            "tag": tag
        }

    # ================================================
    # FIND TARGET CACHE LINES
    # ================================================

    def get_target_lines(self, block_address):

        if self.mapping == "Direct Mapping":

            index = block_address % self.num_lines

            return [index]

        elif self.mapping == "Set Associative":

            set_index = block_address % self.num_sets

            start = set_index * self.associativity

            end = start + self.associativity

            return list(range(start, end))

        else:

            return list(range(self.num_lines))

    # ================================================
    # FIND CACHE HIT
    # ================================================

    def find_line(self, block_address):

        target_lines = self.get_target_lines(
            block_address
        )

        for line_index in target_lines:

            line = self.lines[line_index]

            if (
                line.valid
                and line.block == block_address
            ):

                return line_index

        return None

    # ================================================
    # REPLACEMENT POLICY
    # ================================================

    def choose_replacement_line(
        self,
        block_address
    ):

        target_lines = self.get_target_lines(
            block_address
        )

        # Empty cache line first
        for line_index in target_lines:

            if not self.lines[line_index].valid:

                return line_index

        # LRU
        if self.replacement == "LRU":

            return min(
                target_lines,
                key=lambda i:
                self.lines[i].last_used
            )

        # FIFO
        elif self.replacement == "FIFO":

            return min(
                target_lines,
                key=lambda i:
                self.lines[i].inserted_at
            )

        # Random
        else:

            import random

            return random.choice(
                target_lines
            )

    # ================================================
    # ACCESS MEMORY
    # ================================================

    def access(self, address):

        self.access_counter += 1

        info = self.get_address_info(
            address
        )

        block_address = info["block"]

        # Search cache
        line_index = self.find_line(
            block_address
        )

        # ============================================
        # CACHE HIT
        # ============================================

        if line_index is not None:

            self.hits += 1

            line = self.lines[line_index]

            line.last_used = self.access_counter

            return {
                **info,
                "result": "HIT",
                "line": line_index,
                "data": self.memory[address],
                "replaced": False
            }

        # ============================================
        # CACHE MISS
        # ============================================

        self.misses += 1

        line_index = self.choose_replacement_line(
            block_address
        )

        line = self.lines[line_index]

        was_valid = line.valid

        old_block = line.block

        # Load block into cache
        line.valid = True

        line.block = block_address

        line.tag = info["tag"]

        line.data = self.memory[address]

        line.last_used = self.access_counter

        line.inserted_at = self.access_counter

        return {
            **info,
            "result": "MISS",
            "line": line_index,
            "data": self.memory[address],
            "replaced": was_valid,
            "old_block": old_block
        }

    # ================================================
    # HIT RATE
    # ================================================

    def get_hit_rate(self):

        total = self.hits + self.misses

        if total == 0:
            return 0

        return (
            self.hits / total
        ) * 100

    # ================================================
    # MISS RATE
    # ================================================

    def get_miss_rate(self):

        total = self.hits + self.misses

        if total == 0:
            return 0

        return (
            self.misses / total
        ) * 100