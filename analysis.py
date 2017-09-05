import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import simulation


def simulate_hands(strategy, n=10):
    scores = []
    for i in range(n):
        hand = simulation.simulate_hand(strategy)
        score = hand.score()
        scores.append(score)
    return scores


def calculate_scores(n=100):
    random_scores = simulate_hands(strategy=simulation.random_strategy, n=n)
    best_oracle_scores = simulate_hands(strategy=simulation.best_oracle_strategy, n=n)
    worst_oracle_scores = simulate_hands(strategy=simulation.worst_oracle_strategy, n=n)
    best_blind_scores = simulate_hands(strategy=simulation.best_blind_strategy, n=n)
    all_scores = {'random': random_scores,
                  'best_oracle': best_oracle_scores,
                  'worst_oracle': worst_oracle_scores,
                  'best_blind': best_blind_scores}
    return all_scores


def plot_score_distribution(all_scores):
    f, axarr = plt.subplots(4, sharex=False, figsize=(4, 12))
    axarr[0].hist(all_scores['best_oracle'], bins=range(30), normed=1)
    axarr[0].set_title('Best-Oracle Strategy')
    axarr[0].set_xlabel('Points')
    axarr[0].set_ylabel('Fraction of Hands')

    axarr[1].hist(all_scores['best_blind'], bins=range(30), normed=1)
    axarr[1].set_title('Save-Most-Points Strategy')
    axarr[1].set_xlabel('Points')
    axarr[1].set_ylabel('Fraction of Hands')

    axarr[2].hist(all_scores['random'], bins=range(30), normed=1)
    axarr[2].set_title('Random Strategy')
    axarr[2].set_xlabel('Points')
    axarr[2].set_ylabel('Fraction of Hands')

    axarr[3].hist(all_scores['worst_oracle'], bins=range(30), normed=1)
    axarr[3].set_title('Worse-Possible Strategy')
    axarr[3].set_xlabel('Points')
    axarr[3].set_ylabel('Fraction of Hands')
    plt.tight_layout()
    plt.savefig('plots/strategy_distributions')


def print_strategy_means(all_scores):
    'Strategy Average Scores:'
    for strategy in all_scores.keys():
        print(strategy, ': ', np.mean(all_scores[strategy]))


if __name__ == '__main__':
    all_scores = calculate_scores(10000)
    print_strategy_means(all_scores)
    plot_score_distribution(all_scores)
