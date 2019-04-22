import json
game = {}
with open('game-tree.json', 'r', encoding="utf-8") as f:
    game = json.load(f)
print(game)