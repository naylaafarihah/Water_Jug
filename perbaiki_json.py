import json

operators = [
    "fill_a",
    "fill_b",
    "empty_a",
    "empty_b",
    "pour_a_b",
    "pour_b_a"
]

cases = {
    "ukuran_5_2.json": {
        "cap_a": 5, "cap_b": 2, "target": 1
    },
    "ukuran_4_3.json": {
        "cap_a": 4, "cap_b": 3, "target": 1
    },
    "ukuran_6_4.json": {
        "cap_a": 6, "cap_b": 4, "target": 1
    }
}

for filename, config in cases.items():
    config["start"] = [0, 0]
    config["operators"] = operators

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)

    print(f"Berhasil membuat: {filename}")
