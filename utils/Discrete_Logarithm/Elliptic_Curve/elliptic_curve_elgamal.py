

def square_of_sqrt():
    # 创建模13的平方和平方根之间的对应关系
    S2S = dict()
    for i in range(13):
        sq = (i**2) % 13
        if sq not in S2S:
            S2S[sq] = []
        S2S[sq].append(i)
    return S2S

S2S = square_of_sqrt()

def f1(x):
    y_1s = (x**3+6) %13
    return y_1s

def f2(x):
    y2_s = (x**3 + 2*x + 8) % 13
    return y2_s

def f3(x):
    y3_s = (x**3 + 2*x) %13
    return y3_s


def create_all_solutions_table(f):
    # 创建方程在Z_13上的解
    points = set()
    for x in range(13):
        y_s = f(x)
        # 找到这个y_s对应的所有x
        if y_s in S2S:
            for y in S2S[y_s]:
                points.add((x,y))
    return list(points)


def main():
    # 主函数
    print("(1)方程中所有解为:")
    S1 = create_all_solutions_table(f1)
    S1.sort(key = lambda x:(x[0],x[1]))
    S1.append("O")
    print(S1)

    print("(2)方程中所有解为:")
    S2 = create_all_solutions_table(f2)
    S2.sort(key = lambda x:(x[0],x[1]))
    S2.append("O")
    print(S2)

    print("(3)方程中所有解为:")
    S3 = create_all_solutions_table(f3)
    S3.sort(key = lambda x:(x[0],x[1]))
    S3.append("O")
    print(S3)

print(S2S)
main()




