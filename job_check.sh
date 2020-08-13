stc=`cat log.txt | grep 'stc' -A1 | grep 'currently running' | wc -l`
rlx2=`cat log.txt | grep 'rlx2' -A1 | grep 'currently running' | wc -l`
rlx=`cat log.txt | grep 'rlx' -A1 | grep 'currently running' | wc -l`
echo There are $stc static runs in progress.
cat log.txt | grep 'stc' -A1 | grep 'currently running' -B1 | grep 'stc'
echo There are $rlx2 rlx2 runs in progress.
cat log.txt | grep 'rlx2' -A1 | grep 'currently running' -B1 | grep 'rlx2'
echo There are $rlx rlx runs in progress.
