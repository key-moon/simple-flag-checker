FLAG=Alpaca{h4sh_4lgor1thm_1s_b4s3d_0n_MD5_4nd_keccak}
gcc challenge/dump.c -o challenge/dump

gcc -O3 challenge/main.c -DFLAG_LEN=${#FLAG} -DFLAG_DATA=$(echo $FLAG | challenge/dump) -o checker
rm challenge/dump;
