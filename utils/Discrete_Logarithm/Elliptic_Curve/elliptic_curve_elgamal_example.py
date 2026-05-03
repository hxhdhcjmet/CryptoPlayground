from elliptic_curve import Elliptic_Curve

# 实例方程为y^2 = x^3 + 7x + 6 mod 13
a,b = 7,6
EC = Elliptic_Curve(a=7,b=6,p=13)
print("生成密钥中...")
# 选取生成元G
G = (1,1)
# 选择私钥d
d = 3
# 计算公钥P
P = EC.ktimes(d,G)
print(f"公钥为:(E,11,{G},{P})")

print("加密中...")
M = (11,7)
print(f"加密信息映射到E中点为:{M}")
print("M是否在E上?",EC.is_inCurve(M))

# 随机选取k,这里选的k是2
k = 2
# 计算密文对
C_1 = EC.ktimes(k,G)
C_2 = EC.add(M,EC.ktimes(k,P))
print(f"密文对为:({C_1,C_2})")
print(f"私钥为:(E,11,{G},{d})")
print("解密中...")
dC_1 = EC.ktimes(d,C_1)# 先乘d
neg_dC_1 = (dC_1[0],(-dC_1[1])%13)# 再取反
M_ = EC.add(C_2,neg_dC_1)
print(f"解密结果为:{M_}")

