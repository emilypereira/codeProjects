/* program - mtfencode.c
* by - Emily Pereira V00728841
* date - February 2015 
* 
* input: .txt file
* output: .mtf file
*   
* takes the input file and creates a string table that is outputed to the output file* also looks for duplicate words in input file before adding them to string table
* */
 
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
  
#define LINE_BUFF 81
#define WORD_SIZE 21
#define MAX_WORDS 120
#define LINE_AMOUNT 100
  
int word_count = 0;
int line_num = 0;
int tok_words = 0;
FILE *fout = NULL;
char words[MAX_WORDS][WORD_SIZE];
char lines[LINE_AMOUNT][LINE_BUFF];
 
void tokenize(char *);
void moveToFront(char *,int); 
void insertWord(char []);
void updateFile1(int);
void updateFile2(int);
void updateFile3(char);
 
int main(int argc, char *argv[]){
     FILE *fpin; 37     fpin = fopen(argv[1], "r");
 
     if(fpin == NULL){
         printf("Could not open file\n");
         return 1;
     } else{
         int i;
         size_t n;
         n = strlen(argv[1]);
         char fileName[n+1];
  
         /*changes .txt to .mtf*/
         strcpy(fileName,argv[1]);
         i = n-3;
         fileName[i++] ='m';
         fileName[i++]='t';
         fileName[i]='f';
 
         fout = fopen(fileName, "wb");
 
         /*prints the magic numbers to the output file */
         fputc(0xfa,fout);
         fputc(0xce,fout);
         fputc(0xfa,fout);
         fputc(0xde,fout);
 
         /*reads in the input file line by line and calls tokenize*/
         while (feof(fpin)==0){
             while(fgets(lines[line_num], LINE_BUFF,fpin) != NULL){
                 tokenize(lines[line_num]);
                 line_num++;
             }
         }
   	}
    fclose(fpin);
    fclose(fout);
    return 0;
}

/*Adapted from Seng265 C programming slides #83-108 by Dr.Zastre */
void tokenize(char *inLine){
     char *token;
     char str[WORD_SIZE];
     token = strtok(inLine, " ");
     while(token != NULL){
        tok_words++;
         strncpy(str, token, WORD_SIZE);
         insertWord(str);
         memset(str,0,WORD_SIZE);
         token = strtok(NULL, " ");
     }
     return;
}
 
/*moves a word that is already in the words array to the "front" of the array */
void moveToFront(char *str, int pos){
    int i,x,n;
    char temp [WORD_SIZE];
     x = WORD_SIZE;
     n = word_count-1;
     if(word_count > 1){
 
    /*moves the strings in words up by 1 to account for the duplicate word being moved*/        
    	for(i = pos;i < n;i++){
			strcpy(temp,words[i+1]);
			memset(words[i],0,x);
        	strcpy(words[i],temp);
    		memset(temp,0,x);
        	memset(words[i+1],0,x);
    	}

	    /*places the duplicate word at the end of the array*/
        memset(words[n],0,x);
        strcpy(words[n],str);
	}
    return;
}

/*This function either adds the word that has been tokenized by the tokenize function to the 
words array or it will call the moveToFront function*/
void insertWord(char str[]){
    int i,isEqual,count,pos;
    count = 0;
    char c1,c2;
    char *cp;
    for(i = 0; i < WORD_SIZE; i++){
        c1 = str[i];
        if(c1 == '\n') {
        	c2 = '\n';
        	c1 = '\0';
            str[i] = c1;
        }
    }

    /*checks if the word in str is already in the words array*/
    for(i = 0; i < word_count; i++) {
    	cp = words[i];
        isEqual = strcmp(str,cp);
        if(isEqual !=  0) {
            count++;
    	}

        /*the word in str is already in words, calls moveToFront*/
        if(isEqual == 0){
            pos = word_count-i;
            moveToFront(str,i);
            break;
        }
    }

    /*calls updateFile2 because str was already in the file*/
    if(count < word_count){
        updateFile2(pos);
    }
 
    /*adds str to words because it isn't already in words*/
    if(count == word_count && str[0] != '\0') {
        strcpy(words[word_count],str);
        updateFile1(word_count);
        word_count++;
    }
    updateFile3(c2);
    c2 = '\0';
    return;
}

/*prints to the output file the code # of the word and the letters of the word*/
void updateFile1(int pos) {
     int i,val;
     char c;
     val = (pos+1) + 128;
     fputc(val,fout);
     for(i = 0; i < WORD_SIZE; i++){
         c = words[pos][i];
         if(c == '\0'){
             break;
         }else {
             fputc(c,fout);
         }
     }
     return;
}
 
/*this function is called if a word is a duplicate, and it prints the words previous location 
to the output file */
void updateFile2(int pos){
     pos = pos + 128;
     fputc(pos,fout);
     return;
}
 
/*if there is a new line after a word, this function prints it to the file*/
void updateFile3(char c) {
     if(c == '\n') {
         fputc(c,fout);
     }     return;
}
