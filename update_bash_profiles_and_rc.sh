git add -u
git commit -m $1
git push

echo 172.16.50.181; ssh 172.16.50.181 cd vaelstmpredictor/; git pull
echo 172.16.50.176; ssh 172.16.50.176 cd vaelstmpredictor/; git pull
echo 172.16.50.177; ssh 172.16.50.177 cd vaelstmpredictor/; git pull
echo 172.16.50.163; ssh 172.16.50.163 cd vaelstmpredictor/; git pull
echo 172.16.50.182; ssh 172.16.50.182 cd vaelstmpredictor/; git pull
echo 172.16.50.218; ssh 172.16.50.218 cd vaelstmpredictor/; git pull
echo 172.16.50.235; ssh 172.16.50.235 cd vaelstmpredictor/; git pull
echo 172.16.50.159; ssh 172.16.50.159 cd vaelstmpredictor/; git pull
echo 172.16.50.157; ssh 172.16.50.157 cd vaelstmpredictor/; git pull
echo 172.16.50.237; ssh 172.16.50.237 cd vaelstmpredictor/; git pull
echo 172.16.50.187; ssh 172.16.50.187 cd vaelstmpredictor/; git pull