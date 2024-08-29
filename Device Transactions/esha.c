/*********************************************************************
* Filename:   sha256.c
* Author:     Brad Conte (brad AT bradconte.com) 
* Modified:   Priyanka D. Harish
* Copyright:
* Disclaimer: This code is presented "as is" without any guarantees.
* Details:    Performs known-answer tests on the corresponding SHA1
	          implementation. These tests do not encompass the full
	          range of available test vectors, however, if the tests
	          pass it is very, very likely that the code is correct
	          and was compiled properly. This code also serves as
	          example usage of the functions.
*************************** HEADER FILES ***************************/
#include <stdio.h>
#include <memory.h>
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
#include <sys/time.h>
#include <math.h>

/****************************** MACROS ******************************/
#define ROTLEFT(a,b) (((a) << (b)) | ((a) >> (32-(b))))
#define ROTRIGHT(a,b) (((a) >> (b)) | ((a) << (32-(b))))
#define CH(x,y,z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x,y,z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x) (ROTRIGHT(x,2) ^ ROTRIGHT(x,13) ^ ROTRIGHT(x,22))
#define EP1(x) (ROTRIGHT(x,6) ^ ROTRIGHT(x,11) ^ ROTRIGHT(x,25))
#define SIG0(x) (ROTRIGHT(x,7) ^ ROTRIGHT(x,18) ^ ((x) >> 3))
#define SIG1(x) (ROTRIGHT(x,17) ^ ROTRIGHT(x,19) ^ ((x) >> 10))
#define SHA256_BLOCK_SIZE 32            // SHA256 outputs a 32 byte digest

/**************************** DATA TYPES ****************************/
typedef unsigned char BYTE;             // 8-bit byte
typedef unsigned int  WORD;             // 32-bit word, change to "long" for 16-bit machines
typedef struct {
	BYTE data[64];
	WORD datalen;
	unsigned long long bitlen;
	WORD state[8];
} SHA256_CTX;

/**************************** VARIABLES *****************************/
static const WORD k[64] = {
	0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
	0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
	0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
	0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
	0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
	0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
	0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
	0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
};

int NUMBYTES; // long
int ITERATIONS=0;
int mode;
int realStride; //rs
int blockSize; //B long
int way;        
int NUMBANKS; //P
int blockSize_pow;
int realStride_pow;
BYTE buf[SHA256_BLOCK_SIZE];
int PRINT;
int CPRINT;

/*********************** FUNCTION DEFINITIONS ***********************/
// Added by HK - Function to convert a hexadecimal character to its corresponding byte value
unsigned char hex_to_byte(unsigned char hex) {
    if (hex >= '0' && hex <= '9') {
        return hex - '0';
    } else if (hex >= 'A' && hex <= 'F') {
        return hex - 'A' + 10;
    } else if (hex >= 'a' && hex <= 'f') {
        return hex - 'a' + 10;
    }
    return 0; // Invalid hexadecimal character
}

void hex_string_to_byte_array(unsigned char *hex_string, unsigned char *byte_array) {
    size_t len = strlen(hex_string);
    for (size_t i = 0; i < len; i += 2) {
        byte_array[i / 2] = (hex_to_byte(hex_string[i]) << 4) | hex_to_byte(hex_string[i + 1]);
    }
}

void sha256_transform(SHA256_CTX *ctx, const BYTE data[])
{
	WORD a, b, c, d, e, f, g, h, i, j, t1, t2, m[64];
	for (i = 0, j = 0; i < 16; ++i, j += 4)
		m[i] = (data[j] << 24) | (data[j + 1] << 16) | (data[j + 2] << 8) | (data[j + 3]);
	for ( ; i < 64; ++i)
		m[i] = SIG1(m[i - 2]) + m[i - 7] + SIG0(m[i - 15]) + m[i - 16];
	a = ctx->state[0];
	b = ctx->state[1];
	c = ctx->state[2];
	d = ctx->state[3];
	e = ctx->state[4];
	f = ctx->state[5];
	g = ctx->state[6];
	h = ctx->state[7];

	for (i = 0; i < 64; ++i) {
		t1 = h + EP1(e) + CH(e,f,g) + k[i] + m[i];
		t2 = EP0(a) + MAJ(a,b,c);
		h = g;
		g = f;
		f = e;
		e = d + t1;
		d = c;
		c = b;
		b = a;
		a = t1 + t2;
	}
	ctx->state[0] += a;
	ctx->state[1] += b;
	ctx->state[2] += c;
	ctx->state[3] += d;
	ctx->state[4] += e;
	ctx->state[5] += f;
	ctx->state[6] += g;
	ctx->state[7] += h;
}

void sha256_init(SHA256_CTX *ctx)
{
	ctx->datalen = 0;
	ctx->bitlen = 0;
	ctx->state[0] = 0x6a09e667;
	ctx->state[1] = 0xbb67ae85;
	ctx->state[2] = 0x3c6ef372;
	ctx->state[3] = 0xa54ff53a;
	ctx->state[4] = 0x510e527f;
	ctx->state[5] = 0x9b05688c;
	ctx->state[6] = 0x1f83d9ab;
	ctx->state[7] = 0x5be0cd19;	
}

void sha256_update_optimized(SHA256_CTX *ctx, const BYTE data[], size_t len, int *page, int **blocks, int i_times, int j_times, int realStride_pow)
{	
	WORD k;
	int j, i, block, rowTimesStride, stride;
	for(i=0; i<i_times; i++)  // block access
	{  
	   block = page[i];
	   for(j=0; j<j_times; j++) // stride access
	   {
		   stride =  blocks[block][j]; 		
		   rowTimesStride = stride<<(realStride_pow);
		   for(k=0; k<realStride; ++k) // elements access 
		   {
				ctx->data[ctx->datalen] = data[j*16 + k];
				ctx->datalen++;
				if (ctx->datalen == 64) 
				{
				   sha256_transform(ctx, ctx->data);
				   ctx->bitlen += 512;
				   ctx->datalen = 0;
				}
			}   
		}
	}
}

void sha256_final(SHA256_CTX *ctx, BYTE hash[])
{
	WORD i;
	i = ctx->datalen;
	// Pad whatever data is left in the buffer.
	if (ctx->datalen < 56) {
		ctx->data[i++] = 0x80;
		while (i < 56)
			ctx->data[i++] = 0x00;
	}
	else {
		ctx->data[i++] = 0x80;
		while (i < 64)
			ctx->data[i++] = 0x00;
		sha256_transform(ctx, ctx->data);
		// HK The following commented line was not in original code. Adding original three lines
		memset(ctx->data, 0, 56);
	}

	// Append to the padding the total message's length in bits and transform.
	ctx->bitlen += ctx->datalen * 8;
	ctx->data[63] = ctx->bitlen;
	ctx->data[62] = ctx->bitlen >> 8;
	ctx->data[61] = ctx->bitlen >> 16;
	ctx->data[60] = ctx->bitlen >> 24;
	ctx->data[59] = ctx->bitlen >> 32;
	ctx->data[58] = ctx->bitlen >> 40;
	ctx->data[57] = ctx->bitlen >> 48;
	ctx->data[56] = ctx->bitlen >> 56;
	sha256_transform(ctx, ctx->data);

	for (i = 0; i < 4; ++i) {
		hash[i]      = (ctx->state[0] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 4]  = (ctx->state[1] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 8]  = (ctx->state[2] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 12] = (ctx->state[3] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 16] = (ctx->state[4] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 20] = (ctx->state[5] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 24] = (ctx->state[6] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 28] = (ctx->state[7] >> (24 - i * 8)) & 0x000000ff;
	}
}

int** blocks_access_allocate(){
	int numBlocks = NUMBYTES/blockSize; // 8192/256 = 32
	int numStrides = blockSize/realStride; // 256/16 = 16
	int **array;
	int i;
	array = (int**)malloc(numBlocks * sizeof(int *));
    //printf("\n NumBlocks = %d and NumStrides = %d\n", numBlocks, numStrides);
	if(array == NULL){
		fprintf(stderr, "out of memory\n");
		exit(1);
	}
	for(i = 0; i < numBlocks; i++){
		array[i] = (int*)malloc(numStrides * sizeof(int));
		if(array[i] == NULL){
			fprintf(stderr, "out of memory\n");
			exit(1);
		}
  	}
	return array;
}

void blocks_access_del(int** array){
  int i;
  for (i = 0; i < NUMBYTES/blockSize; i++){  
    free(array[i]);  
  }  
  free(array);  
}

int PowerOfTwo(int x)
{
	int y;
	y = log(x) / log(2);
	return y;
}


//this function defines the realStrides chunks
//within each blocks. so each block contains
// blockSize/realStride chunks of real strides
// with the mapping in place for block[i], we
// make sure that its real strides belong to 
//the same bank (assuming a stride by stride
//allocation across banks). 
void set_blocks_strides(int** blocks)
{
  int i, j, k, l, num, n, m;  
  for(i=0, n=0; i<NUMBYTES/(NUMBANKS*blockSize); i++) // super blocks P*B
  {
    for(j=0; j<NUMBANKS; j++){  // blocks B
      n=i*NUMBANKS+j;
      for(k=0; k<blockSize/realStride; k++)  // real strides rs
        blocks[n][k] = j + k*NUMBANKS + i*(NUMBANKS*blockSize)/realStride;      
    }
  }
}

// this function sets the access for blocks
// way = 1 is P-way parallel, way = NUMBANKS is 1-way parallel
// the page[] array contains this access pattern based on way
void setPageTable(int *page, int way){
	int i, factor=0; 
    int numBlocks = NUMBYTES / blockSize;

	for (int i = 0; i < numBlocks; i++) {
		//HK was i>1 
		if (i > 0 && (i * way) % numBlocks == 0)
			factor++;
		page[i] = (i * way + factor) % numBlocks;
	}
}

BYTE * allocate(long numbytes){
   char * vector;
   vector = (BYTE*)malloc(numbytes* sizeof(BYTE));
   if(vector==NULL){
       printf("error\n");
   }else{
        return vector;
   }
}

void set(BYTE* str)
{
  memset(str,'c', NUMBYTES-1);
  str[NUMBYTES - 1] = '\0';
}

void del(BYTE* str){
  free(str);
}

int * allocateInt(int numbytes){
   int * vector;
   vector = (int*)malloc(numbytes* sizeof(int));
   if(vector==NULL){
    	printf("error\n");
   }else{
    	return vector;
   }
}

void setInt(int* str){
  memset(str,0, NUMBYTES-1);
}

void delInt(int* str){
  free(str);
}

//void sha256_test(BYTE input[])
void sha_test(const char *input)
{
	//struct timeval tv1, tv2;
	//long execution_time;
	//the allocation of strides to blocks
	int** blocks = blocks_access_allocate();
	set_blocks_strides(blocks);
	//vector to perform writes
	BYTE* str = allocate(NUMBYTES);
	set(str);
	//the setting of the page table
	int* page = allocateInt(NUMBYTES/blockSize);
	setPageTable(page, way); 
	int i_times = NUMBYTES/blockSize;
	int j_times = blockSize/realStride;

	SHA256_CTX ctx;
	
	int pass = 1;
 	//gettimeofday(&tv1, NULL);
	for (int index=0; index < ITERATIONS; index++){	
		if (PRINT == 1 && index == ITERATIONS - 1) 
			CPRINT = 1;
			//CPRINT = 0;
		sha256_init(&ctx);
		sha256_update_optimized(&ctx, input, NUMBYTES, page, blocks, i_times, j_times, realStride_pow);
		sha256_final(&ctx, buf);
	}
	//gettimeofday(&tv2, NULL);
	//execution_time= (tv2.tv_sec - tv1.tv_sec) * 1000000L + tv2.tv_usec - tv1.tv_usec;

        FILE *file = fopen("output.txt","w");
	if (PRINT==1){
		for (int index = 0; index < sizeof(buf); index++)
		{
			fprintf(file, "%02X", (unsigned char)buf[index]);		
		}		
	}
	fclose(file);

	//printf("\n Execution time: %ld nsec\n", execution_time);
/* 	sha256_init(&ctx);
	printf("\nsha256_init;");
	gettimeofday(&tv1, NULL);
	sha256_update_optimized(&ctx, input, NUMBYTES, page, blocks, i_times, j_times, realStride_pow);
	gettimeofday(&tv2, NULL);
	printf("\nsha256_update_optimized;");
	sha256_final(&ctx, buf);
	printf("\nsha256_final;");
	pass = pass && !memcmp(input, buf, SHA256_BLOCK_SIZE);
	execution_time= (tv2.tv_sec - tv1.tv_sec) * 1000000L + tv2.tv_usec - tv1.tv_usec;
	printf("\n Execution time: %ld nsec", execution_time); */

	del(str);
	delInt(page);
	blocks_access_del(blocks);	
}

void maint(int way, const char *text)
{
	char* result;
	int stridesInBlock = 1;
	int Blocks = 8;
	const char *hex_string = text;
	way = way;
	CPRINT = 0;
	PRINT = 1;
	mode = 0;
	ITERATIONS = 1;
	NUMBANKS = 8;
	realStride = strlen(hex_string);
	blockSize = realStride * stridesInBlock;
	NUMBYTES = blockSize * Blocks;

    	blockSize_pow = PowerOfTwo(blockSize);
    	realStride_pow = PowerOfTwo(realStride);
	sha_test(hex_string);
}
