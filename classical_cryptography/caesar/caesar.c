#include<stdio.h>
#include<stdint.h>
#include<string.h>
/*
caesar移位密码实现
*/

void caesar_encrypt(char* c,const char* m,size_t n,int k){
    /*
    c:加密后结果
    m:明文
    n:明文长度
    k:密钥
    */
   k = k % 26;
   for(size_t i = 0;i<n;i++){
        if((m[i]>='A'&&m[i]<='Z')||(m[i]>='a'&&m[i]<='z')){
            c[i] = (char)(m[i]+k);
        }else{
            c[i] = m[i];
        }
    }
}

void caesar_decrypt(char* m,const char* c,size_t n,int k){
//caesar密码解密算法
    k = k % 26;
    caesar_encrypt(m,c,n,-k);
}

int main(){
    int k = 190;
    char m[10] = "h[hhhAaAaA";
    char c[10] = "";
    printf("原文m:%s\n",m);
    caesar_encrypt(c,m,10,k);
    printf("加密后结果:%s\n",c);
    char m_decode[10]="";
    caesar_decrypt(m_decode,c,10,k);
    printf("解密后的结果为:%s\n",m_decode);
    return 0;
}