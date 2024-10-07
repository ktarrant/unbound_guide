import os
import json
from unbound_guide.utils import json_dir, routes_dir, source_dir
from unbound_guide.utils import get_pokedex_entry


key_to_name = lambda key: key.replace("_", " ").title()
clean_ability = lambda ability: key_to_name(ability.replace("ABILITY_", ""))
clean_item = lambda item: key_to_name(item.replace("ITEM_", ""))
clean_type = lambda type: key_to_name(type.replace("TYPE_", ""))
clean_gender = lambda gender: f"{int(gender)}%" if isinstance(gender, float) else "N/A"


def summarize_entry(entry):
    evs = []
    for stat in ["HP", "Attack", "Defense", "SpAttack", "SpDefense", "Speed"]:
        value = entry[f"evYield_{stat}"]
        if value > 0:
            evs.append(f"{value} {stat[:3]}")
    summary = {
        "Name": entry["name"],
        "Type 1": "" if "NONE" in entry["type1"] else clean_type(entry['type1']),
        "Type 2": "" if "NONE" in entry["type2"] else clean_type(entry['type2']),
        "Catch Rate": entry["catchRate"],
        "Exp": entry["expYield"],
        "Ev 1": evs[0],
        "Ev 2": "" if len(evs) == 1 else evs[1],
        "Item 1": "" if entry["item1"] == "ITEM_NONE" else clean_item(entry["item1"]),
        "Item 2": "" if entry["item2"] == "ITEM_NONE" else clean_item(entry["item2"]),
        "Gender Ratio": clean_gender(entry["genderRatio"]),
        "Growth Rate": key_to_name(entry["growthRate"][7:]),
        "Ability 1": clean_ability(entry["ability1"]),
        "Ability 2": "" if "NONE" in entry["ability2"] else clean_ability(entry["ability2"]),
        "Hidden Ability": "" if "NONE" in entry["hiddenAbility"] else clean_ability(entry["hiddenAbility"]),
    }
    return summary


def summarize_location_data(location_data_entry):
    location_summary = {}
    for method, method_entry in location_data_entry.items():
        clean_method = key_to_name(method)
        location_summary[clean_method] = {}
        for area, area_entry in method_entry.items():
            location_summary[clean_method][area] = []
            for i in range(len(area_entry)):
                species = area_entry[i]
                try:
                    pokedex_entry = get_pokedex_entry(species)
                except FileNotFoundError:
                    print(f"Species in location data not found in pokedex: {species}")
                    continue

                try:
                    location_summary[clean_method][area].append(summarize_entry(pokedex_entry))
                except KeyError:
                    print(f"Species data imcomplete: {species}")
    return location_summary


def write_row(values, file):
    first = True
    for value in values:
        if first:
            prefix = "   * - "
            first = False
        else:
            prefix = "     - "
        file.write(prefix + str(value) + "\n")


if __name__ == "__main__":
    routes_file = os.path.join(json_dir, "locations.json")
    with open(routes_file, "r") as json_file:
        routes_data = json.load(json_file)

    route_toctree_list = ""
    for route in routes_data:
        summary = summarize_location_data(routes_data[route])
        route_file_name = route.replace(" ", "_")
        rst_path = os.path.join(routes_dir, f"{route_file_name}.rst")
        with open(rst_path, "w") as f:
            f.write(route + "\n")
            f.write("=" * len(route) + "\n\n")
            for method in summary:
                for area in summary[method]:
                    table = summary[method][area]

                    if not table:
                        continue

                    if area:
                        f.write(f".. list-table:: {route} - {area} - {method}\n")
                    else:
                        f.write(f".. list-table:: {route} - {method}\n")

                    headers = list(table[0].keys())
                    width = int(100 / len(headers))
                    width_list = ", ".join([str(width)] * len(headers))

                    f.write(f"   :widths: " + width_list + "\n")
                    f.write(f"   :header-rows: 1\n\n")

                    write_row(headers, f)
                    for row in table:
                        write_row(row.values(), f)
                    f.write("\n")

        route_toctree_list += "routes/" + route_file_name + "\n"
    print(route_toctree_list)
