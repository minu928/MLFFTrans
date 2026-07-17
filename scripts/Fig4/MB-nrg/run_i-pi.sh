rm /tmp/ipi_localhost

i-pi config.xml &
echo $! > sipi.id

sleep 10

export OMP_NUM_THREADS=32

ipi_driver config.nrg mbx.json

id=`cat sipi.id`
kill $id

