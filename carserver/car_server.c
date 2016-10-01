#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <time.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#include <wiringPi.h>

#define BUFSIZE 512

#define MOTOR_GO_FORWARD   digitalWrite(1,HIGH);digitalWrite(4,LOW);digitalWrite(5,HIGH);digitalWrite(6,LOW)
#define MOTOR_GO_BACK	   digitalWrite(4,HIGH);digitalWrite(1,LOW);digitalWrite(6,HIGH);digitalWrite(5,LOW)
#define MOTOR_GO_RIGHT	   digitalWrite(1,HIGH);digitalWrite(4,LOW);digitalWrite(6,HIGH);digitalWrite(5,LOW)
#define MOTOR_GO_LEFT	   digitalWrite(4,HIGH);digitalWrite(1,LOW);digitalWrite(5,HIGH);digitalWrite(6,LOW)
#define MOTOR_GO_STOP	   digitalWrite(1, LOW);digitalWrite(4,LOW);digitalWrite(5, LOW);digitalWrite(6,LOW)

typedef struct CLIENT {
	int fd;
	struct sockaddr_in addr;
}CLIENT;

int main(int argc, char *argv[])
{
    int sockfd;
    int listenfd;
    int connectfd;

    int ret;
    int maxfd=-1;
    struct timeval tv;

    struct sockaddr_in server_addr;
    struct sockaddr_in client_addr;

    socklen_t len;
    int portnumber;

    char buf[BUFSIZE]={0xff,0x00,0x00,0x00,0xff};

    int z,i,maxi = -1;
    int k;
    fd_set rset,allset;

    CLIENT client[FD_SETSIZE];

    /*RPI*/
    wiringPiSetup();
    /*WiringPi GPIO*/
    pinMode (1, OUTPUT);	//IN1
    pinMode (4, OUTPUT);	//IN2
    pinMode (5, OUTPUT);	//IN3
    pinMode (6, OUTPUT);	//IN4

    pinMode (3, OUTPUT);	//beed
	
	/*Init output*/
	digitalWrite(1,HIGH);
	digitalWrite(4,HIGH);
	digitalWrite(5,HIGH);
	digitalWrite(6,HIGH);
	
	digitalWrite(1,HIGH);

    if(argc != 2)
    {
        printf("Please add portnumber!");
        exit(1);
    }

    if((portnumber = atoi(argv[1]))<0)
    {
        printf("Enter Error!");
        exit(1);
    }


    if((listenfd = socket(PF_INET, SOCK_STREAM, 0)) == -1)
    {
        printf("Socket Error!");
        exit(1);
    }


    memset(&server_addr, 0, sizeof server_addr);
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(portnumber);


    if((bind(listenfd, (struct sockaddr *)(&server_addr), sizeof server_addr)) == -1)
    {
        printf("Bind Error!");
        exit(1);
    }

    if(listen(listenfd, 128) == -1)
    {
        printf("Listen Error!");
        exit(1);
    }

    for(i=0;i<FD_SETSIZE;i++)
    {
	client[i].fd = -1;
    }

    FD_ZERO(&allset);
    FD_SET(listenfd, &allset);

    maxfd = listenfd;

    printf("waiting for the client's request...\n");

    while (1)
    {
	rset = allset;

	tv.tv_sec = 0;      //wait 1u second
        tv.tv_usec = 1;
    
        ret = select(maxfd + 1, &rset, NULL, NULL, &tv);
    
	if(ret == 0)
	    continue;
	else if(ret < 0)
	{
	    printf("select failed!");
       	    break;
	}
	else
	{
	    if(FD_ISSET(listenfd,&rset)) // new connection
	    {
		len = sizeof (struct sockaddr_in);
		if((connectfd = accept(listenfd,(struct sockaddr*)(&client_addr),&len)) == -1)
		{
		    printf("accept() error");
		    continue;
                }

		for(i=0;i<FD_SETSIZE;i++)
		{
		    if(client[i].fd < 0)
		    {
		        client[i].fd = connectfd;
			client[i].addr = client_addr;
			printf("[HELLO]You got a connection from %s\n",inet_ntoa(client[i].addr.sin_addr));
			break;
		    }
		}

		if(i == FD_SETSIZE)
		    printf("Overfly connections");

		FD_SET(connectfd,&allset);

		if(connectfd > maxfd)
		    maxfd = connectfd;

		if(i > maxi)
		    maxi = i;
	    }
	    else
	    {
		for(i=0;i<=maxi;i++)
		{
		    if((sockfd = client[i].fd)<0)
		        continue;

                    if(FD_ISSET(sockfd,&rset))
		    {
			bzero(buf,BUFSIZE + 1);
			if((z = read(sockfd,buf,sizeof buf)) >0)
			{
      		            buf[z] = '\0';
                	    //printf("num = %d received data:%s\n",z,buf);
			    /*
                            for(k=0;k<z;k++) 
			        printf("buf[%d]=%x\n",k,buf[k]);
			    */
			    if(z == 5)
			    {
				if(buf[1] == 0x00)
				{
	     			    switch(buf[2])
		         	    {
					case 0x01:MOTOR_GO_FORWARD; printf("forward\n");break;
					case 0x02:MOTOR_GO_BACK;    printf("back\n");break;            						
					case 0x03:MOTOR_GO_LEFT;    printf("left\n");break;
					case 0x04:MOTOR_GO_RIGHT;   printf("right\n");break;
					case 0x00:MOTOR_GO_STOP;    printf("stop\n");break;
					default: break;
				    }
				    digitalWrite(3, HIGH);
				}
				else
				{
				    digitalWrite(3, LOW);
				    MOTOR_GO_STOP;
				}
			    }
			    else if(z == 6)
			    {
				if(buf[2] == 0x00)
				{
				    switch(buf[3])
				    {
					case 0x01:MOTOR_GO_FORWARD; printf("forward\n");break;
					case 0x02:MOTOR_GO_BACK;    printf("back\n");break;							
					case 0x03:MOTOR_GO_LEFT;    printf("left\n");break;
					case 0x04:MOTOR_GO_RIGHT;   printf("right\n");break;
					case 0x00:MOTOR_GO_STOP;    printf("stop\n");break;
					default: break;
				    }
				    digitalWrite(3, HIGH);
				}
				else
				{
				    digitalWrite(3, LOW);
				    MOTOR_GO_STOP;
				}
			    }
			    else
			    {
				digitalWrite(3, LOW);
				MOTOR_GO_STOP;
			    }
				
                        }
		        else
		        {
		            printf("disconnected by client!");
	                    close(sockfd);
	                    FD_CLR(sockfd,&allset);
	                    client[i].fd = -1;
		        }
	            }
	        }
            }
        }
    }
    close(listenfd);
    return 0;
}

