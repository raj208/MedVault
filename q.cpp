#include<bits/stdc++.h>
using namespace std;

int main(){
    cout<<"Enter the first number: ";
    int a;
    cin>>a;
    cout<<"Enter the second number: ";
    int b;
    cin>>b;
    int sum = a + b;
    int one = 2;
    int two = 5;
    int three = 5;
    int four = 4;
    int five = 5;
    int six = 6;
    int seven = 3;
    int eight = 7;
    int nine = 9;;
    int zero = 6;
    vector<int>v;
    int tempSum = sum;
    if (tempSum == 0) {
        v.push_back(0);
    } else {
        while (tempSum > 0) {
            v.push_back(tempSum % 10);
            tempSum /= 10;
        }
        reverse(v.begin(), v.end()); 
    }
    int temp = 0;
    for (int i = 0; i < v.size(); i++)
    {
        if (v[i] == 1)
        {
            temp += one;
        }
        else if (v[i] == 2)
        {
            temp += two;
        }
        else if (v[i] == 3)
        {
            temp += three;
        }
        else if (v[i] == 4)
        {
            temp += four;
        }
        else if (v[i] == 5)
        {
            temp += five;
        }
        else if (v[i] == 6)
        {
            temp += six;
        }
        else if (v[i] == 7)
        {
            temp += seven;
        }
        else if (v[i] == 8)
        {
            temp += eight;
        }
        else if (v[i] == 9)
        {
            temp += nine;
        }
        else
        {
            temp += zero;
        }
    }
    cout<<temp<<endl;

    
    
    return 0;
}