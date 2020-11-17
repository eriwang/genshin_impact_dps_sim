from collections import namedtuple
import random

_AUTO_ATTACK_DMG_PERCENTS = [0.441, 0.468, 0.581, 0.577, 0.721]
_AUTO_ATTACK_TIME = 2.6 / 5


CharStats = namedtuple('CharStats', ['base_atk', 'percent_atk', 'crit_rate', 'crit_dmg'])
WeaponStats = namedtuple('WeaponStats', ['base_atk', 'percent_atk', 'crit_rate'])
ArtifactStats = namedtuple('ArtifactStats', ['flat_atk', 'percent_atk', 'crit_rate', 'crit_dmg'])


class Fischl:
    def __init__(self, weapon_stats, artifact_stats):
        self._char_stats = CharStats(216, 0.18, 0.05, 0.5)  # Fischl 80/80
        self._weap_stats = weapon_stats
        self._arti_stats = artifact_stats

        self._next_auto_index = 0
        # self._skill_ready_ts = 0
        # self._burst_ready_ts = 0

    def run_iteration(self, controller, current_time):  # pylint: disable=unused-argument
        auto_attack_damage = _calculate_damage(self._char_stats, self._weap_stats, self._arti_stats,
                                               _AUTO_ATTACK_DMG_PERCENTS[self._next_auto_index])

        controller.perform_active_action(self, auto_attack_damage, _AUTO_ATTACK_TIME)
        self._next_auto_index = (self._next_auto_index + 1) % len(_AUTO_ATTACK_DMG_PERCENTS)


def _calculate_damage(char_stats, weap_stats, artifact_stats, skill_dmg_percent):
    atk_percent_bonus = char_stats.percent_atk + weap_stats.percent_atk + artifact_stats.percent_atk
    final_attack_stat = (char_stats.base_atk + weap_stats.base_atk) * (1 + atk_percent_bonus) + artifact_stats.flat_atk

    crit_rate = char_stats.crit_rate + weap_stats.crit_rate + artifact_stats.crit_rate
    crit_dmg = char_stats.crit_dmg + artifact_stats.crit_dmg
    crit_multiplier = (crit_dmg + 1) if (random.random() < crit_rate) else 1

    return final_attack_stat * skill_dmg_percent * crit_multiplier
