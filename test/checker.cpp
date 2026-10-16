/*  checker.cpp  ── IONC Simulator output-only 評測程式
 *  ---------------------------------------------------
 *  ‣ Input  (inf):  一行  subtaskId  ∈ 1…20
 *  ‣ Output (ouf):  一行  <savecode>
 *
 *  編譯：
 *    g++ -std=gnu++17 -DCMS -O2 -pipe -static -s checker.cpp -o checker.exe -lz
 *
 *  只依賴 testlib.h 與 <zlib.h>。
 */
#include "testlib.h"
#include <bits/stdc++.h>
#include <zlib.h>
using namespace std;

/*── CMS 用快捷函式 ───────────────────*/
void exit_WA()               { quitf(_wa, "Wrong Answer"); }
void exit_AC()               { quitf(_ok, "Accept"); }
void exit_PAR(double score)  { quitp(score, "Partially Correct"); } // 0~1

/*── Obfuscated key (44 bytes) ─────────────────────────*/
static const uint8_t PERM[44]={
 32,33,42,27,6,9,1,10,18,43,39,11,28,4,12,24,
 38,7,35,37,0,16,22,3,15,34,25,26,19,5,8,2,
 13,40,17,20,29,30,23,31,21,41,14,36};
static const uint8_t SALT[44]={
 168,20,40,102,131,144,42,113,50,231,249,243,196,66,
 134,246,252,85,255,27,16,165,229,186,28,151,210,7,
 8,159,9,107,69,54,62,94,12,158,31,2,95,44,21,64};
static const uint8_t OBF [44]={
 205,75,64,18,177,249,69,28,65,147,139,156,183,112,
 242,143,163,96,144,98,121,196,186,217,120,244,141,84,
 125,175,86,5,42,95,87,53,120,241,125,108,54,75,74,48};

/*──────────── SHA-256 (迷你實作，取自 PicoSHA2) ────────────*/
namespace sha256{
using u32 = uint32_t; using u8 = uint8_t;
inline u32 R(u32 x,int n){return (x>>n)|(x<<(32-n));}
inline u32 Ch(u32 x,u32 y,u32 z){return (x&y)^(~x&z);}
inline u32 Maj(u32 x,u32 y,u32 z){return (x&y)^(x&z)^(y&z);}
inline u32 BS0(u32 x){return R(x,2)^R(x,13)^R(x,22);}
inline u32 BS1(u32 x){return R(x,6)^R(x,11)^R(x,25);}
inline u32 SS0(u32 x){return R(x,7)^R(x,18)^(x>>3);}
inline u32 SS1(u32 x){return R(x,17)^R(x,19)^(x>>10);}
const u32 K[64]={
 0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,
 0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,
 0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,
 0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
 0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,
 0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,
 0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,
 0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
 0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,
 0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,
 0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
void hash(const u8* m,size_t len,u8* out){
    uint64_t bit=len*8; vector<u8>d(m,m+len);
    d.push_back(0x80); while((d.size()+8)%64) d.push_back(0);
    for(int i=7;i>=0;--i) d.push_back((bit>>(i*8))&0xFF);
    u32 h[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
              0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    u32 w[64];
    for(size_t off=0; off<d.size(); off+=64){
        for(int i=0;i<16;++i){
            w[i]=(d[off+4*i]<<24)|(d[off+4*i+1]<<16)|
                 (d[off+4*i+2]<<8)|d[off+4*i+3];
        }
        for(int i=16;i<64;++i) w[i]=SS1(w[i-2])+w[i-7]+SS0(w[i-15])+w[i-16];
        u32 a=h[0],b=h[1],c=h[2],d0=h[3],e=h[4],f=h[5],g=h[6],hh=h[7];
        for(int i=0;i<64;++i){
            u32 t1=hh+BS1(e)+Ch(e,f,g)+K[i]+w[i];
            u32 t2=BS0(a)+Maj(a,b,c);
            hh=g; g=f; f=e; e=d0+t1; d0=c; c=b; b=a; a=t1+t2;
        }
        h[0]+=a; h[1]+=b; h[2]+=c; h[3]+=d0;
        h[4]+=e; h[5]+=f; h[6]+=g; h[7]+=hh;
    }
    for(int i=0;i<8;++i){
        out[4*i]=(h[i]>>24)&0xFF; out[4*i+1]=(h[i]>>16)&0xFF;
        out[4*i+2]=(h[i]>>8)&0xFF; out[4*i+3]=h[i]&0xFF;
    }
}}
vector<uint8_t> hmac_sha256(const vector<uint8_t>& key,
                            const vector<uint8_t>& msg){
    const size_t B=64;
    vector<uint8_t> k=key;
    if(k.size()>B){ k.resize(32); sha256::hash(key.data(),key.size(),k.data()); }
    k.resize(B,0);
    vector<uint8_t> o(B),i(B);
    for(size_t j=0;j<B;++j){ o[j]=k[j]^0x5c; i[j]=k[j]^0x36; }
    vector<uint8_t> tmp=i; tmp.insert(tmp.end(),msg.begin(),msg.end());
    uint8_t inner[32]; sha256::hash(tmp.data(),tmp.size(),inner);
    vector<uint8_t> tmp2=o; tmp2.insert(tmp2.end(),inner,inner+32);
    uint8_t outer[32]; sha256::hash(tmp2.data(),tmp2.size(),outer);
    return vector<uint8_t>(outer,outer+32);
}

/*────────── Base64 URL-safe decode ──────────*/
vector<uint8_t> b64url_decode(string_view s){
    static uint8_t LUT[256]; static bool init=false;
    if(!init){
        fill(begin(LUT),end(LUT),0x80);
        string t="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
        string u="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
        for(int i=0;i<64;++i){
            LUT[(uint8_t)t[i]]=i; LUT[(uint8_t)u[i]]=i;
        }
        init=true;
    }
    vector<uint8_t> out; out.reserve(s.size()*3/4);
    uint32_t buf=0; int bits=0;
    for(char c:s){
        if(c=='=') break;
        uint8_t v=LUT[(uint8_t)c]; if(v&0x80) return {};
        buf=(buf<<6)|v; bits+=6;
        if(bits>=8){ bits-=8; out.push_back((buf>>bits)&0xFF); }
    }
    return out;
}

/*────────── zlib inflate ──────────*/
bool inflateZ(const vector<uint8_t>& in,string& out){
    if(in.empty()) return false;
    z_stream zs{}; zs.next_in=const_cast<Bytef*>(in.data()); zs.avail_in=in.size();
    if(inflateInit(&zs)!=Z_OK) return false;
    uint8_t buf[4096]; int ret;
    do{
        zs.next_out=buf; zs.avail_out=sizeof(buf);
        ret=inflate(&zs,Z_NO_FLUSH);
        if(ret==Z_NEED_DICT||ret==Z_DATA_ERROR||ret==Z_MEM_ERROR)
        { inflateEnd(&zs); return false; }
        out.append((char*)buf,sizeof(buf)-zs.avail_out);
    }while(ret!=Z_STREAM_END);
    inflateEnd(&zs); return true;
}

/*────────── 還原祕鑰 ──────────*/
vector<uint8_t> getSecret(){
    vector<uint8_t> key(44);
    for(int i=0;i<44;++i) key[PERM[i]] = OBF[i] ^ SALT[i];
    return key;
}

/*────────── 解析 savecode → raw JSON string ──────────*/
bool decodeSC(const string& sc,string& raw){
    auto blob=b64url_decode(sc); if(blob.size()<=32) return false;
    vector<uint8_t> comp(blob.begin()+32,blob.end());
    vector<uint8_t> sig(blob.begin(),blob.begin()+32);
    if(sig!=hmac_sha256(getSecret(),comp)) return false;
    return inflateZ(comp,raw);
}

/*────────── 抓 int flag（支援 "123" 或 123） ──────────*/
int getIntFlag(const string& j,const string& key){
    string pat="\""+key+"\"";
    size_t p=j.find(pat); if(p==string::npos) return 0;
    p=j.find(':',p+pat.size()); if(p==string::npos) return 0;
    ++p; while(p<j.size() && isspace(j[p])) ++p;
    if(p<j.size() && j[p]=='\"') ++p;
    return strtol(j.c_str()+p,nullptr,10);
}
/*────────── 卡片判定 ──────────*/
bool hasCard(const string& j,const string& id){
    return j.find("\""+id+"\"")!=string::npos ||
           j.find("\"card_"+id+"\"")!=string::npos ||
           j.find("\"has_"+id+"\"")!=string::npos;
}

/*────────── 計分 ──────────*/
double score(int sub,const string& j){
    if(sub>=1 && sub<=4){                        /* 每天 /100 */
        int pts=max(getIntFlag(j,"score_day"+to_string(sub)),
                    getIntFlag(j,"day"+to_string(sub)+"_score"));
        return max(0.0,min(1.0,pts/100.0));
    }
    if(sub==5){                                 /* Day5 /500 */
        int pts=max(getIntFlag(j,"score_day5"),
                    getIntFlag(j,"day5_score"));
        return max(0.0,min(1.0,pts/500.0));
    }
    const map<int,string> ends={
        {6,"end_be_quarrel"},{7,"end_be_yakitori"},{8,"end_ne_imoto"},
        {9,"end_ne_senpai"},{10,"end_ne_friend"},{11,"end_ne_sus"},
        {12,"end_te_true_end"}};
    if(ends.count(sub)) return getIntFlag(j,ends.at(sub))?1.0:0.0;

    const map<int,string> cards={
        {13,"out_of_the_box"},{14,"imoto_love"},{15,"forever"},
        {16,"friends"},{17,"yakitori"},{18,"sus"},
        {19,"imoto_daisuki"},{20,"owari"}};
    if(cards.count(sub)) return hasCard(j,cards.at(sub))?1.0:0.0;

    return 0.0;
}

/*────────── main ──────────*/
int main(int argc,char* argv[]){
    registerTestlibCmd(argc,argv);

    int sub=inf.readInt(0,20,"subtaskId");  // 某些題可能從 0 開始，保險改 0-20
    string savecode=ouf.readWord("savecode");

    string raw;
    // if(!decodeSC(savecode,raw)) exit_WA();
	decodeSC(savecode,raw);
	quitf(_wa, "Decode failed: %s", raw.c_str());

    double sc=score(sub,raw);
    if(sc>=0.999) exit_AC();
    else if(sc>0.0) exit_AC();
    else exit_WA();
}

/*
g++ -std=gnu++17 -DCMS -Wall -Wextra -O2 checker.cpp -o checker.exe -lz
*/