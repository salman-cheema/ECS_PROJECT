## ECS ::
 Is a service which manage container service,it is not product.
 It maintain availablity of the application and allow every user to scale containers when necessary.
## FOR ECS WITH S3 + SQS + Cloudfomation + AUtoscaling follow this link.
- https://github.com/aws-samples/ecs-refarch-batch-processing



## ECS EXAMPLPE:::
  - GOAL
     - Mongo database should be installed/running in private
     - Flask app should be running and it should connect to mongo 
     - Application load balancer in front of Flask app to distribute the traffic
     - Every thing should be dockerized.
We will achieve this `dockerized goal` with the help of docker and and maintain it's 
orchestration with `ECS`
STEP 1::
  -  Create a `cluster`
      - Name
      - Number of Instances
      - Type of Instances
      - VPC , Security group and roles
STEP 2::
  - Create a `Task Definition` for Mongo
  `Task Definition` it is related to container image , cpu , memory , we say it as `Task`
   we create a task definition for every new `image` 
    - Type ( Faragate or EC2)
    - Name
    - `Task` Role `Optional IAM role that tasks can use to make API requests to authorized AWS services.`
    - Task execution role 
       - `This role is required by tasks to pull container images and publish container logs to Amazon CloudWatch on your behalf. If you do not    have the ecsTaskExecutionRole already, we can create one for you.` 
    - Task size   The task size allows you to specify a fixed size for your task
       - Task memory (GB)    The amount of memory (in MiB) used by the task.
       - Task CPU (vCPU)     The number of CPU units used by the task
    - Container Definitions
       - we define container's inside that tab.
          - Container name*
          - Image* from `dockerhub` or `ECR`
          - Port mappings of conatiner
          - Environment variables that you want to pass to conatiner
          many more things which are not done yet.
STEP 3::
  - Create Service for Mongo:
     - A service lets you specify how many copies of your task definition to run and maintain in a cluster. You can optionally use an Elastic     Load Balancing load balancer to distribute incoming traffic to containers in your service. Amazon ECS maintains that number of tasks and   coordinates task scheduling with the load balancer. You can also optionally use Service Auto Scaling to adjust the number of tasks in      your service.
    - Launch type
    - Task Definition
       - Family (name of task defintion which you have created in task definition)
       - Revision of task definition
    - Cluster
    - Service name
    - Number of task.  (A service lets you specify how many copies of your task definition to run and maintain in a cluster)
                        Task are nothing but running contaier of task defintion
    - Deployments.   we select the deployment type here because whenever we decide to release our new 
                     version of code according to that type deployment is done.
    - `Configure network` for service
      - Cluster VPC ( same vpc which we have chossen for cluster)
      -  Subnets
      - secuirty groups ( open the ports in security group which you need for your container )
      - Auto assign IP if you think you need internet to download something
    - ` Load balancing `  (An Elastic Load Balancing load balancer distributes incoming traffic across the tasks running in your service)
      - Till now I have used  Application Load Balancer.
        - we define the load balaner infront of `service`
          - `why?`
             - Because we define conatiner to be run as task they get ip's through which we connect with them
                but they keep on changing if we deploy new version of code or somathing else happen due to docker management behaviour
                of ECS it deploy new conatiner and keep the service up by providing new conatiner's and due to that new ip's 
                are assigned and we can't rely on ip in such case so we do 2 things
                - If we want to connect to container from the other conatiner we use `Docker service discovery` method 
                   in this case we connect through this name it is defined while creating `service` for `Task definition`.
                - If we want to connect to service which is running multiple `task/conatiner` of same `task definition`
                  then they can have multiple ip's so how we are going to distribute the traffic and the problem of changing ip's is also
                  there.
                  So, we use load balancer infront of service which is pointing to service so if ip's keep on changing we don't have 
                  to change anything and traffic is distribute by load balancer.
      - Create load balancer and target group:
        - Your load balancer routes requests to the targets in a target group using the target group settings that you specify, and performs      health checks on the targets using the health check settings that you specify.
        - Target group name
        - Type (ip ,lambda, instance)
        - Protocol (The protocol the load balancer uses when routing traffic to targets in this target group)
        - port ( The port the load balancer uses when routing traffic to targets in this target group (1-65535))
        - VPC 
        - Now create load balancer select type and vpc.
    - `Service Discovery`
       - Service discovery uses Amazon Route 53 to create a namespace for your service, which allows it to be discoverable via DNS.
          example which we have discuss in load balancing
    - ` Auto scaling `
        Automatically adjust your service’s desired count up and down within a specified range in response to CloudWatch alarms. You can modify your Service Auto Scaling configuration at any time to meet the needs of your application.
STEP 4::
  - I have created a flask image in that flask app it access mongodb and show the dbs inside it.
  - Then I have uploaded the flask image to docker hub
  - created a task defintion for flask
  - service for flask and deifned 3 `task` for flask and created a load balancer for service and when all three `task` were running 
     i took `DNS` of `ALB` and hit it i got the databases.
  - Then to release new version of code i changed the revison of `task defintion` and updated the `service` so that it cam point to
     new version of code beacuse of that `ECS`  destroyed the previous provisioned conatiner and created a new one's but service never went down after all the desired conatiner were provisioned previous one's went down.
  - Traffic is routed to differnet instaces behind ALB.
