"""Core Gossip State Synchronizer implementation."""
import time
from typing import Dict, List, Tuple, Optional, Any


class StateEntry:
    def __init__(self, key: str, value: Any, version: int, origin_node: str, timestamp: float):
        self.key = key
        self.value = value
        self.version = version
        self.origin_node = origin_node
        self.timestamp = timestamp


class GossipNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.state: Dict[str, StateEntry] = {}
        self.vector_clock: Dict[str, int] = {node_id: 0}

    def set(self, key: str, value: Any):
        self.vector_clock[self.node_id] = self.vector_clock.get(self.node_id, 0) + 1
        ver = self.vector_clock[self.node_id]
        entry = StateEntry(key, value, ver, self.node_id, time.time())
        self.state[key] = entry

    def get(self, key: str) -> Optional[Any]:
        entry = self.state.get(key)
        return entry.value if entry else None

    def get_digest(self) -> Dict[str, Tuple[int, float]]:
        # Returns key -> (version, timestamp)
        return {k: (e.version, e.timestamp) for k, e in self.state.items()}

    def compute_deltas(self, remote_digest: Dict[str, Tuple[int, float]]) -> List[StateEntry]:
        deltas = []
        for key, entry in self.state.items():
            if key not in remote_digest:
                deltas.append(entry)
            else:
                rem_ver, rem_ts = remote_digest[key]
                if entry.version > rem_ver or (entry.version == rem_ver and entry.timestamp > rem_ts):
                    deltas.append(entry)
        return deltas

    def merge_deltas(self, deltas: List[StateEntry]):
        for delta in deltas:
            curr = self.state.get(delta.key)
            if not curr:
                self.state[delta.key] = delta
            else:
                if delta.version > curr.version or (delta.version == curr.version and delta.timestamp > curr.timestamp):
                    self.state[delta.key] = delta

    def sync_with_peer(self, peer: 'GossipNode'):
        digest_self = self.get_digest()
        digest_peer = peer.get_digest()

        deltas_for_peer = self.compute_deltas(digest_peer)
        deltas_for_self = peer.compute_deltas(digest_self)

        peer.merge_deltas(deltas_for_peer)
        self.merge_deltas(deltas_for_self)
