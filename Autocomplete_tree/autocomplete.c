#include <stdio.h>
#include "file.h"
#include "hashtable.h"
#include <stdlib.h>
#include "autocomplete.h"
#include "set.h"
#include "counters.h"
#include <string.h>
#include <stdbool.h>
/*
Nathan Schneider schnei.nathan@gmail.com 
The prefix tree is implemented in actree_t nodes, which are found in autocompletete.c. 
These nodes hold a frequency value, for how many times there exists the word that ends
 on that node in the index of words. To give autocomplete suggestions, we take our 
 prefix and traverse to it's ending character by moving through the tree. From there,
  a search of the remaining subtree to find the node with the largest frequency gives
   us the word that begins with our input prefix and is most frequent in the index. 
*/


//Global variables 
int maxval = 0; //used for finding the maximum value word  in a character subtree
char* maxword;


//Method prototypes
char* getinput(hashtable_t *index, actree_t* tree);
actree_t * maketree(hashtable_t* index);
static void insertword(char* word, int index,actree_t* node,int value);
static actree_t* newnode();
static char* findmax(char* word, actree_t* root);
static actree_t* traverse(actree_t* root, char* word,int index);
static void maxrecurse(void* arg, char* key, void* val);
void deletetree(void* val);



//stores a frequency value, a set of child nodes, and a string to hold the char or end word. 
//Our tree is made of these nodes
typedef struct actree {
    int val;
    set_t * letter_set;
    char* c;
}actree_t;


//To create a new node in the tree, we allocate memory for it and it's character set
actree_t* newnode(){
    actree_t * node = malloc(sizeof(actree_t));
    node->letter_set = set_new();
    return node;
}

//Holds an integer pointer with iterator helper methods to find the frequency sums
void countersum(void* arg,int key, int val){
    int *sum = (int*)arg;
    *sum = *sum +val;
}

//helps recursively insert words through hashtable_iterate
void inserthelper(void* arg,char* key, void* val){
    counters_t* ctrs = (counters_t*)val; //sum the counters in the index
    int sum = 0; counters_iterate(ctrs,&sum,countersum); //use the int* for summing the counters
    actree_t* root = (actree_t*)arg;
    insertword(key,0,root,sum); //insert the word at this point
}

//recursive method for inserting words into the tree
//bool freec was used for some tricky memory problems
void insertword(char* word, int index,actree_t* root,int value){
    char* c = malloc(2); //use the char as a len 2 string
    bool free_c_after = true; //assume we free it when we're done
    c[0] = word[index]; c[1] = '\0';
    set_t* set = root->letter_set;
    actree_t* node;
    if (set_find(set,c)==NULL) { //if we need to create the node to proceed, we do
        node = newnode();
        node->c = c;
        node->val = 0;
        free_c_after = false; //but then we must not free c
    }
    else {
        node = set_find(set,c); //the case we don't need to create the new node (leftover from anothe word)
    }

    if (word[index] == '\0'){ 
        node-> val = value;
        set_insert(set,c,node); //if this word is done being inserted (aka index at the end)
        free(c);    //set the end node to the word value, not the character
        c = malloc(strlen(word)+1);
        strcpy(c,word); //copy the word in 
        node->c = c;
    }
    else {
        set_insert(set,c,node); 
        insertword(word,index+1,node,value);//if not done being inserted, recurse further
    }
    if(free_c_after) free(c); //free c if we need to
}

//This is called from the main querier, and it starts the tree making process
actree_t * maketree(hashtable_t* index){
    actree_t *root = newnode();
    root->c = malloc(1);
    strcpy(root->c, ""); //initialize the new node
    hashtable_iterate(index,root,(void (*)(void *, const char *, void *))inserthelper); //iterate over the hashtable to 
    //add all words to the tree

    return root;
}

//Takes a word with index and traverses to the end of the word through the tree
//returns the node that it reaches
actree_t* traverse(actree_t* root, char* word,int index){
    char* c = malloc(2); c[0] = word[index]; c[1] = '\0'; //use the current character as a len 2 string
    set_t* set = root->letter_set;
    if (c[0]=='\0') return root; //if we've reached the end of the word
    if (set_find(set,c) == NULL) { //if there is no expected next node, return NULL
        free(c);
        return NULL;
    } 
    else { //or traverse to that node, increment the index and recurse
        actree_t* node = set_find(set,c);
        free(c);
        return traverse(node,word,index+1);
    }
}

//To find the max, we traverse to the end point of the prefix, then find
//the maximum value in the subtree after that
char* findmax(char* baseword, actree_t* root){  
    maxword = malloc(50); 
    maxval =0; 
    root = traverse(root,baseword,0); //get the node at the end of the prefix
    if (root==NULL){
        strcpy (maxword,""); //if there is no node, return no guess
        return maxword;
    }
    set_t* set = root->letter_set; //iterate over the set with the helper method that updates maxword
    set_iterate(set,root,(void (*)(void *, const char *, void *))maxrecurse);
    return maxword;
}

//Helper method called by set_iterate to traverse from the end point of the prefix to the max frequency node
//It compares to the max scores, and will change the maxword (autocomplete guess) as a result
void maxrecurse(void* arg, char* key, void* val){
    actree_t* node = (actree_t*)val;
    set_t* set = node->letter_set;

    //compare score
    int score = node->val;
    char* word = node->c;
    if (score > maxval){ //update the guess
        maxval = score;
        strcpy(maxword,word);
    }
    set_iterate(set,node,(void (*)(void *, const char *, void *))maxrecurse);
}

//Called from the main querier function. It takes the hashtable index and the created prefix tree
//it returns the end result of the query function, and autocompleted string of words
char* getinput(hashtable_t *index, actree_t* tree){
    char* query = malloc(200);
    char* input= malloc(50);
    char* guess;
    char c = 32; int i=0;

    //Setup for the char by char input
    system ("/bin/stty raw");
    system ("/bin/stty -echo");
    printf("Query: ");
    strcpy(query,"");

    //For each of the characters you fetch from the terminal
    while((c=getchar()) && c!=3 && c!=4){
        input[i] = c;
        input[i+1] = '\0';
        i++;

        //Backspace sets the last character to null
        if (c==8 && i>2){
            input[i-2] = '\0';
            i-=2;
        }

        //Pressing tab copies the guess onto the input, completing the word
        if(c == 9){
            strcpy(input,guess);
            strcat(query,input);

            i=0;
            strcpy(input,"");
        }

        //Space bar (32) or enter (13) ends the current word, resetting the autocomplete process
        if(c ==32 || c==13){
            strcat(query,input);
            i=0;
            strcpy(input,"");
        }
        //newline breaks the look and allows the input to reach the querier
        if(c==13){
            break;
        }

        //Find the max by traversing the tree
        guess = findmax(input,tree);

        //Escape codes to display the correct input style:
        
        // did you mean Dartmouth ? 
        // dart

        printf("\033[1J");
        printf("\033[H");
        printf("\033[[\r");
        printf("\nDid you mean: %s \n",guess);
        printf("\033[[\r");
        printf("Query? ");
        printf("%s%s",query,input);

    }
    //reset terminal settings
    system ("/bin/stty cooked");
    system ("/bin/stty sane");
    free(input);

    //Allow 3 (ctrl-c) and 4 (ctrl-d) end the autocomplete program
    if ( c==3 || c==4) return NULL;
    if (query == NULL) query = " ";

    return query;
}

//recursively delete the entire tree
void deletetree(void* val){
    actree_t* root = (actree_t*) val; //start at the root, delete the set of children recursively
    set_t* set = root->letter_set;
    free(root->c);
    free(root);
    set_delete(set,deletetree);
}