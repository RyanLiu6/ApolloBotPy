import copy
import json
import random
import logging
import datetime


# class Santa:
#     def __init__(self, name, recipient):
#         self.name = name
#         self.recipient = recipient

#     def __eq__(self, other):
#         return self.name == other.name and self.recipient == other.recipient


# class SecretSantas:
#     def __init__(self):
#         self.santas = {}

#     def add_santa(self, santa):
#         self.santas[santa.name] = santa

#     def get_santa(self, name):
#         return self.santas[name]

#     def get_names(self):
#         return self.santas.keys()

#     def __str__(self):
#         to_return = ""
#         for k, v in self.santas.items():
#             to_return += f"Name: {k} | Recipient: {v.recipient}\n"

#         return to_return

class Santa:
    def __init__(self):
        self.santas = {}

    def add_santa(self, gift_giver, gift_receiver):
        self.santas[gift_giver] = gift_receiver

    def get_receiver(self, gift_giver):
        return self.santas[gift_giver]

    def get_givers(self):
        return self.santas.keys()

    def get_receivers(self):
        return self.santas.values()

    def __str__(self):
        to_return = ""
        for k, v in self.santas.items():
            to_return += f"Name: {k} | Recipient: {v.recipient}\n"

        return to_return


class SecretSanta:
    def get_secret_santa_by_year(year):
        with open("previous_years.json") as read_file:
            data = json.load(read_file)

        year_data = data[str(year)]
        santas = SecretSantas()

        for k, v in enumerate(year_data):
            if k < len(year_data) - 1:
                index = k + 1
            else:
                index = 0

            santas.add_santa(Santa(
                name=v,
                recipient=year_data[index]))

        return santas


def make_secret_santas():
    # Load previous year's secret santa
    current_year = datetime.datetime.now().year

    with open("previous_years.json") as read_file:
        data = json.load(read_file)

    previous_data = data[str(current_year - 1)]

    previous_santas = assemble_santas(previous_data)
    current_data = copy.deepcopy(previous_data)
    random.shuffle(current_data)
    current_santas = assemble_santas(current_data)

    while not validate_santas(previous_santas, current_santas):
        random.shuffle(current_data)
        current_santas = assemble_santas(current_data)

    # Store it in the json file
    current_year_json = []
    for k, v in current_santas.santas.items():
        current_year_json.append(v.name)

    data[str(current_year)] = current_year_json

    with open("previous_years.json", "w") as write_file:
        json.dump(data, write_file, indent=4)

    return current_santas

def validate_santas(previous, current):
    logging.getLogger("Discord").debug(f"Previous: \n{previous}")
    logging.getLogger("Discord").debug(f"Current: \n{current}")

    for name in current.get_names():
        if current.get_santa(name) == previous.get_santa(name):
            return False

    return True

def assemble_santas(input_list):
    santas = SecretSantas()

    for key, name in enumerate(input_list):
        if key < len(input_list) - 1:
            index = key + 1
        else:
            index = 0

        santas.add_santa(Santa(
            name=name,
            recipient=input_list[index]))

    return santas

