import random

from matplotlib import pyplot

from controller import Controller


class DummyChar:
    def __init__(self, base_damage):
        self._base_damage = base_damage

    def run_iteration(self, controller):
        controller.perform_active_action(self, self._base_damage + random.gauss(0, 1), 20)
        controller.perform_passive_action(0.5 * self._base_damage)


def main():
    controller = Controller()
    trials = 1000

    dummy_10_trials = [controller.simulate_total_damage(DummyChar(10), 100) for _ in range(trials)]
    dummy_11_trials = [controller.simulate_total_damage(DummyChar(11), 100) for _ in range(trials)]

    pyplot.hist(dummy_10_trials, alpha=0.5, label='Dummy Character 10')
    pyplot.hist(dummy_11_trials, alpha=0.5, label='Dummy Character 11')
    pyplot.legend(loc='upper right')
    pyplot.show()


if __name__ == '__main__':
    main()
