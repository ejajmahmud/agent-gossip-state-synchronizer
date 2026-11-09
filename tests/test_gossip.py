"""Unit tests for agent-gossip-state-synchronizer."""
import unittest
from agent_gossip_state_synchronizer.gossip import GossipNode


class TestGossipNode(unittest.TestCase):
    def setUp(self):
        self.node_a = GossipNode("A")
        self.node_b = GossipNode("B")

    def test_gossip_convergence(self):
        self.node_a.set("config_k", "val_a")
        self.node_b.set("config_j", "val_b")

        self.node_a.sync_with_peer(self.node_b)

        self.assertEqual(self.node_a.get("config_j"), "val_b")
        self.assertEqual(self.node_b.get("config_k"), "val_a")

    def test_newer_version_wins(self):
        self.node_a.set("key_1", "initial")
        self.node_b.sync_with_peer(self.node_a)

        # Update on A
        self.node_a.set("key_1", "updated")
        self.node_b.sync_with_peer(self.node_a)
        self.assertEqual(self.node_b.get("key_1"), "updated")
