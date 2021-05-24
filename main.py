from Controller.Controller import Controller
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("gui", type=int)
    parser.add_argument("username", type=str)
    parser.add_argument("password", type=str)
    parser.add_argument("multiplayer", type=int)
    parser.add_argument("secretkey", type=str)
    parser.add_argument("room_id", type=str)
    args = parser.parse_args()
    app = Controller(bool(args.gui), args.username, args.password, bool(args.multiplayer),
                     args.secretkey if args.secretkey != "" else None, args.room_id if args.room_id != "" else None)
