//RC4实现C语言版本

#include<stdio.h>
#include<stdint.h>
#include<string.h>

//定义状态
typedef struct{
    uint8_t s[256];
    int i,j;
}RC4_context;

void swap(uint8_t *a,uint8_t *b){
    //交换函数手动实现
    uint8_t temp = *a;
    *a = *b;
    *b = temp;
}

void rc4_init(RC4_context *ctx,const uint8_t *key,size_t key_len){
    //初始化S盒
    int i;
    for (i = 0;i<256;i++){
        ctx->s[i] = i;
    }
    //交换
    int j = 0;
    for (i = 0;i<256;i++){
        j = (j + ctx->s[i] + key[i % key_len]) % 256;
        swap(&ctx->s[i],&ctx->s[j]);
    }
    ctx->i = 0;
    ctx->j = 0;
}

//加解密用同一个函数
void rc4_process(RC4_context *ctx,const uint8_t *input,uint8_t *output,size_t len){
    //输入input,输出output,不区分加解密
    int i = ctx->i;
    int j = ctx->j;
    uint8_t *s = ctx->s;

    //生成密钥流
    size_t k;
    for (k = 0;k<len;k++){
        i = (i+1) % 256;
        j = (j + s[i]) % 256;
        swap(&s[i],&s[j]);

        uint8_t t = (s[i] + s[j]) % 256;

        output[k] = input[k] ^ s[t];
    }

    //更新索引
    ctx->i = i;
    ctx->j = j;
}


int main(){
    printf("开始测试RC4...\n");
    const char *key = "test_key_202646";
    const char *m = "Hello world!This is RC4 in C";
    size_t len = strlen(m);

    uint8_t encryption[64];
    uint8_t decryption[64];

    printf("明文原文:%s\n",m);

    RC4_context rc4;

    //开始加密
    printf("开始加密...\n");
    rc4_init(&rc4,(uint8_t*)key,strlen(key));
    rc4_process(&rc4,(uint8_t*)m,encryption,len);
    printf("加密结果:\n");
    int i;
    for (i = 0;i < len;i++){
        printf("%02X",encryption[i]);
    }
    printf("\n");

    //开始解密
    printf("开始解密...\n");
    rc4_init(&rc4,(uint8_t*)key,strlen(key));
    rc4_process(&rc4,encryption,decryption,len);
    decryption[len] = '\0';//加截至符
    printf("解密结果:%s\n",decryption);
    return 0;



}