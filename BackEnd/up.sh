echo "*************** Server starting ***************"



echo "*************** Running compose Up ***************"
sudo docker-compose up --build --scale web=3 --scale asgi_web=3
# sudo docker-compose up

