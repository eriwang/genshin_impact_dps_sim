from matplotlib import pyplot

from controller import Controller
from fischl import Fischl


def main():
    controller = Controller()
    trials = 1000

    # Rust 80/80
    rust_trials = [controller.simulate_total_damage(Fischl(449, 0.377, 0), 10) for _ in range(trials)]

    # Slingshot 80/80
    slingshot_trials = [controller.simulate_total_damage(Fischl(314, 0, 0.285), 10) for _ in range(trials)]

    if trials == 1:
        print(rust_trials[0])
        print(slingshot_trials[0])
        return

    pyplot.hist(rust_trials, alpha=0.5, label='Rust')
    pyplot.hist(slingshot_trials, alpha=0.5, label='Slingshot')
    pyplot.legend(loc='upper right')
    pyplot.show()


if __name__ == '__main__':
    main()
