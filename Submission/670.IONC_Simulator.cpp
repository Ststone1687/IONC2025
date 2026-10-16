#include "Hat.h"
using namespace std;
#define ll long long
#define pb push_back

bool hat(int n, int k, std::vector<bool> answer, std::vector<bool> correct){
    if(k==1){
        int cnt=0;
        for(int i=0; i<n-1; i++){
            if(correct[i]) cnt++;
        }
        if(cnt%2) return true;
        else return false;
    }
    else{
        bool final=false;
        for(int i=0; i<answer.size(); i++){
            if(answer[i]) final^=1;
        }
        for(int i=0; i<correct.size(); i++){
            if(correct[i]) final^=1;
        }
        return final;
    }
}