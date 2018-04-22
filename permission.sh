sudo su
chown -R www-data pyscript
chmod -R 755 pyscript/
echo "" > container.log
echo "" > judge.log
chown www-data:www-data pyscript/container.log pyscript/judge.log
chown -R www-data docker/userData/
chmod -R 755 docker/userData/