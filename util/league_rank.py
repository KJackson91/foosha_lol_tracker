from dataclasses import dataclass


@dataclass(eq=True)
class LoLRank:
    tier: str
    rank: str
    lp: int

    def to_dict(self):
        return {
            'tier': self.tier,
            'rank': self.rank,
            'lp': self.lp
        }

    def to_str(self):
        return f"{self.tier} {self.rank} {self.lp}LP"
