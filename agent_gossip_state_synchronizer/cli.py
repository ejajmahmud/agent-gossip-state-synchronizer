"""CLI for agent-gossip-state-synchronizer."""
import sys
import argparse
from .gossip import GossipNode


def main():
    parser = argparse.ArgumentParser(description="Agent Gossip State Synchronizer CLI")
    parser.add_argument("--demo", action="store_true", help="Run gossip sync demo between 3 nodes")
    args = parser.parse_args()

    if args.demo:
        n1 = GossipNode("node_1")
        n2 = GossipNode("node_2")
        n3 = GossipNode("node_3")

        n1.set("model_temperature", 0.7)
        n2.set("active_tool", "bash")
        n3.set("max_tokens", 8192)

        print("Initial States:")
        print("  Node 1:", [k for k in n1.state.keys()])
        print("  Node 2:", [k for k in n2.state.keys()])
        print("  Node 3:", [k for k in n3.state.keys()])

        # Gossip round: 1 syncs with 2, 2 syncs with 3, 1 syncs with 3
        n1.sync_with_peer(n2)
        n2.sync_with_peer(n3)
        n1.sync_with_peer(n3)

        print("
Post-Gossip Converged States:")
        print("  Node 1 keys:", sorted(list(n1.state.keys())))
        print("  Node 2 keys:", sorted(list(n2.state.keys())))
        print("  Node 3 keys:", sorted(list(n3.state.keys())))
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
