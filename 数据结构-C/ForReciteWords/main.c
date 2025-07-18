#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define size 75

int main()
{
    void shuffles(int [], int);
    char words[size][30] = {"empirical","syndrome","empowerment","resilience","expertise","hierarchy","charismatic"//7
                            "intense","relief","extroverted","grumpy","pessimistic","jolly","meek","rivalry","traumatic","exert","clamor",//11
                            "amicably","fertility","consensus","robust","marginally","nurture","verbalizing","steeper","refractive","dementia","frailty","refrain","ameliorate","skew",//14
                            "bidding","urbanization","gravitate","infrastructure","sanitation","deploy","versatile",//7
                            "surpluses","resilient",//2
                            "redefining","malleable","irrigation","non-pneumatic","depleted","integral","commuters","autonomous",//8
                            "imagery","contemporary","enigmatic","ethereal","stroke","radical",//6
                            "brush and ink","calligraphy","sentimental","intrigued","nostalgic","exhilarated","euphemism","aesthetic","empowered","poised","polarize","populism","stigmatisation","intuition","unorthodox",//13
                            "irritate","trainee","sparingly","attire","diploma","discourse","etiquette","exterior","factual","sentimental","malleable","ramification","eligibility","remunerate","protagonist"};//10
    int dices[size];
    int i, j, copy, randomNum;

    for(i = 0; i < size; i++)
    {
        dices[i] = i;
    }

    srand(time(NULL));

    for(j = size - 1; j > 0; j--)
    {
        randomNum = rand()%j;

        copy = dices[j];
        dices[j] = dices[randomNum];
        dices[randomNum] = copy;
    }

    for(i = 0; i < 15; i++)
    {


        printf("No.%d is %s\n\n", (i + 1), words[dices[i]]);
    }

    return 0;
}
