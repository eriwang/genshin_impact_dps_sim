from matplotlib import pyplot

from controller import Controller
from fischl import WeaponStats, ArtifactStats, Fischl


def main():
    controller = Controller()
    trials = 10000

    # Feather +20 ATK is 311
    # Artifact +20 ATK% is 46.6, Crit rate is 31.3, dmg is 62.2

    rust = WeaponStats(449, 0.377, 0)  # Rust 80/80
    crit_rate_artifacts = ArtifactStats(311, 2 * 0.466, 0.4, 0.2)
    rust_trials = [controller.simulate_total_damage(Fischl(rust, crit_rate_artifacts), 10) for _ in range(trials)]

    slingshot = WeaponStats(314, 0, 0.285)  # Slingshot 80/80
    crit_dmg_artifacts = ArtifactStats(311, 2 * 0.466, 0.2, 0.8)
    slingshot_trials = [controller.simulate_total_damage(Fischl(slingshot, crit_dmg_artifacts), 10)
                        for _ in range(trials)]

    if trials == 1:
        print(rust_trials[0])
        print(slingshot_trials[0])
        return

    pyplot.hist(rust_trials, alpha=0.5, label='Rust')
    pyplot.hist(slingshot_trials, alpha=0.5, label='Slingshot')
    pyplot.xlabel('Total Damage over 10 seconds')
    pyplot.ylabel('Frequency')
    pyplot.legend(loc='upper right')
    pyplot.title('Estimated Simulated Damage for Rust v. Slingshot for Fischl Auto-Attacks')
    pyplot.show()


if __name__ == '__main__':
    main()
