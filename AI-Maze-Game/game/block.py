# THIS IS NOT A DECLARATION, THESE ARE THE IDS
EMPTY = 0
LIGHT_BLOCK = 1
MEDIUM_BLOCK = 2
HEAVY_BLOCK = 3
TRAP_BLOCK = 4
WALL_BLOCK = 5

# Declare blocks, will add more in future

BLOCK_LIST = [
    {
        "id": EMPTY,
        "name": "Empty",
        "color": (255, 255, 255) # white
    },
    {
        "id": LIGHT_BLOCK,
        "name": "Light Block",
        "color": (144, 238, 144) # light green
    },
    {
        "id": MEDIUM_BLOCK,
        "name": "Medium Block",
        "color": (255, 165, 0) # orange
    },
    {
        "id": HEAVY_BLOCK,
        "name": "Heavy Block",
        "color": (255, 0, 0) # red
    },
    {
        "id": TRAP_BLOCK,
        "name": "Trap Block",
        "color": (148, 0, 211) # purple
    },
    {
        "id": WALL_BLOCK,
        "name": "Wall",
        "color": (40, 40, 40) # dark gray
    },
]

# Create class for block objects to be placed
class Block:

    def __init__(self, block_id):
        # check if block_id is valid
        valid_ids = [0, 1, 2, 3, 4, 5]
        if block_id not in valid_ids:
            print("invalid block id:", block_id)
            return

        self.block_id = block_id

        # find the matching block info from the list
        self.info = None
        for block in BLOCK_LIST:
            if block["id"] == block_id:
                self.info = block

        self.name = self.info["name"]
        self.color = self.info["color"]

    def is_wall(self):
        # walls are totally impassable
        if self.block_id == WALL_BLOCK:
            return True
        return False

    def is_trap(self):
        return self.block_id == TRAP_BLOCK

    def __str__(self):
        # debugging
        return f"Block({self.name}, id={self.block_id}, color={self.color})"