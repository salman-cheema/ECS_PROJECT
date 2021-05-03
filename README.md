### Implementation
#### Resources
- Ec2
- Cloudwatch alarm
- SNS 
- Lambda
- SES
#### What does it do
- It create `Ec2` with `cloudwatch agent and cloudwatch alarm`.
- When a specific like `MetricName:CPUUtilization` exceed it's defined value.
- It notify `SNS` topic.
- That `SNS tigger lambda` which is subscribed to it.
- That `lambda` parse the event of sns and customize the message and send a mail with the help of `SES` administrator. 

#### How it work
- It work with the help of nested stack.
- First Template is Roles, it create roles which are needed for `Lambda` and `Ec2 to use cloudwatcg agent`.
    - It output the 2 things `lambdaroleArn` and `CloudwatchAgentRole` --> name
- That output `lambdaroleArn` is sent to the `lambda stack` as a parameter because lambda need that role.
    - As a output it produce `lambda.arn` 
- That ouput is sent to `lambda.arn` is sent to `SNS stack` as a parameter because SNS need that arn to trigger lambda.
    - As a output it produce `Sns.arn`.
- Last stack is Ec2+cloudwatchalarm it take 2 param one from role `CloudwatchAgentRole` and other `sns.arn` for cloudwatch alarm to notify that sns in case of action.


#### Note:
- I have practised `import export` functions of cfn but I face issue while creating nested stack and deleteing stack.
- All the things which i did with outputs i tried to do it with import and export 
- For e.g i Had exported the `role.arn` from role stack and try to import it in nested parent stack as input param but when i tried to create stack it say i could not found the exported property i have added `dependsOn` property so that they should create in order but still that `import param` does not work.
- Reason:
    - If we are creating the stack which is exporting the value and the stack which is importing the value
    in the same nested stack then this `import,export` will not work.
- And If i have to delete it again import export make issue mean that export property is being used in another stack delete that first.
- To overcome these issues I created all the stacks and the information which i needed I passed it as simple `Output`
- In the `parent nested stack` where I have to send input param I used `stackname.outputs.logical-id` and used the `dependOn` property.
