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
	"Statement": [{
			"Sid": "DelegateS3Access",
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::<<root-a/c-number>>:root"
			},
			"Action": [
				"s3:ListBucket",
				"s3:GetObject"
			],
			"Resource": [
				"arn:aws:s3:::bucket-name/*.extension-to-be allowed",
				"arn:aws:s3:::bucket-name"
			]
		},
		{
			"Sid": "S3AllowedExtensions",
			"Effect": "Deny",
			"Principal": "*",
			"Action": "s3:PutObject",
			"NotResource": "arn:aws:s3:::bucket-name/*.extensions-to-be-allowed"
		}
	]
    }
       
       
Attaching SNS topic for S3 Bucket Role:-
          
	  {
             "Version": "2012-10-17",
             "Id": "s3EventSNS",
             "Statement": [
               {
                 "Sid": "s3EventSNSNotification",
                 "Effect": "Allow",
                 "Principal": "*",
                 "Action": "sns:Publish",
                 "Resource": "arn:aws:sns:us-east-1:a/c-no.:my_sns",
                 "Condition": {
                   "ArnLike": {
                     "aws:SourceArn": "arn:aws:s3:::s3-bucket-name"
                  }
            }
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
 
 
 
3. SNS Publish Policy For Lambda:-

        {
           "Version": "2012-10-17",
           "Statement": [
               {
                 "Sid": "VisualEditor0",
                 "Effect": "Allow",
                 "Action": "sns:Publish",
                 "Resource": "arn:aws:sns:*:a/c no.:*"
               }
             ]
           }


4. Create An Inline Policy:-
                  
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

EC2 Instance Profile Role

1.EC2S3PolicyRole


    {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "S3Access",
                    "Effect": "Allow",
                    "Action": [
                    "s3:PutObject"
                    ],
                    "Resource": "arn:aws:s3:::<<bucket-name>>/*"
                }
            ]
        }
	
	
2.Attach SSMFullAccess to the Instance 



Convert Python Script to .exe File

Step 1:
Install the library pyinstaller in Windows Server.

           python -m pip install pyinstaller
           
           
Step 2:
Go into the directory where your ‘.py’ file is located.

Step 3:
Press shift⇧ button and simultaneously right click at the same location. You will get below box.


Step 4:
Click on ‘Open PowerShell window here’.

Step 5:
Type the command given below in that PowerShell window.

          .\pyinstaller --onefile -w 'filename.py'

Step 6:
After typing the command ‘Hit the Enter’.
It will take some time to finish the process depending on the size of the file

Step 7:
See the directory it should contain a dist folder.

Next Comes the Task Scheduler to run the python code as a cron job
Windows Task Scheduler is a component that gives the ability to schedule and automate tasks in Windows by running scripts or programs automatically at a given moment.

Steps:-

    1.Go to Task Scheduler
    2.Create Task
    3.Give Name to your Task
    4.Click on the Actions and specify your python.exe file path (can be found by 'where python' on Command Prompt)
    5.Paste the path of your python code at the start checkbox.
    6.Give the name of your python file in the arguments section .
    7.Specify triggers based on the time when you want to start and stop your pyhton executable file.
    
To provide Administrative permission to the Task scheduler

   1.Open Command Prompt As Administartor
   
   
   2.Run the following Command
                 
		 SCHTASKS /Create /TN "Name" /SC (HOUR/Minute Of your choice) /MO 5(5 denotes no. of minutes) /TR:Path/to/the/loggedin/User/filename.bat(C:\User\Abhi)\f.bat) /RU Username
		 /RP Password /RL HIGHEST(to run the script with higher privilleges)
		 
   3. To delete any tasks from task scheduler
    
                 SCHTASKS /delete /TN "taskname"
		 
   4. To disable a task in the task scheduler
    
                 Disable-ScheduledTask -TaskName "SystemScan"

To schedule the PowerShell script, specify the following parameters in Task Scheduler Create Basic Task Action tab:

    1.Action: Start a program
    2.Program\script: powershell
    3.Add arguments (optional): -File [Specify the file path to the script here]

Click “OK” to save your changes.


To run Shell-Script as a Cron job in Linux Machine:

    1. Make a Directory(Best Practice),give it a name
    2. Go to the directory and create a .sh file as:- vi/vim scripts.sh
    3. Change the permission of the file as:- chmod +x filename.sh
    4. Next is to edit the crontab of Linux Machine as:- sudo crontab -e
    5. Provide the scheduling time as:- */5 * * * * path/to/filename.sh (5 denotes no. of minutes)
    
    
Note

    1. if you get a Network Connectivity issue while running aws cli command in EC2 Instances.
    2. Check the Instance profile policy if they have mentioned policy attached for specific service requested.
    3. Do aws configure in root section:-
                                          sudo -i
					  aws configure

RDP into Windows Machine Using SSm(System Session Manager)

Connect to the Instance Using AWS Console Managerwith SSM Enabled

   1.Input password as a secure string: 
                                          
					  $Password = Read-Host -AsSecureString

                                          New-LocalUser “User01” -Password $Password
			
   2. For Administrtive Access Add the USER to Administartive User Group:-
   
					  Add-LocalGroupMember -Group “Remote Desktop Users/Administrators” -Member “User01”


   3.Terminate the session from the Console
   
   4.Use AWS SSM CLI Command to create a tunnel for doing RDP into the Instance
   
       aws ssm start-session --target <instance-id> --document-name AWS-StartPortForwardingSession --parameters "localPortNumber=55678,portNumber=3389"

Data Pipeline Architecture Cross AWS S3 Accounts:

![alt text](https://github.com/Abhishek010397/LambdaDataPipeline/blob/master/Architecture.png)
