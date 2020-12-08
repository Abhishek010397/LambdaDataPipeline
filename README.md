# LambdaEC2CloudWatch


1.    Create a custom AWS Identity and Access Management (IAM) policy and execution role for your Lambda function.

2.    Create Lambda functions that stop and start your EC2 instances.

3.    Create CloudWatch Events rules that trigger your function on a schedule. For example, you could create a rule to stop your EC2 instances at night, and another to start them again in the morning.

1. Create an IAM policy and role
2.    Create an IAM role for Lambda. When attaching a permissions policy, search for and choose the IAM policy that you created.

Create Lambda functions that stop and start your EC2 instances

      1.    In the Lambda console, choose Create function.

      2.    Choose Author from scratch.

      3.    Under Basic information, add the following:
            For Function name, enter a name that identifies it as the function used to stop your EC2 instances. For example, "StopEC2Instances".
            For Runtime, choose Python 3.7.
            Under Permissions, expand Choose or create an execution role.
            Under Execution role, choose Use an existing role.
            Under Existing role, choose the IAM role that you created.

      4.    Choose Create function.
      5.    Under Basic settings, set Timeout to 10 seconds.
      6.    Choose Save.

      7.    Repeat steps 1-7 to create another function. Do the following differently so that this function starts your EC2 instances:
            In step 3, enter a Function name it as the function used to start your EC2 instances. For example, "StartEC2Instances".
            
 Test your Lambda functions

     1.    In the Lambda console, choose Functions.

     2.    Select one of the functions that you created.

     3.    Choose Actions, and then choose Test.

     4.    In the Configure test event dialog, choose Create new test event.

     5.    Enter an Event name, and then choose Create.

Note: You don't need to change the JSON code for the test event—the function doesn't use it.

     6.    Choose Test to execute the function.

     7.    Repeat steps 1-6 for the other function that you created.

Tip: You can check the status of your EC2 instances before and after testing to confirm that your functions work as expected.


Create rules that trigger your Lambda functions

    1.    Open the CloudWatch console.

    2.    In the left navigation pane, under Events, choose Rules.

    3.    Choose Create rule.

    4.    Under Event Source, choose Schedule.

    5.    Do either of the following:
          For Fixed rate of, enter an interval of time in minutes, hours, or days.
          For Cron expression, enter an expression that tells Lambda when to stop your instances. For information on the syntax of expressions, see Schedule                     
          Expressions for Rules.
Note: Cron expressions are evaluated in UTC. Be sure to adjust the expression for your preferred time zone.

    6.    Under Targets, choose Add target.

    7.    Choose Lambda function.

    8.    For Function, choose the function that stops your EC2 instances.

    9.    Choose Configure details.

    10.    Under Rule definition, do the following:
    For Name, enter a name to identify the rule, such as "StopEC2Instances".
    (Optional) For Description, describe your rule. For example, "Stops EC2 instances every night at 10 PM."
    For State, select the Enabled check box.

    11. Choose Create rule.

    12. Repeat steps 1-11 to create a rule to start your EC2 instances. Do the following differently:
    In step 5, for Cron expression, enter an expression that tells Lambda when to start your instances.  
    In step 8, for Function, choose the function that starts your EC2 instances.
    In step 10, under Rule definition, enter a Name like "StartEC2Instances", and optionally enter a Description like "Starts EC2 instances every morning at 6     AM."
    
    
# Lambda Cross Account S3 File Upload


Attach the policy to Source S3 Bucket of the Source Account

The Bucket policy set up in the source AWS account. Do NOT forget to change the account number and bucket name in the below policy.

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "DelegateS3Access",
                "Effect": "Allow",
                "Principal": {"AWS": "<<Account-Number-of-source-a/c>>"},
                "Action": ["s3:ListBucket","s3:GetObject"],
                "Resource": [
                    "arn:aws:s3:::YOUR-SOURCE-BUCKET-NAME-HERE/*",
                    "arn:aws:s3:::YOUR-SOURCE-BUCKET-NAME-HERE"
                ]
            }
        ]
    }
            
Create a Lambda function as :-

     Give A Name To The Lambda Function.
     Head-On to IAM.
     Create A role For Lambda Function.
     Attach Policies to the respective role.
 

Policies:-

1.S3 Full-Access
     
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:*",
                    "Resource": "*"
                }
            ]
        }
     
2.Lambda-Basic Execution Role
           
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "logs:CreateLogGroup",
                    "Resource": "arn:aws:logs:us-east-1:<<Account-Number-Source:*>>"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                    ],
                    "Resource": [
                        "arn:aws:logs:us-east-1:<<Source-A/c-Number>>:log-group:/aws/lambda/LambdaBucketS3:*"
                    ]
                }
            ]
        }
    
3. Create An Inline Policy:-
                  
        {
                "Version": "2012-10-17",
                "Statement": 
                    {
                        "Effect": "Allow",
                        "Action": "sts:AssumeRole",
                        "Resource": "arn:aws:iam::<<Destination-A/c-Number>>:role/<<Name-of-Dest-A/c-Role>>"
                    }
        }

Now Edit the Trust-Relationship of the respective role in Source A/c

Attach a Assume-Role-Policy as:-


        {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                        "Service": "lambda.amazonaws.com",
                        "AWS": "arn:aws:iam::<<Dest-A/c-Number>>:role/<<Dest-A/c-Role-Name>>"
                    },
                    "Action": "sts:AssumeRole"
                    }
                ]
        }


Head On to the Destination Account

1.Create A role as:-

          Select type of trusted entity as:-
                                  1.Another AWS Account
                                  2. Provide Your Root A/c Number in the Desired Checkbox
               
       
2. Attach Policy to it

Policies:-

1.S3 Full Access

    {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PolicyForAllowUpload",
                    "Effect": "Allow",
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::<<Dest-bucket-name>>/*"
                }
            ]
    }

