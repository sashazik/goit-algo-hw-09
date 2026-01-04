import timeit

# Набір монет, заданий в умові
COINS = [50, 25, 10, 5, 2, 1]

def find_coins_greedy(amount):
    """
    Жадібний алгоритм: обирає найбільші доступні монети.
    Часова складність: O(N), де N - кількість номіналів монет.
    """
    result = {}
    for coin in COINS:
        if amount >= coin:
            count = amount // coin
            amount -= count * coin
            result[coin] = count
    return result

def find_min_coins(amount):
    """
    Алгоритм динамічного програмування: знаходить справжній мінімум монет.
    Часова складність: O(A * N), де A - сума, N - кількість номіналів.
    """
    # dp[i] зберігатиме мінімальну кількість монет для суми i
    # Ініціалізуємо нескінченністю, крім 0
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # last_coin_used[i] зберігає останню монету, додану для досягнення суми i
    # Це потрібно для відновлення результату (які саме монети взяли)
    last_coin_used = [0] * (amount + 1)

    # Заповнюємо таблицю DP
    for i in range(1, amount + 1):
        for coin in COINS:
            if i >= coin:
                if dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1
                    last_coin_used[i] = coin

    # Відновлюємо результат (backtracking)
    result = {}
    current_sum = amount
    while current_sum > 0:
        coin = last_coin_used[current_sum]
        if coin in result:
            result[coin] += 1
        else:
            result[coin] = 1
        current_sum -= coin
        
    return result

# --- Тестування та порівняння ---
if __name__ == "__main__":
    test_amounts = [113, 1000, 5000, 10000]
    
    print(f"{'Сума':<10} | {'Greedy (sec)':<15} | {'Dynamic Prog (sec)':<18} | {'Результат співпадає?'}")
    print("-" * 65)

    for amount in test_amounts:
        # Заміряємо час для жадібного алгоритму
        greedy_time = timeit.timeit(lambda: find_coins_greedy(amount), number=100)
        
        # Заміряємо час для динамічного програмування
        # Для великих сум зменшуємо кількість повторів, бо DP повільний
        runs = 10 if amount > 2000 else 100
        dp_time = timeit.timeit(lambda: find_min_coins(amount), number=runs)
        
        # Нормалізуємо час до 100 запусків для коректного порівняння
        if runs != 100:
            dp_time = dp_time * (100 / runs)

        res_greedy = find_coins_greedy(amount)
        res_dp = find_min_coins(amount)
        
        # Для даного набору монет результати мають співпадати за кількістю монет
        is_same = sum(res_greedy.values()) == sum(res_dp.values())

        print(f"{amount:<10} | {greedy_time:.6f}        | {dp_time:.6f}           | {is_same}")