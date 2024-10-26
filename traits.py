import json


assessment = json.load(open("ipip50.json", "r"))


def max_min_for_types(assessment: list) -> list:
    types_max_min = [{"max": 0, "min": 0} for i in range(5)]
    for task in assessment:
        if task["math"] == "+":
            types_max_min[task["type"]]["max"] += 5
            types_max_min[task["type"]]["min"] += 1
        else:
            types_max_min[task["type"]]["max"] -= 1
            types_max_min[task["type"]]["min"] -= 5


def main():
    assessment = json.load(open("ipip50.json", "r"))
    types_max_min = max_min_for_types(assessment)


if __name__ == "__main__":
    main()
