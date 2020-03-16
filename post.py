#!/usr/bin/env python3

import htb
from TwitterAPI import TwitterAPI
import sys


def post(machine, twitterAPI):
    message = f"""I just owned {machine['name']}! It was made by\
            {machine['maker']['name']} and was rated {machine['rating']}."""
    if len(message) > 140:
        print("ERROR: too long")
        exit(1)
    r = twitterAPI.request("statuses/update", {'status': message})
    if r.status_code != 200:
        print("Failure while tweeting")


def main(key, machine_name, twitter_token):
    h = htb.HTB(key)
    machines = h.get_machines()
    machine_info = list(filter(lambda d: d['name'] == machine_name, machines))
    if not machine_info:
        print("There is no machine with this name.")
        exit(1)

    machine = machine_info[0]

    lines = None
    with open(twitter_token, "r") as f:
        lines = f.readlines()
    tokens = list(map(lambda x: x.rstrip(), lines[:4]))
    tAPI = TwitterAPI(*tokens)

    post(machine, tAPI)
    # print(f"{machine['name']} info:")
    # for k, v in machine.items():
    #     if k != "avatar_thumb":
    #         print(f"\t{k} : {v}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} API_key machine_name twitter_token")
        exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
