/* Purpose(s): To complete the given jobs(some or all) such that
 *             the sum of "total completion time" and "total rejection cost" is minimized.
 * Author: Siddharth Chhatbar
 * Date: 07-10-2021
 * Persons discussed w/: None
 * References: None
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void print_pe(int n, int p[n], int e[n])
{
    printf("%d\n", n);

    for (int i = 0; i < n; i++)
    {
        printf("%d %d\n", p[i], e[i]);
    }
    printf("\n");

    return;
}

void print_STP(int len, int J[len][2])
{
    printf("The accepted jobs in STP order:\n");
    for (int i = 0; i < len; i++)
    {
        printf("%d %d\n", J[i][0], J[i][1]);
    }
    printf("\n");

    return;
}

void sort_J(int len, int J[len][2])
{
    int counter = 1;

    while (counter < len)
    {
        for (int i = 0; i < len - counter; i++)
        {
            if (J[i][0] > J[i+1][0])
            {
                for (int j = 0; j < 2; j++)
                {
                    int temp = J[i][j];
                    J[i][j] = J[i+1][j];
                    J[i+1][j] = temp;
                }
                    
            }
        }
        counter++;
    }

    return;
}

int completion(int len, int J[len][2])
{
    int completion_time = 0;

    for (int i = 0; i < len; i++)
    {
        completion_time += J[i][0];
    }
    return completion_time;
}

void jobs(int n, int p[], int e[])
{
    srand(time(NULL));

    int J[n][2], rejection_cost = 0, j = 0;

    for (int i = 0; i < n; i++)
    {
        if (rand() % 2)
        {
            J[j][0] = p[i];
            J[j++][1] = e[i];
        }

        else
        {
            rejection_cost += e[i];
        }
    }

    sort_J(j, J);
    int completion_time = completion(j, J);
    int objective = completion_time + rejection_cost;

    print_pe(n, p, e);
    print_STP(j ,J);

    printf("total completion time = %d\n", completion_time);
    printf("total rejection cost = %d\n", rejection_cost);
    printf("objective = %d\n", objective);
    
    return;
}

int main(int argc, char **argv)
{
    int n; // n is the number of jobs
    if (!scanf("%d", &n))
    {
        printf("Invalid instance");
        exit(0);
    }

    int p[n], e[n]; // p is the continuous time period to finish the job, e is rejection cost of the job

    for (int i = 0; i < n; i++)
    {
        if(!scanf("%d %d", &p[i], &e[i]))

        {
            printf("Invalid instance");
            exit(0);
        }
    }

    jobs(n, p, e);

    return 0; 
}
