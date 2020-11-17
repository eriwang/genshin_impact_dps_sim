import random

_AUTO_ATTACK_DMG_PERCENTS = [0.441, 0.468, 0.581, 0.577, 0.721]
_AUTO_ATTACK_TIME = 2.6 / 5


class Fischl:
    def __init__(self, weap_base_atk, weap_percent_atk, weap_crit_rate):
        # Fischl 80/80
        self._char_base_atk = 216
        self._char_percent_atk = 0.18
        self._char_crit_rate = 0.05
        self._char_crit_dmg = 0.5

        self._weap_base_atk = weap_base_atk
        self._weap_percent_atk = weap_percent_atk
        self._weap_crit_rate = weap_crit_rate

        self._next_auto_index = 0
        # self._skill_ready_ts = 0
        # self._burst_ready_ts = 0

    def run_iteration(self, controller, current_time):  # pylint: disable=unused-argument
        auto_attack_damage = _calculate_damage(self._char_base_atk + self._weap_base_atk,
                                               self._char_percent_atk + self._weap_percent_atk,
                                               0,
                                               self._char_crit_rate + self._weap_crit_rate,
                                               self._char_crit_dmg,
                                               _AUTO_ATTACK_DMG_PERCENTS[self._next_auto_index])

        controller.perform_active_action(self, auto_attack_damage, _AUTO_ATTACK_TIME)
        self._next_auto_index = (self._next_auto_index + 1) % len(_AUTO_ATTACK_DMG_PERCENTS)


def _calculate_damage(char_weap_base_atk, atk_percent_bonus, artifact_flat_atk_bonus, crit_rate, crit_dmg,
                      skill_dmg_percent):
    final_attack_stat = char_weap_base_atk * (1 + atk_percent_bonus) + artifact_flat_atk_bonus
    crit_multiplier = (crit_dmg + 1) if (random.random() < crit_rate) else 1
    return final_attack_stat * skill_dmg_percent * crit_multiplier
