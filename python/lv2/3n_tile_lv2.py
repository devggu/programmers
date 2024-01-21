def solution(n):
    # DP 테이블 초기화
    dp = [0] * (n + 1)
    print(dp)
    # 기저 사례 처리
    dp[0] = 1  # 3x0 판은 빈 경우의 수로 1
    if n >= 1:
        dp[1] = 0  # 3x1 판은 채울 수 없으므로 0
    if n >= 2:
        dp[2] = 3  # 3x2 판은 3가지 방법으로 채울 수 있음

    # 3x3 이상의 판을 처리 
    for i in range(3, n + 1):
        # 3x(i-2) 판을 채우는 방법과 2개의 추가 블록을 이용한 방법
        dp[i] = dp[i - 2] * 3
        # 3x(i-4), 3x(i-6), ... 판을 채우는 방법들을 더함
        for j in range(4, i + 1, 2):
            dp[i] += dp[i - j] * 2

    return dp[n] % 1000000007


def solution2(n):
    if n % 2:
        return 0
    front = back = 1
    for _ in range(n//2):
        front, back = back, (4*back - front) % 1000000007
    return back

solution(8)